from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.dateparse import parse_date


from xhtml2pdf import pisa
import csv

from profiles.models import Profile
from sales.models import Sale, Position, CSV
from products.models import Product
from customers.models import Customer

from .utils import get_report_image
from .models import Report
from .forms import ReportForm
 


class ReportListView(ListView):
  model = Report
  template_name = 'reports/main.html'


class ReportDetailView(DetailView):
  model = Report
  template_name = 'reports/detail.html'


class UploadTemplateView(TemplateView):
  template_name = 'reports/from_file.html'


def csv_upload_view(request):
  if request.method == 'POST':
    csv_filename = request.FILES.get('file').name
    csv_file = request.FILES.get('file')
    csv_object, created = CSV.objects.get_or_create(
      file_name=csv_filename,
      csv_file=csv_file
    )

    if created:
      with open(csv_object.csv_file.path, 'r') as f:
        reader = csv.reader(f)
        reader.__next__()

        for row in reader:
          data = "".join(row)
          data = data.split(';')
          data.pop()

          transaction_id = data[1]
          product = data[2]
          quantity = int(data[3])
          customer = data[4]
          date = parse_date(date[5])

          try:
            product_object = Product.objects.get(name__iexact=product)
          except Product.DoesNotExist:
            product_object = None

          if product_object is not None:
            customer_object, _ = Customer.objects.get_or_create(name=customer)
            salesman_object = Profile.objects.get(user=request.user)
            position_object = Position.objects.create(
              product=product_object,
              quantity=quantity,
              created=date,
            )
            sale_object, _ = Sale.objects.get_or_create(
              transaction_id=transaction_id,
              customer=customer_object,
              salesman=salesman_object,
            )
            sale_object.positions.add(position_object)
            sale_object.save()

        return JsonResponse({'message': 'Create new entries'})
    else:
      return JsonResponse({'message': 'This file was already processed.'})    
  return HttpResponse()


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
