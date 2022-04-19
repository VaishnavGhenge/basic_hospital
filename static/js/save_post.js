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
            }
            else {
                console.log('error');
                $('#save-error-message').html(message.msg);
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
                $('#edit-error' + id).slideUp();
                $('#edit-success' + id).slideDown();
            }
            else {
                console.log('error');
                $('#edit-error-message' + id).html(message.msg);
                $('#edit-success' + id).slideUp();
                $('#edit-error' + id).slideDown();
            }
        });
    });

    $('form.appointment-form').submit(function (e) {
        e.preventDefault();

        var data = $(this).serialize();
        var action = $(this).attr('action');

        console.log(data);

        $.ajax({
            type: "POST",
            url: action,
            data: data,
            timeout: 40000
        }).done(function (message) {
            if (message.status == 'success') {
                

                $('#confirm-name').text(message.name);
                $('#confirm-date').text(message.date);
                $('#confirm-sttime').text(message.sttime);
                $('#confirm-entime').text(message.entime);

                $('#appointment-error').slideUp();
                $('#confirm-btn').html('<i class="fa-solid fa-file-check"></i> Done');
                $('#confirm-btn').attr('type', 'button');
                $('#confirm-btn').attr('data-bs-dismiss', 'modal');
                $('#appointment-success').slideDown();
            }
            else {
                console.log('error');
                $('#appointment-error-message').html(message.msg);
                $('#appointment-success').slideUp();
                $('#appointment-error').slideDown();
            }
        });
    });

})(jQuery);