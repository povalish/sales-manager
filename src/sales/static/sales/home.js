console.log('Script from Django.');

const reportButton = document.getElementById('report-btn');
const graphImage = document.getElementById('graph-img');
const reportModalBody = document.getElementById('report-modal');

if (graphImage) {
  reportButton.classList.remove('d-none');
}


reportButton.addEventListener('click', function() {
  reportModalBody.prepend(graphImage);
});
