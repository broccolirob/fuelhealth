/**
 * Created by robert on 9/21/14.
 */
$(document).ready(function() {

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

function vote (article_id) {
    debugger;
    $.ajax({
        type: "POST",
        url: "/vote/",
        data: {"article": article_id},
        success: function() {
            $("#article-vote-" + article_id).replaceWith("<span class='glyphicon glyphicon-ok pull-right' style='color:orange;'></span>");
            $("#points-" + article_id).replaceWith("-");
        },
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
    return false;
}

$("a.vote").click(function() {
    var article_id = parseInt(this.id.split("-")[2]);
    return vote(article_id);
});

});