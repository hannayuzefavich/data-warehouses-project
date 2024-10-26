from faker import Faker
from faker.providers import DynamicProvider
from random import randint
import threading
import concurrent.futures
import json
import time

fake = Faker()

OFFICE_NUMBER = 5
REAL_ESTATE_NUMBER = 5
EMPLOYEES_NUMBER = 5

start_time = time.time()
lock = threading.Lock()
data = []
def fakeOffice(n):
    for i in range(1, n):
        temp = {}
        temp['pk']= i
        temp['address'] = fake.address()  
        with lock:
            data.append(temp)
        
# data provider for generating fake positions for employees
employee_positions_provider = DynamicProvider(
     provider_name="employee_position",
     elements=["customer service", "finance", "head office manager", "operations manager", "marketing manage"],
)
fake.add_provider(employee_positions_provider)

def fakeEmployee(n):
    data = []
    for i in range(1, n):
        temp = {}
        temp['pk'] = i
        temp['fk_office'] = randint(1,OFFICE_NUMBER)
        temp['firstName'] = fake.first_name()
        temp['lastName'] = fake.last_name()
        temp['position'] = fake.employee_position()
        temp['employmentDate'] = fake.date()
        # temp['pesel'] = 
        data.append(temp)
    print(data)

# data provider for generating types of real estate
real_estate_type_provider = DynamicProvider(
     provider_name="real_estate_type",
     elements=["house", "apartment", "commercial office"],
)
fake.add_provider(real_estate_type_provider)

def fakeRealEstate(n):
    data = []
    for i in range(1, n):
        temp = {}
        temp['pk'] = i
        temp['address'] = fake.address()
        temp['type'] = fake.real_estate_type()
        temp['number_of_rooms'] = randint(1, 5)
        temp['area'] = randint(20, 80)
        temp['price'] = randint(1000, 5000)
        temp['owner'] = fake.name()
        data.append(temp)
    print(data)

pool = concurrent.futures.ThreadPoolExecutor(max_workers=5)

for i in range(5):
    pool.submit(fakeOffice(10000))
pool.shutdown(wait=True)
with open("results.json", "a") as f:
    json.dump(data, f, indent=0)
end_time = time.time()
elapsed_time = end_time - start_time

print(f"time: {elapsed_time}")
