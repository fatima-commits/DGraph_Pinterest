import csv
import pydgraph

# Crear el esquema
def create_schema(client):
    """
    - Crear un esquema que contenga al menos 4 tipos de nodos.
    - Incluir:
        * Un campo de texto indexado.
        * Un campo numérico indexado.
        * Un campo de tipo geo.
        * Al menos una relación con dirección inversa (@reverse).
    - Usa client.alter(pydgraph.Operation(schema=schema_string))
    """
    schema = """ ... """
    client.alter(pydgraph.Operation(schema=schema))
    pass

# Cargar Datos
def load_data(client):
    """
    - Cargar datos desde archivos CSV y crear nodos.
    - Crear relaciones entre nodos
    - Usar transacciones y mutations.
    - Ejemplo de estructura:
        txn = client.txn()
        txn.mutate(set_obj=lista_de_objetos)
        txn.commit()
    """
    pass

# Queries
def query_text_index(client, value):
    """Query que utilice el índice de texto."""
    pass


def query_numeric_index(client, min_value, max_value):
    """Query que utilice el índice numérico."""
    pass


def query_graph_data(client):
    """Query que involucre al menos 2 tipos de nodos relacionados."""
    pass
    

def query_reverse_relation(client):
    """Query que use una relación inversa (@reverse)."""
    pass


def query_order_and_pagination(client):
    """Query que ordene resultados y use paginación (first, offset)."""
    pass


def query_count_example(client):
    """Query que use la función count()."""
    pass


# Eliminaciones
def delete_by_condition(client):
    """Eliminar datos que cumplan una condición específica."""
    pass


def delete_all(client):
    """
    - Eliminar todo el contenido del grafo.
    - Usa client.alter(pydgraph.Operation(drop_all=True))
    """
    pass
