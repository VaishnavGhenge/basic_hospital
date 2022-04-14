!(function ($) {
    "use strict";

    $('form.new-post').submit(function (e) {
        e.preventDefault();
        var data = new FormData(this);
        var action = $(this).attr('action');
        var val = e.originalEvent.submitter.name;

        $.ajax({
            type: "POST",
            url: action + val + '/',
            data: data,
            timeout: 40000,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (message) {
            if (message.status == 'success') {
                console.log('success');
                $('#save-error').slideUp();
                $('#save-success').slideDown();
            }
            else {
                console.log('error');
                $('#save-error-message').html(message.msg);
                $('#save-success').slideUp();
                $('#save-error').slideDown();
            }
        });
    });

    $('form.form-edit').submit(function (e) {
        e.preventDefault();
        var data = new FormData(this);
        var action = $(this).attr('action');
        var val = e.originalEvent.submitter.name;
        var id = $(this).attr('id');

        $.ajax({
            type: "POST",
            url: action + val + '/' + id + '/',
            data: data,
            timeout: 40000,
            cache: false,
            contentType: false,
            processData: false
        }).done(function (message) {
            if (message.status == 'success') {
                console.log('success');
                $('#edit-error'+id).slideUp();
                $('#edit-success'+id).slideDown();
            }
            else {
                console.log('error');
                $('#edit-error-message'+id).html(message.msg);
                $('#edit-success'+id).slideUp();
                $('#edit-error'+id).slideDown();
            }
        });
    });

})(jQuery);