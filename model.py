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
def query1(client):
    pass


def query2(client):
    pass


def query3(client):
    pass
    

def query4(client):
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
