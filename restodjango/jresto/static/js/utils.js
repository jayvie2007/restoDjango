// scripts used for alert message in register/login error

const dismissableAlert = document.getElementById('dismissableAlert');
const dismissButton = document.getElementById('dismissButton');

// Add a click event listener to the SVG close button
dismissButton.addEventListener('click', () => {
    // Hide the alert by setting its display style to 'none'
    dismissableAlert.style.display = 'none';
});