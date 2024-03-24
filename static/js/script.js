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
    var wrapper = document.querySelector('.wrapper');
    var footer = document.querySelector('.footer');
  
    var footerHeight = footer.offsetHeight;
    var wrapperHeight = wrapper.offsetHeight;
  
    if (wrapperHeight > window.innerHeight - footerHeight) {
      wrapper.style.height = 'auto';
      footer.style.position = 'static';
    } else {
      wrapper.style.height = '100vh';
      footer.style.position = 'fixed';
      footer.style.bottom = '0';
      footer.style.width = '100%';
    }
  }