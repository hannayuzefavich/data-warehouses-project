from faker import Faker
from faker.providers import DynamicProvider
from random import randint
import threading
import concurrent.futures
import json
import time
import os
from multiprocessing import Pool
import csv

fake = Faker('pl_PL')

OFFICE_NUMBER = 5
REAL_ESTATE_NUMBER = 5
EMPLOYEES_NUMBER = 5

start_time = time.time()
lock = threading.Lock()

def fakeOffice(n):
    fake2 = Faker()
    data = []
    print(os.getpid())
    for i in range(1, n):
        temp = {}
        temp['pk']= i
        temp['address'] = fake2.address()  
        data.append(temp)
    return data
        #with lock:
           # data.append(temp)
    
        
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


def generateMultithreaded(thread_count):
    with concurrent.futures.ProcessPoolExecutor(max_workers=thread_count) as executor:
        results = [executor.submit(fakeOffice, 10000) for _ in range(thread_count)]
        
        all_data = []
        for r in results:
            all_data.extend(r.result())
    return all_data

def fakeAddress(n):
    data = []
    print(os.getpid())
    for i in range(1, n):
        temp = {}
        temp['city'] = fake.city()
        temp['neighbourhood'] = fake.city_suffix()  
        temp['street '] = fake.street_name()  
        temp['house_number '] = fake.building_number()  
        temp['apartment_number '] = fake.random_int(min=1, max=50)
        temp['postal_code'] = fake.postcode()  
        data.append(temp)
    return data

def main():
    #results = generateMultithreaded(5)
    results = fakeAddress(50000)
    keys = results[0].keys()
    with open('results.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writerows(results)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"time: {elapsed_time}")

if __name__ == "__main__":
    main()