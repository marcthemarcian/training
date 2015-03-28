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

    $('#login-sattempt').on('submit', function(e){
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
                console.log(data);
                if (data['success'] == true) {
                    window.location.reload();
                } else {
                    alert("Nope.");
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

    $('#post-form').on('submit', function(e){
        e.preventDefault();

        if ($('#id_text').val().trim() == "") {
            alert("Please write something.");
            $('#id_text').val("");
            return;
        }

        $.ajax({
            type: 'POST',
            url:  postStatusURL,
            data: {
                'text': $('#id_text').val()
            },
            beforeSend: setCSRFToken,
            success: function(response) {
                $('#posts').prepend(response);
                $('#posts > div:nth-child(1)').hide().fadeIn();
                $('#id_text').val("");
            },
            error: function(response, e) {
                alert(response.responseText)
            }
        });
    });

    $('#posts').on('click', '.removePost', function(e){

        e.preventDefault();

        choice = prompt("Are you sure you want to delete this post? (y/n)");
        
        if (choice.toLowerCase() == "yes" || choice.toLowerCase() == "y") {
            $.ajax({
                type: 'POST',
                url:  removePostURL,
                data: {
                    'post-id': $(this).attr('id')
                },
                beforeSend: setCSRFToken,
                success: function(response) {
                    var data = JSON.parse(response);
                    if (data['success'] == true) {
                        $("#container_"+data['post-id']).fadeOut();
                    }
                },
                error: function(response, e) {
                    alert(response.responseText)
                }
            });
            }
    });
});