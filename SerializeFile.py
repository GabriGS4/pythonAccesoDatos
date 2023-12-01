import pickle
import pandas as pd
import json
from Customer import *


def saveCustomer(json_filename, oC):
    with open(json_filename, 'r') as json_file:
        customer_data = json.load(json_file)

    customer_data.append({
        "Id": oC.ID,
        "Name": oC.name,
        "Bill Address": oC.bill,
        "email": oC.email,
        "phone": oC.phone,
        "pos": oC.posFile,
        "erased": "0"  # Por defecto, el nuevo cliente no está borrado
    })

    with open(json_filename, 'w') as json_file:
        json.dump(customer_data, json_file, indent=2)

    pass

def deleteCustomer(json_filename, posFile):
    with open(json_filename, 'r') as json_file:
        customer_data = json.load(json_file)

    for customer_json in customer_data:
        if str(customer_json['pos']) == str(posFile):
            customer_json['erased'] = "1"

    with open(json_filename, 'w') as json_file:
        json.dump(customer_data, json_file)
    pass


def modifyCustomer():

    pass

def readCustomer(f, lC):
    df = pd.read_json(f)
    for custo in df.values.tolist():
        if custo[6] == 0:
            lC.append(Customer(custo[0], custo[1], custo[2], custo[3], custo[4], custo[5]))
