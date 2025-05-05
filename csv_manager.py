import csv
import os



import csv
import os

def read_csv():
    ''' 
    Reads the 'data.csv' file and returns its content as a list of dictionaries.

    '''
    if not os.path.isfile('data.csv'):
        with open('data.csv', mode='w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'tipo', 'monto'])
            writer.writeheader() 
    with open('data.csv', mode='r', encoding='utf-8') as f:
        lector = csv.DictReader(f)  
        return list(lector) 


def write_csv(data):
    '''
    Writes a list of dictionaries to 'data.csv', overwriting existing content (keys: id, tipo, and monto)

    '''
    if not data:
        return 
    with open('data.csv', mode='w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'tipo', 'monto']) 
        writer.writeheader() 
        writer.writerows(data)
