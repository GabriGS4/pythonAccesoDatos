import pandas as pd
import json
from Customer import *


def saveCustomer(json_filename, oC):
    with open(json_filename, 'r') as json_file:
        customer_data = json.load(json_file)

    # Obtener el posFile del último cliente
    if customer_data:
        last_posFile = int(customer_data[-1]['pos'])
    else:
        last_posFile = -1

    # Asignar un nuevo posFile al cliente actual
    oC.posFile = str(last_posFile + 1)

    # Agregar el nuevo cliente al archivo JSON
    customer_data.append({
        "Id": oC.ID,
        "Name": oC.name,
        "Bill Address": oC.bill,
        "email": oC.email,
        "phone": oC.phone,
        "pos": oC.posFile,
        "erased": "0"  # Por defecto, el nuevo cliente no está borrado
    })

    # Guardar los datos actualizados en el archivo JSON
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


def modifyCustomer(json_filename, posFile, new_customer):
    # Abrir el archivo JSON y cargar los datos existentes
    with open(json_filename, 'r') as json_file:
        customer_data = json.load(json_file)

    # Buscar el cliente en la lista por su posición
    for customer_json in customer_data:
        if customer_json['pos'] == str(posFile):
            # Actualizar la información del cliente con los datos del nuevo cliente
            customer_json['Name'] = new_customer.name
            customer_json['Bill Address'] = new_customer.bill
            customer_json['phone'] = new_customer.phone
            customer_json['email'] = new_customer.email

            # Puedes agregar más campos según sea necesario

            break  # Terminar el bucle después de encontrar y actualizar el cliente

    # Guardar los datos actualizados de nuevo en el archivo JSON
    with open(json_filename, 'w') as json_file:
        json.dump(customer_data, json_file, indent=2)

    pass

def readCustomer(f, lC):
    df = pd.read_json(f)
    for custo in df.values.tolist():
        if custo[6] == 0:
            lC.append(Customer(custo[0], custo[1], custo[2], custo[3], custo[4], custo[5]))
