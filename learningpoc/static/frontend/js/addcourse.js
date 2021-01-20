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
    function addcourse(){
        console.log("inside");
        var name = document.getElementById("course_name").value;
        var description = document.getElementById("description").value;
        var price = document.getElementById("course_price").value;
        var vid = document.getElementById("video").value;
        console.log(name,description,price,number,vid);
        var q_list = [];
        if(number > 1)
        {
            for(i=0;i<number-1;i++)
            {
                try {
                var q = document.getElementById("question " + (i+1)).value;
                var opt1 = document.getElementById("option1 " + (i+1)).value;
                var opt2 = document.getElementById("option2 " + (i+1)).value;
                var opt3 = document.getElementById("option3 " + (i+1)).value;
                var ans = document.getElementById("answer " + (i+1)).value;
                var question = {
                    "question":q,
                    "option1":opt1,
                    "option2":opt2,
                    "option3":opt3,
                    "answer":ans
                }
                q_list.push(question);
                }
                catch{
                    console.log("deleted");
                }
            }
        }
        console.log(q_list);
        var collectedData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'course_name':name,
            'course_description':description,
            'course_price':price,
            'quiz':q_list,
            'vid': new FormData(form)
        }
        $.ajax({
            url: 'add-course.html',
            type: 'POST',
            data: collectedData,
            datatype: 'json',
            success: function (response) {
                console.log(response);
            },
            error: function () {
                alert("We faced some difficulty in logging you in. Please try again later.")
            }
        });
    }