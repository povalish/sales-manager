from django.shortcuts import render
from django.views.generic import ListView, DetailView
import pandas as pd

from .models import Sale
from .forms import SalesSearchForm
from .utils import get_customer_by_id, get_salesman_by_id


def home_view(request):
  form = SalesSearchForm(request.POST or None)

  sales_dataframe = None
  sales_dataframe_html = None

  positions_dataframe = None
  positions_dataframe_html = None

  salesdf_with_positiondf = None

  main_dataframe = None
  main_dataframe_html = None


  if request.method == 'POST':
    date_from = request.POST.get('date_from')
    date_to = request.POST.get('date_to')
    chart_type = request.POST.get('chart_type')

    query_set = Sale.objects.filter(
      created__date__lte=date_to,
      created__date__gte=date_from
    )

    if len(query_set) > 0:
      sales_dataframe = pd.DataFrame(query_set.values())

      sales_dataframe['customer_id'] = sales_dataframe['customer_id'].apply(get_customer_by_id)
      sales_dataframe['salesman_id'] = sales_dataframe['salesman_id'].apply(get_salesman_by_id)
      sales_dataframe['created'] = sales_dataframe['created'].apply(lambda x: x.strftime('%d-%m-%y'))
      sales_dataframe['updated'] = sales_dataframe['updated'].apply(lambda x: x.strftime('%d-%m-%y'))

      sales_dataframe = sales_dataframe.rename({
        'customer_id': 'customer', 
        'salesman_id': 'salesman',
        'id': 'sales_id',
      }, axis=1)

      # sales_dataframe['sale_id'] = sales_dataframe['id']

      positions = []

      for sale in query_set:
        for position in sale.get_positions():
          position_object = {
            'position_id': position.id,
            'product': position.product.name,
            'quantity': position.quantity,
            'price': position.price,
            'sales_id': position.get_sale_id(),
          }
        positions.append(position_object)

      positions_dataframe = pd.DataFrame(positions)
      salesdf_with_positiondf = pd.merge(positions_dataframe, sales_dataframe, on='sales_id')
      main_dataframe = salesdf_with_positiondf.groupby('transaction_id', as_index=False)['price'].agg('sum')

      sales_dataframe_html = sales_dataframe.to_html()
      positions_dataframe_html = positions_dataframe.to_html()
      salesdf_with_positiondf_html = salesdf_with_positiondf.to_html()
      main_dataframe_html = main_dataframe.to_html()



  context = {
    'form': form,
    'sales_dataframe': sales_dataframe_html,
    'positions_dataframe': positions_dataframe_html,
    'salesdf_with_positiondf': salesdf_with_positiondf_html,
    'main_dataframe': main_dataframe_html,
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
