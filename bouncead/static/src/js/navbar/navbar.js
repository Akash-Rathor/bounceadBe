// navbar.js
document.addEventListener('DOMContentLoaded', function () {
    var menuToggle = document.getElementById('menuToggle');
    var navbarCta = document.getElementById('navbar-cta');

    if (menuToggle && navbarCta) {
        menuToggle.addEventListener('click', function () {
            var ariaExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
            menuToggle.setAttribute('aria-expanded', !ariaExpanded);
            navbarCta.classList.toggle('hidden');
            signup_login_btn.style.display = 'none';
        });
    }
});



document.addEventListener('DOMContentLoaded', function () {
    var signup_login_btn = document.getElementById('signup_login_btn');
    
    if (signup_login_btn) { // Check if the anchor element exists
        signup_login_btn.addEventListener('click', function (event) {
            event.preventDefault(); // Prevent the default anchor tag behavior (navigation)

            // Hide the button after clicking
            signup_login_btn.style.display = 'none';
        });
    }
});

