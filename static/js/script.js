// Return function for when users choose not to delete something 
function denyDelete() {
    window.history.back();
}
// Triggers a content warning modal for first time visitors 
if (!localStorage.getItem('modalShown')) {
    var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    myModal.show();
    localStorage.setItem('modalShown', true);
}
// Auto resizes the footer if the content doesn't fill a page 
window.addEventListener('load', function() {
    positionFooter();
});

window.addEventListener('resize', function() {
    positionFooter();
});

function positionFooter() {
    var footer = document.querySelector('.footer');
    var windowHeight = window.innerHeight;
    var bodyHeight = document.body.clientHeight;

    if (bodyHeight < windowHeight) {
        footer.style.position = 'fixed';
        footer.style.bottom = '0';
        footer.style.width = '100%';
    } else {
        footer.style.position = 'static';
    }
}
