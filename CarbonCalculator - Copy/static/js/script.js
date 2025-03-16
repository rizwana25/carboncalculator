//script.js
function loadTemplate(templatePath, containerId) {
  fetch(templatePath)
    .then(response => response.text())
    .then(data => {
      document.getElementById(containerId).innerHTML = data;
      addFormEventListeners();
    });
}

function addFormEventListeners() {
  document.getElementById('loginForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    // Handle login logic here
    alert(`Logged in with email: ${email}`);
    window.location.href = 'templates/details.html'; // Redirect to details page
  });

  document.getElementById('signupForm')?.addEventListener('submit', function(event) {
    event.preventDefault();
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    // Handle signup logic here
    alert(`Signed up with email: ${email}`);
    window.location.href = 'templates/details.html'; // Redirect to details page
  });

  document.getElementById('showSignup')?.addEventListener('click', function(event) {
    event.preventDefault();
    loadTemplate('templates/signup.html', 'templateContainer');
  });

  document.getElementById('showLogin')?.addEventListener('click', function(event) {
    event.preventDefault();
    loadTemplate('templates/login.html', 'templateContainer');
  });
}

document.addEventListener('DOMContentLoaded', function() {
  loadTemplate('templates/login.html', 'templateContainer'); // Load login template by default
});

