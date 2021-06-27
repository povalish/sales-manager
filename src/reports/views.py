from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

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


