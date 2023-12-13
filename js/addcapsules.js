$(function () {  
    $('#capsule_form').submit(function (event) {
  
      var form_data = new FormData($('#capsule_form')[0]);

      $.ajax({
        url: 'http://orino.tech/api/v1/capsules/add',
        type: 'POST',
        data: form_data,
        processData: false,
        contentType: false,
        success: function (data) {
          $('#capsule_form')[0].reset();
        },
        error: function(xhr, status, error) {
          console.error("AJAX error:", status, error);
        }
      });
  
      event.preventDefault();
    });
  });