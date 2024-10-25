// Update the year in the footer
const date = new Date();
document.querySelector(".year").innerHTML = date.getFullYear();

// Fade out messages after 3 seconds
setTimeout(function () {
    $("#messages").fadeOut('slow');
}, 3000);
