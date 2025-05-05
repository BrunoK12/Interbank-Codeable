# BRUNO DIAZ ARRAASCUE 71099598
# brunodiaz1612@gmail.com

import csv_manager  # lector y sobrescritor de data.csv (modulo auxiliar)
import click  # interfaz para apps de lineas de comando


# GRUPO PRINCIPAL DE COMANDOS
@click.group()
def cli_principal():
    pass

# COMANDOS SECUNDARIOS 
# @cli_principal.command() es un decorador que registra función como comando en cli_principal
@cli_principal.command()
def info():
    '''
    Display the main report from data.csv.
    '''

    transactions = csv_manager.read_csv()
    if not transactions:
        click.echo("No hay transacciones para procesar.")
        return None
    
    # Inicialización de valores
    balance = 0.0
    transaction_counts = {'Crédito': 0, 'Débito': 0} 
    max_transaction = None 

    for i in transactions:
        tipo = i['tipo']
        monto = float(i['monto'])
        if tipo == 'Crédito':
            balance += monto
            transaction_counts['Crédito'] += 1
        elif tipo == 'Débito':
            balance -= monto
            transaction_counts['Débito'] += 1
        
        if (max_transaction is None) or (monto > float(max_transaction['monto'])):
            max_transaction = i

    click.echo("REPORTE")
    click.echo("---------------------------------------------")
    click.echo(f"Balance Final: {balance:.2f}")
    click.echo(f"Transacción de Mayor Monto: ID {max_transaction['id']} - {float(max_transaction['monto']):.2f}")
    click.echo(f"Conteo de Transacciones: Crédito: {transaction_counts['Crédito']} Débito: {transaction_counts['Débito']}")
    return None




@cli_principal.command()
@click.option('--tipo', required=True, help='Tipo de Transacción')
@click.option('--monto', required=True, help='Monto de Transacción')
@click.pass_context
def new(ctx, tipo, monto):
    '''
    Creates a new register for data.csv
    '''

    if not tipo or not monto:
        ctx.fail('El tipo y monto son requeridos')
    else:
        if tipo == 'Crédito' or tipo == 'Débito':
            try:
                monto = float(monto)  
                if monto > 0:
                    data = csv_manager.read_csv()
                    new_id = len(data) + 1
                    new_data = {
                        'id': new_id,
                        'tipo': tipo,
                        'monto': monto
                    }
                    data.append(new_data)
                    csv_manager.write_csv(data)
                    print(f"Se ha agregado la transacción {new_id} con el monto {monto} de tipo {tipo}")
                else:
                    print("El monto debe ser mayor a 0")
            except ValueError:
                print("El monto debe ser un número")
        else:
            ctx.fail('El tipo solo puede ser Crédito o Débito')
    return None



@cli_principal.command()
def view():
    '''
    Display the last 10 entries from data.csv.
    '''

    transaction = csv_manager.read_csv()
    last_10 = transaction[-10:] 
    for i in last_10:
        print(f"{i['id']} - {i['tipo']} - {i['monto']}")
    return None




@cli_principal.command()
@click.argument('id',type=int)
def delete(id):
    '''
    Delete a user from the data.csv file by their ID 
    '''

    data = csv_manager.read_csv()
    n = next((x for x in data if int(x['id']) == id), None)
    if n is None:
        print(f"User with id {id} not found")
    else:
        data.remove(n)
        csv_manager.write_csv(data)
        print(f"User with id {id} deleted successfully")
    
    return None




if __name__ == '__main__':
    cli_principal()
