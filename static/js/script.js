function showSuccessMessage() {
    var successMessage = document.querySelector('.success-message');
    successMessage.classList.add('show');
    setTimeout(function() {
        successMessage.classList.remove('show');
    }, 3000); // Hide after 3 seconds
}
