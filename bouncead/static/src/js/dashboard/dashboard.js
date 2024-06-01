
  document.addEventListener("DOMContentLoaded", function() {
    // Get the job posts form
    var jobPostsForm = document.getElementById("job_posts_form");

    // Get the candidates form
    var candidatesForm = document.getElementById("candidates_form");

    // Get the analytics form
    var analyticsForm = document.getElementById("analytics_form");

    // Add click event listener to job posts form
    jobPostsForm.addEventListener("click", function() {
      jobPostsForm.submit(); // Submit the form
    });

    // Add click event listener to candidates form
    candidatesForm.addEventListener("click", function() {
      candidatesForm.submit(); // Submit the form
    });

    // Add click event listener to analytics form
    analyticsForm.addEventListener("click", function() {
      analyticsForm.submit(); // Submit the form
    });
  });
