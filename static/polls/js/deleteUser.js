/**
 * Created by klayman on 6/3/16.
 */
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


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
    $(".delete-user-button").click(function()
    {
        var userID = $(this).attr('id');
        $("#confirmDialog").modal('show');
        $("#deleteButton").click(function()
        {
            $.ajax({
                type: 'POST',
                // data: {'userid': userID},
                url: '/polls/deleteUser/' + userID + '/',

                success: function (data) {
                    alert("Delete user " + userID);
                    window.location.href = '/polls/usersList/'
                },
                error: function (xhr, desc, err) {
                    console.log(xhr);
                    console.log("Details: " + desc + "\nError:" + err);
                }
            }); // end ajax call
            $("#confirmDialog").modal('hide');
        });
    });
});