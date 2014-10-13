$(document).ready(function(){

    // using jQuery
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
    var csrftoken = getCookie('csrftoken');

    $('#login_form').on('submit', function(e){
        event.preventDefault();
        $.ajax({
            url: '/signin/',
            type: 'POST',
            dataType: 'text',
            data: $('#login_form').serialize(),
            success: function(msg){
                console.log(msg);
                window.location = msg;
            },
            headers: {'X-CSRFToken': csrftoken}
        });
    });
});
