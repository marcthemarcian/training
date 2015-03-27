$(document).ready(function(){
    $('input[type="text"],input[type="password"],input[type="email"]').prop('required', true);

    var setCSRFToken = function(xhr) {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            if (cookies[i].indexOf('csrftoken') == 0) {
                xhr.setRequestHeader('X-CSRFToken', cookies[i].split('=')[1]);
                break;
            }
        }
    }

    $('#login').on('submit', function(e){
        e.preventDefault();
        
        $.ajax({
            type: 'POST',
            url:  verifyLoginURL,
            data: {
                'username': $('#id_username').val(),
                'password': $('#id_password').val()
            },
            beforeSend: setCSRFToken,
            success: function(response) {
                var data = JSON.parse(response);

                if (data['success'] == true) {
                    window.location.reload();
                } else {
                    window.location = loginURL;
                }
            },
            error: function(response, e) {
                alert(response.responseText)
            }
        });
    });

    $('#signup').on('submit', function(e){
        e.preventDefault();

        $.ajax({
            type: 'POST',
            url:  verifySignUpURL,
            data: {
                'first_name': $('#id_first_name').val(),
                'last_name': $('#id_last_name').val(),
                'email': $('#id_email').val(),
                'username': $('#signup #id_username').val(),
                'password1': $('#id_password1').val(),
                'password2': $('#id_password2').val()
            },
            beforeSend: setCSRFToken,
            success: function(response) {
                var data = JSON.parse(response);

                if (data['success'] == true) {
                    window.location.reload();
                } else {
                    var s = "";
                    for (key in data['error']) {
                        s += data['error'][key][0] + '<br>'
                    }

                    $('#sign-up-container > .error-message').remove();
                    $('#sign-up-container').append('<div class="error-message">'+s+'</div>');
                }
            },
            error: function(response, e) {
                alert(response.responseText)
            }
        });
    });
});