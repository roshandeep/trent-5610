import json
import time
import pandas as pd

from django.http import HttpResponse, request
from django.shortcuts import render

# third-part imports
from django.views.decorators.csrf import csrf_exempt
from core.classify import classify_question
from core.models import Intents, Questions, Intent_Answers, Variables

from core.train import trainbot


def load_variables():
    var_obj = Variables.objects.first()
    GREETING_MSG_EN = var_obj.greeting_msg_en
    GREETING_MSG_FR = var_obj.greeting_msg_fr
    APOLOGY_MSG = var_obj.apology_msg
    DEFAULT_FALLBACK_MSG = var_obj.default_fallback_msg
    MISCLASSIFY_THRESHOLD = var_obj.misclassify_threshold


def chatbot_home(request):
    template_name = 'core/chatbot_ui.html'
    # Only called the first time to load data from excel
    # load_data()
    var_obj = Variables.objects.first()
    GREETING_MSG_EN = var_obj.greeting_msg_en
    GREETING_MSG_FR = var_obj.greeting_msg_fr

    print(GREETING_MSG_EN)
    context = {
        "intro_en": GREETING_MSG_EN,
        "intro_fr": GREETING_MSG_FR,
    }
    return render(request, template_name, context)


@csrf_exempt
def canatracechatbot(request):
    response = {"status": None}
    if request.method == 'POST':
        chatbotInput = request.POST.get('input', False)
        language = request.POST.get('language', False)
        chatbotOutput = chatbot_query(chatbotInput, request, language)
        response['message'] = chatbotOutput
        response['status'] = "OK"
        time.sleep(2)
    else:
        response['error'] = "No post data found"

    return HttpResponse(json.dumps(response), content_type='application/json')


def chatbot_query(chatbotInput, request, language):
    var_obj = Variables.objects.first()
    # if language == 'EN':
    APOLOGY_MSG = var_obj.apology_msg_en
    DEFAULT_FALLBACK_MSG = var_obj.default_fallback_msg_en
    # elif language == 'FR':
    #     APOLOGY_MSG = var_obj.apology_msg_fr
    #     DEFAULT_FALLBACK_MSG = var_obj.default_fallback_msg_fr

    MISCLASSIFY_THRESHOLD = var_obj.misclassify_threshold
    # print(MISCLASSIFY_THRESHOLD, APOLOGY_MSG, MISCLASSIFY_THRESHOLD)

    fallback = APOLOGY_MSG
    result = ''
    try:
        result, intent_prob = classify_question(chatbotInput, language)
        # intent_prob is the class probability of the classified intent
        # Use default use probablity 30%

        intent_prob = float(intent_prob)
        print(intent_prob)
    finally:
        if float(intent_prob) <= MISCLASSIFY_THRESHOLD:
            result = fallback

        if result == fallback:
            if request.session.get('fallback_counter'):
                request.session['fallback_counter'] += 1
                if request.session.get('fallback_counter') >= 3:
                    result = DEFAULT_FALLBACK_MSG
            else:
                request.session['fallback_counter'] = 1
        else:
            request.session['fallback_counter'] = 0

        print('Fall back counter value = ', request.session.get('fallback_counter'))
    return result


def load_data():
    df1 = pd.read_excel('core/canatrace.xlsx', sheet_name='final', usecols=['Questions', 'Intents'])
    df2 = pd.read_excel('core/canatrace.xlsx', sheet_name='Intent & Answer',
                        usecols=['Intents', 'EN_Answer', 'FR_Answer'])

    # Run each object one by one because of Foreign Key Dependency

    intents_list = df1.Intents.unique()
    print(intents_list)
    objs1 = [
        Intents(
            intent=intent,
        )
        for intent in intents_list
    ]
    Intents.objects.bulk_create(objs1)

    objs2 = [
        Questions(
            question=row['Questions'],
            intents=Intents.objects.get(intent=row['Intents']),
        )
        for index, row in df1.iterrows()
    ]
    Questions.objects.bulk_create(objs2)

    row_iter2 = df2.iterrows()
    objs3 = [
        Intent_Answers(
            intent=Intents.objects.get(intent=row['Intents']),
            EN_Answer=row['EN_Answer'],
            FR_Answer=row['FR_Answer'],
        )
        for index, row in row_iter2
    ]
    Intent_Answers.objects.bulk_create(objs3)


def trainchatbot(request):
    trainbot()
    return HttpResponse("Model trained successfully")
