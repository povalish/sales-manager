from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from.forms import SalesSearchForm


def home_view(request):
  form = SalesSearchForm(request.POST or None)
  context = {
    'form': form,
  }
  return render(request, 'sales/home.html', context)


class SalesListView(ListView):
  model = Sale
  template_name = 'sales/main.html'
  context_object_name = 'sales_list'
  


class SaleDetailView(DetailView):
  model = Sale
  template_name = 'sales/detail.html'



# Another approach

def sale_list_view(request):
  qs = Sale.objects.all()
  return render(request, 'sales/main.html', { 'object_list': qs })


def sale_detail_view(request, **kwargs):
  pk = kwargs.get('pk')
  object = Sale.objects.get(pk=pk)
  return render(request, 'sales/detail.html', { 'object': object })
