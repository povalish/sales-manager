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



def get_chart(chart_type, data, **kwargs):
  plt.switch_backend('AGG')
  fig = plt.figure(figsize=(10, 4))

  if chart_type == '#1':
    # plt.bar(
    #   data['transaction_id'],
    #   data['price'],
    # )
    sns.barplot(
      x='transaction_id',
      y='price',
      data=data,
    )
  elif chart_type == '#2':
    labels = kwargs.get('label')
    plt.pie(
      data=data,
      x='price',
      labels=labels
    )
  elif chart_type == '#3':
    plt.plot(
      data['transaction_id'],
      data['price'],
      color='red',
      marker='o'
    )
  else:
    print('Can not find required chart.')

  plt.tight_layout()
  chart = get_graph()
  return chart