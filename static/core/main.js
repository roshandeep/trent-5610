
$(document).ready(function () {



    var input_field = document.getElementById("chat-input-text_id")
    input_field.addEventListener("keyup", function(event) {
        // Number 13 is the "Enter" key on the keyboard
        if (event.key === "Enter") {
          // Cancel the default action, if needed
          event.preventDefault();
          // Trigger the button element with a click
          $("#send_btn").click()
        }
    });

    $(".chat-animation-div").hide()
    $("#send_btn").click(function(){
        var chatbot_input = $("#chat-input-text_id").val()
        $("#chat-input-text_id").val("")
        var reply_div="<div class='chat-bubble me'> <div class='chat-msg'> <p>"+chatbot_input+"</p></div><div class='chat-img'> <img src='/static/core/img/user-avatar4.png' alt='user' style='width:50px;border-radius: 50%;'> </div> </div>"
        $(reply_div).insertBefore(".chat-animation-div")

        $("#chat-screen").animate({ scrollTop: 1000000}, 1000);
        $("#chatbot-body").animate({ scrollTop: 1000000}, 1000);

        $(".chat-animation-div").show()
        $.ajax({
            type: "POST",
            url: "/canatracechatbot/",
            data:{
                'input':chatbot_input,
                'language':lang
            },
            dataType:'json',
            success: function(data){
                response = data['message']
                var reply_div="<div class='chat-bubble you'> <div class='chat-img'> <img src='/static/core/img/tracy.PNG' alt='tracy' style='width:50px;border-radius: 50%;'> </div> <div class='chat-msg'> <p>"+response+"</p></div></div>"
                $(reply_div).insertBefore(".chat-animation-div")

                $(".chat-animation-div").hide()
                $("#chat-screen").animate({ scrollTop: 1000000}, 1000);
                $("#chatbot-body").animate({ scrollTop: 1000000}, 1000);
            }
        })

    });
});


