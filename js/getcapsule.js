$(function () {
  // Function to populate capsules on page load
  function populateCapsules() {
    $.ajax({
      url: 'http://localhost:5000/api/v1/capsules/',
      success: function (data) {
        if (data.length > 0) {
          // If there are capsules, hide the "No opened capsules" message
          $('#noCapsulesMessage').hide();

          // Populate capsules in the capsulesContainer
          var capsulesContainer = $('#capsulesContainer');
          capsulesContainer.empty(); // Clear previous capsules

          // Iterate over each capsule in the data
          data.forEach(function (capsule) {
            // Create a div element for each capsule
            var capsuleDiv = $('<div class="capsule"></div>');

            // Add title to the capsuleDiv
            capsuleDiv.append('<h3>' + capsule.title + '</h3>');

            // Check if the image is not null, then add an image element
            if (capsule.image !== null) {
              capsuleDiv.append('<img src="' + capsule.image + '" alt="Capsule Image">');
            }

            // Add message to the capsuleDiv
            capsuleDiv.append('<p>' + capsule.message + '</p>');

            // Append the capsuleDiv to the capsulesContainer
            capsulesContainer.append(capsuleDiv);
          });
        } else {
          // If there are no capsules, show the "No opened capsules" message
          $('#noCapsulesMessage').show();
        }
      }
    });
  }

  // Call the function to populate capsules on page load
  populateCapsules();
});