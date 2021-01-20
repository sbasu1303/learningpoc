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
    function login(){
        var email = document.getElementById("user_login").value;
        var password = document.getElementById("user_pass").value;
        console.log(document);
        var collectedData = {
            'csrfmiddlewaretoken': getCookie('csrftoken'),
            'username' : email,
            'password' : password,
        }
        $.ajax({
            url: '/login.html',
            type: 'POST',
            data: collectedData,
            datatype: 'json',
            success: function (response) {
                if (response.includes('Sorry account not found or password is invalid')){
                     alert(response);
                }
                else {
                    document.open();
                    document.write(response);
                    window.history.pushState('data', 'Title', "index.html");
                    document.close();
                }
            },
            error: function () {
                alert("We faced some difficulty in logging you in. Please try again later.")
            }
        });
    }