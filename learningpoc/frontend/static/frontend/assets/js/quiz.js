function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
            }
        }
    }
    return cookieValue;
}
function quiz(){
    var form = document.getElementById("quiz1");
    var collectedData = {
        'csrfmiddlewaretoken': getCookie('csrftoken'),
        'form' : FormData(form),
    }
    console.log("inside");
    // $.ajax({
    //     url: 'check-quiz',
    //     type: 'POST',
    //     data: collectedData,
    //     datatype: 'json',
    //     success: function (response) {
    //         console.log("success")
    //     },
    //     error: function () {
    //         alert("We faced some difficulty in logging you in. Please try again later.")
    //     }
    // });
}