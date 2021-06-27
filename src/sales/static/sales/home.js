console.log('Script from Django.');

const reportButton = document.getElementById('report-btn');
const graphImage = document.getElementById('graph-img');
const reportModalBody = document.getElementById('report-modal');
const reportForm = document.getElementById('report-form');
const reportAlert = document.getElementById('report-alert');

const reportName = document.getElementById('id_name');
const reportRemarks = document.getElementById('id_remarks');
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;


const handleAlerts = (type, message) => {
  reportAlert.innerHTML = `
    <div class="alert alert-${type}" role="alert">
      ${message}
    </div>
  `
}


if (graphImage) {
  reportButton.classList.remove('d-none');
}


reportButton.addEventListener('click', function() {
  reportModalBody.prepend(graphImage);

  reportForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrf);
    formData.append('name', reportName.value);
    formData.append('remarks', reportRemarks.value);
    formData.append('image', graphImage.src);

    $.ajax({
      type: 'POST',
      url: '/reports/save/',
      data: formData,
      success: function(response) { handleAlerts('success', response.msg); },
      error: function(error) { handleAlerts('danger', response.msg); },
      processData: false,
      contentType: false,
    });
  })
});
