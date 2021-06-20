import uuid, base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns

from customers.models import Customer
from profiles.models import Profile



def generate_code():
  return str(uuid.uuid4()).replace('-', '')[:12]



def get_salesman_by_id(id):
  return Profile.objects.get(id=id).user.username



def get_customer_by_id(id):
  return Customer.objects.get(id=id)



def get_graph():
  buffer = BytesIO()
  plt.savefig(buffer, format='png')
  buffer.seek(0)

  image_png = buffer.getvalue()
  graph = base64.b64encode(image_png)
  graph = graph.decode('utf-8')

  buffer.close()

  return graph


def get_key(res_by):
  key = None

  if res_by == '#1':
    key = 'transaction_id'
  if res_by == '#2':
    key = 'created'
  
  return key


def get_chart(chart_type, data, results_by, **kwargs):
  plt.switch_backend('AGG')
  fig = plt.figure(figsize=(10, 4))
  key = get_key(results_by)
  grouped_data = data.groupby(key, as_index=False)['total_price'].agg('sum')

  if chart_type == '#1':
    # plt.bar(
    #   grouped_data[key],
    #   grouped_data['total_price'],
    # )
    sns.barplot(
      x=key,
      y='total_price',
      data=grouped_data,
    )
  elif chart_type == '#2':
    plt.pie(
      data=grouped_data,
      x='total_price',
      labels=grouped_data[key].values
    )
  elif chart_type == '#3':
    plt.plot(
      grouped_data[key],
      grouped_data['total_price'],
      color='red',
      marker='o'
    )
  else:
    print('Can not find required chart.')

  plt.tight_layout()
  chart = get_graph()
  return chart