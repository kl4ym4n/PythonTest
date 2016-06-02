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
    $("body").on('click','.delete-link-button',function()
    {

        var linkID = $(this).attr('id');
        // alert(linkID);
        $("#confirmDialog").modal('show');
        $("#deleteButton").click(function()
        {
            $.ajax({
                type: 'POST',
                data: {'linkid': linkID},
                url: 'http://33.33.33.10:8000/polls/deleteLink/' + linkID + '/',

                success: function (data) {
                    alert("Delete link " + linkID);
                    window.location.href = 'http://33.33.33.10:8000/polls/allLinks/'
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
