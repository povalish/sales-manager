import uuid
from customers.models import Customer
from profiles.models import Profile



def generate_code():
  return str(uuid.uuid4()).replace('-', '')[:12]



def get_salesman_by_id(id):
  return Profile.objects.get(id=id).user.username


def get_customer_by_id(id):
  return Customer.objects.get(id=id)
