# Dgraph Lab 3 - ITESO BDNR

### 1. Crear un esquema que:
- Contenga **al menos 4 tipos de nodos**.
- Tenga un **campo de texto indexado** (`@index(term)`).
- Tenga un **campo numérico indexado** (`@index(int)`).
- Incluya un **campo geo** (`location: geo .`).
- Genere **una relación con dirección inversa** (`@reverse`).

### 2. Operaciones del cliente:
- Cargar datos desde CSV.
- Ejecutar al menos **4 tipos de queries**, incluyendo:
  - Texto indexado.
  - Numérico indexado.
  - Relaciones entre 2+ tipos.
  - Relación inversa.
  - Orden y paginación.
  - Count.
- Eliminar datos:
  - Por condición.
  - Borrar todo el grafo.

### Requisitos
### Setup de un ambiente virtual de python virtual con pydgraph instalado
```
# Si no tienes pip instalado
sudo apt update
sudo apt install python3-pip

# Instalar y activar el virtual env (Linux/MacOS)
python3 -m pip install virtualenv
python3 -m venv ./venv
source ./venv/bin/activate

# Instalar y activar el virtual env (Windows)
python3 -m pip install virtualenv
python3 -m venv ./venv
.\venv\Scripts\Activate.ps1

# Instalar los requerimientos de python al project
pip install -r requirements.txt
```

### Para cargar los datos
Asegurate de tener una instancia de dgraph corriendo
i.e.:
```
docker run --name dgraph -d -p 8080:8080 -p 9080:9080 dgraph/standalone
```
Correr main.py
i.e.:
```
python3 main.py
```

