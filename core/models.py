from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Intents(models.Model):
    intent = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.intent

    class Meta:
        ordering = ['intent']


class Questions(models.Model):
    intents = models.ForeignKey(Intents, on_delete=models.DO_NOTHING)
    question = models.TextField(unique=True)

    def __str__(self):
        return "%s --> %s" % (self.intents, self.question)

    class Meta:
        ordering = ['intents']


class Intent_Answers(models.Model):
    intent = models.ForeignKey(Intents, on_delete=models.DO_NOTHING, unique=True)
    EN_Answer = models.TextField()
    FR_Answer = models.TextField()

    def __str__(self):
        return "%s --> %s" % (self.intent, self.EN_Answer)

    class Meta:
        ordering = ['intent']


class Variables(models.Model):
    greeting_msg_en = models.TextField(default="")
    greeting_msg_fr = models.TextField(default="")
    apology_msg_en = models.TextField(default="")
    apology_msg_fr = models.TextField(default="")
    default_fallback_msg_en = models.TextField(default="")
    default_fallback_msg_fr = models.TextField(default="")
    misclassify_threshold = models.FloatField(
        validators=[MinValueValidator(1.0), MaxValueValidator(100.0)],
    )

    def __str__(self):
        return 'Chatbot variables'
