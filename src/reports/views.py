from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from profiles.models import Profile

from .utils import get_report_image
from .models import Report
from .forms import ReportForm
 


class ReportListView(ListView):
  model = Report
  template_name = 'reports/main.html'


class ReportDetailView(DetailView):
  model = Report
  template_name = 'reports/detail.html'


def create_report_view(request):
  form = ReportForm(request.POST or None)

  if request.is_ajax():
    image_source = request.POST.get('image')
    image = get_report_image(image_source)
    author = Profile.objects.get(user=request.user)

    if form.is_valid():
      instance = form.save(commit=False)
      instance.image = image
      instance.author = author
      instance.save()

    return JsonResponse({'msg': 'everything is OK.'})
  return JsonResponse({'msg': 'something went wrong.'})


def render_pdf_view(request, pk):
    template_path = 'reports/pdf.html'
    obj = get_object_or_404(Report, pk=pk)
    context = {
      'pdfTitle': 'PDF Document',
      'object': obj,
    }

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # id downloading file
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if displaying file
    response['Content-Disposition'] = 'filename="report.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
