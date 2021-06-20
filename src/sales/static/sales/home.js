console.log('Script from Django.');

const reportButton = document.getElementById('report-btn');
const graphImage = document.getElementById('graph-img');


if (graphImage) {
  reportButton.classList.remove('d-none');
}