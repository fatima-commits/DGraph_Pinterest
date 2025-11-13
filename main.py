#!/usr/bin/env python3
import os
import pydgraph
import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        1: "Crear esquema",
        2: "Cargar datos desde CSV",
        3: "Query #1: Cambiar nombre",
        4: "Query #2: Cambiar nombre",
        5: "Query #3: Cambiar nombre",
        6: "Query #4: Cambiar nombre",
        7: "Eliminar por condición",
        8: "Eliminar todo",
        0: "Salir",
    }
    for key in mm_options.keys():
        print(key, "--", mm_options[key])

def create_client_stub():
    """Crea el stub de conexión gRPC con Dgraph."""
    return pydgraph.DgraphClientStub(DGRAPH_URI)


def create_client(client_stub):
    """Crea el cliente principal para interactuar con Dgraph."""
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    """Cierra la conexión con Dgraph."""
    client_stub.close()

def main():
    # Inicializar conexión con Dgraph
    client_stub = create_client_stub()
    client = create_client(client_stub)

    while True:
        print_menu()
        try:
            option = int(input('Seleccione una opción: '))
        except ValueError:
            print("Opción inválida, intente de nuevo.")
            continue

        if option == 1:
            # Crear esquema
            model.create_schema(client)

        elif option == 2:
            # Cargar datos desde CSV
            model.load_data(client)

        elif option == 3:
            # Query 1: Pedir input al usuario dependiendo de su modelado
            model.query1(client)

        elif option == 4:
            # Query 2: Pedir input al usuario dependiendo de su modelado
            model.query2(client)

        elif option == 5:
            # Query 3: Pedir input al usuario dependiendo de su modelado
            model.query3(client)

        elif option == 6:
            # Query 4: Pedir input al usuario dependiendo de su modelado
            model.query4(client)

        elif option == 7:
            # Eliminar por condición
            # Agregar parametros si llegan a ser necesarios (valor de la condicion)
            model.delete_by_condition(client)

        elif option == 8:
            # Eliminar todo el contenido del grafo
            confirm = input("¿Seguro que deseas eliminar TODO el grafo? (s/n): ")
            if confirm.lower() == "s":
                model.delete_all(client)
                print("Grafo eliminado completamente.")
            else:
                print("Operación cancelada.")

        elif option == 0:
            # Cerrar conexión y salir
            close_client_stub(client_stub)
            print("Conexión cerrada.")
            exit(0)

        else:
            print("Opción no válida, intenta nuevamente.")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error: {}'.format(e))