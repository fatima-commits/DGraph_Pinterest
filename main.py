#!/usr/bin/env python3
import os
import pydgraph
import model

DGRAPH_URI = os.getenv('DGRAPH_URI', 'localhost:9080')

def print_menu():
    mm_options = {
        1: "Crear esquema",
        2: "Cargar datos desde CSV",
        3: "Query por texto indexado",
        4: "Query por campo numérico",
        5: "Query de grafo (2+ tipos)",
        6: "Query con relación inversa",
        7: "Query con orden y paginación",
        8: "Query con count()",
        9: "Eliminar por condición",
        10: "Eliminar todo",
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
            # Query: texto indexado
            value = input("Valor de texto a buscar: ")
            model.query_text_index(client, value)

        elif option == 4:
            # Query: campo numérico
            min_v = input("Ingrese el valor mínimo: ")
            max_v = input("Ingrese el valor máximo: ")
            model.query_numeric_index(client, min_v, max_v)

        elif option == 5:
            # Query: grafo (2+ tipos)
            # Agregar parametros si llegan a ser necesarios
            model.query_graph_data(client)

        elif option == 6:
            # Query: relación inversa
            # Agregar parametros si llegan a ser necesarios
            model.query_reverse_relation(client)

        elif option == 7:
            # Query: orden y paginación
            # Agregar parametros si llegan a ser necesarios (tipo de orden y offset)
            model.query_order_and_pagination(client)

        elif option == 8:
            # Query: uso de count()
            model.query_count_example(client)

        elif option == 9:
            # Eliminar por condición
            # Agregar parametros si llegan a ser necesarios (valor de la condicion)
            model.delete_by_condition(client)

        elif option == 10:
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