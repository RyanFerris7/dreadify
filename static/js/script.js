// Trigger modal for first time visitor
if (!localStorage.getItem('modalShown')) {
    var myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'));
    myModal.show();
    localStorage.setItem('modalShown', true);
}