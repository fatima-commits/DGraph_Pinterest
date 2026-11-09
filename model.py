import csv
import json
import pydgraph

# Crear el esquema
def create_schema(client):    
    schema= """
        username: string @index(exact, term) @upsert .
        follower_count: int @index(int) .
        age: int @index(int) .
        user_location: geo @index(geo) .

        image_url: string @index(exact) .
        like_count: int @index(int) .
        comment_count: int .
        views: int .

        tag: string @index(exact, term) @upsert .

        board_name: string @index(exact, term) @upsert .

        SAVES: [uid] @reverse @count .
        COMMENTS: [uid] @reverse @count .
        LIKES: [uid] @reverse @count .
        CREATES: [uid] @reverse .
        FOLLOWS: [uid] @reverse @count .
        SHARES: [uid] @reverse .
        MADE_OF: [uid] @reverse .
        CONTAINS: [uid] @reverse .

        type User {
            username
            follower_count
            age
            user_location
            SAVES
            COMMENTS
            LIKES
            CREATES
            FOLLOWS
            SHARES
        }

        type Pin {
            image_url
            like_count
            comment_count
            views
            MADE_OF
            CONTAINS
        }

        type Board {
            board_name
            like_count
        }

        type Tag {
            tag
        }
    """
    client.alter(pydgraph.Operation(schema=schema))
    print("Schema creado correctamente")

#HELPERS
def parse_location(location_str):
    # Recibe "lon,lat" y regresa GeoJSON Point
    partes = location_str.split(",")
    lon = float(partes[0])
    lat = float(partes[1])
    return {"type": "Point", "coordinates": [lon, lat]}

def ask_int(prompt, default):
    #Pide un entero al usuario; si lo deja vacío o es inválido usa el default.
    #HECHO CON IA
    value = input(prompt + " [" + str(default) + "]: ").strip()
    if value == "":
        return str(default)
    try:
        return str(int(value))
    except ValueError:
        print("Valor inválido, se usa", default)
        return str(default)

# Cargar Datos
def load_data(client):
    #PARA EVITAR DUPLICADOS. RECOMENDACION POR IA
    check = client.txn(read_only=True).query("{ q(func: type(User), first: 1) { uid } }")
    if json.loads(check.json)["q"]:
        print("Ya existen datos cargados. Usa 'Eliminar todo' antes de volver a cargar.")
        return
    
    user_uids = load_users(client)
    pin_uids = load_pins(client)
    board_uids = load_boards(client)
    tag_uids = load_tags(client)
    create_edges(client, user_uids, pin_uids, board_uids, tag_uids)

#usuarios
def load_users(client):
    txn = client.txn()
    try:
        users = []
        with open("csv/users.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                users.append({
                    "uid": "_:" + row["user_id"],
                    "dgraph.type": "User",
                    "username": row["username"],
                    "follower_count": int(row["follower_count"]),
                    "age": int(row["age"]),
                    "user_location": parse_location(row["longitude"] + "," + row["latitude"]),
                })

        res = txn.mutate(set_obj=users)
        txn.commit()
        print(f"Usuarios cargados: {len(users)}")
        return res.uids
    finally:
        txn.discard()

#pines
def load_pins(client):
    txn = client.txn()
    try:
        pins = []
        with open("csv/pins.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pins.append({
                    "uid": "_:" + row["pin_id"],
                    "dgraph.type": "Pin",
                    "image_url": row["image_url"],
                    "like_count": int(row["like_count"]),
                    "comment_count": int(row["comment_count"]),
                    "views": int(row["views"]),
                })

        res = txn.mutate(set_obj=pins)
        txn.commit()
        print(f"Pines cargados: {len(pins)}")
        return res.uids
    finally:
        txn.discard()

#boards
def load_boards(client):
    txn = client.txn()
    try:
        boards = []
        with open("csv/boards.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                boards.append({
                    "uid": "_:" + row["board_id"],
                    "dgraph.type": "Board",
                    "board_name": row["board_name"],
                    "like_count": int(row["like_count"]),
                })

        res = txn.mutate(set_obj=boards)
        txn.commit()
        print(f"Tableros cargados: {len(boards)}")
        return res.uids
    finally:
        txn.discard()

#tags
def load_tags(client):
    txn = client.txn()
    try:
        tags = []
        with open("csv/tags.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                tags.append({
                    "uid": "_:" + row["tag_id"],
                    "dgraph.type": "Tag",
                    "tag": row["tag"],
                })

        res = txn.mutate(set_obj=tags)
        txn.commit()
        print(f"Tags cargados: {len(tags)}")
        return res.uids
    finally:
        txn.discard()

#crear relaciones
def create_edges(client, user_uids, pin_uids, board_uids, tag_uids):
    txn = client.txn()
    try:
        #SAVES
        with open("csv/saves.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["user_id"]],
                    "SAVES": [{"uid": pin_uids[row["pin_id"]],
                               "SAVES|timestamp": row["timestamp"]}],
                })

        #COMMENTS
        with open("csv/comments.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["user_id"]],
                    "COMMENTS": [{"uid": pin_uids[row["pin_id"]],
                                  "COMMENTS|timestamp": row["timestamp"]}],
                })

        #LIKES
        with open("csv/likes.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["user_id"]],
                    "LIKES": [{"uid": pin_uids[row["pin_id"]],
                               "LIKES|timestamp": row["timestamp"]}],
                })

        #FOLLOWS
        with open("csv/follows.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["follower_id"]],
                    "FOLLOWS": [{"uid": user_uids[row["followed_id"]],
                                 "FOLLOWS|timestamp": row["timestamp"]}],
                })

        #CREATES
        with open("csv/creates.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["user_id"]],
                    "CREATES": [{"uid": board_uids[row["board_id"]],
                                 "CREATES|timestamp": row["timestamp"]}],
                })

        #SHARES
        with open("csv/shares.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": user_uids[row["user_id"]],
                    "SHARES": [{"uid": board_uids[row["board_id"]]}],
                })

        # MADE_OF
        with open("csv/made_of.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": pin_uids[row["pin_id"]],
                    "MADE_OF": [{"uid": board_uids[row["board_id"]]}],
                })

        # CONTAINS
        with open("csv/contains.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn.mutate(set_obj={
                    "uid": pin_uids[row["pin_id"]],
                    "CONTAINS": [{"uid": tag_uids[row["tag_id"]]}],
                })

        txn.commit()
        print("Relaciones creadas")
    finally:
        txn.discard()

# Queries
def query1(client):
    #Consultar todos los usuarios que tengan más de 20 años y los tableros que han creado.
    age = ask_int("Edad mínima (mayores a)", 20)
    limit = ask_int("Límite de resultados (limit)", 3)
    skip = ask_int("Resultados a saltar (skip)", 0)
 
    query = """
    query q($age: int, $limit: int, $skip: int) {
        usuarios(func: gt(age, $age), orderdesc: follower_count, first: $limit, offset: $skip) @filter(type(User)) {
            uid
            username
            age
            follower_count
            total_tableros: count(CREATES)
            CREATES {
                board_name
            }
        }
    }
    """
 
    res = client.txn(read_only=True).query(
        query, variables={'$age': age, '$limit': limit, '$skip': skip})
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))


def query2(client):
    #Mostrar todas las relaciones que tiene un usuario con los otros nodos: que tableros han creado, 
    # los usuarios que sigue, y los pines que ha likeado + comentado + compartido.
    username = input("Username (ej. fatima): ")
 
    query = """
    query q($username: string) {
        usuarios_relaciones(func: eq(username, $username)) @filter(type(User)) {
            username
            age
            follower_count
            seguidores: count(~FOLLOWS)
            total_seguidos: count(FOLLOWS)
            total_likes: count(LIKES)
            total_saves: count(SAVES)
            total_comments: count(COMMENTS)
 
            CREATES  { board_name }
            SHARES   { board_name }
            FOLLOWS  (orderasc: username) { username }
            LIKES    (orderdesc: like_count) { image_url }
            SAVES    { image_url }
            COMMENTS { image_url }
        }
    }
    """
 
    res = client.txn(read_only=True).query(query, variables={'$username': username})
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))

def query3(client):
    #Mostrar todos los pines con más de n likes para ver que pines son los más populares.
    likes = ask_int("Likes mínimos", 1000)
    limit = ask_int("Límite de resultados (limit)", 5)
    skip = ask_int("Resultados a saltar (skip)", 0)
 
    query = """
    query q($likes: int, $limit: int, $skip: int) {
        pines_populares(func: gt(like_count, $likes), orderdesc: like_count, first: $limit, offset: $skip) @filter(type(Pin)) {
            image_url
            like_count
            comment_count
            views
            usuarios_que_dieron_like: count(~LIKES)
        }
    }
    """
 
    res = client.txn(read_only=True).query(
        query, variables={'$likes': likes, '$limit': limit, '$skip': skip})
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))    

def query4(client):
    #Consultar que usuarios han guardado un pin especifico y en que tablero han sido guardados.
    print("Ejemplo: https://pinterest-lab.example.com/img/p01.jpg")
    image_url = input("image_url del pin: ").strip()
 
    query = """
    query q($image_url: string) {
        pines_guardados(func: eq(image_url, $image_url)) @filter(type(Pin)) {
            image_url
            like_count
            total_guardados: count(~SAVES)
            total_likes_usuarios: count(~LIKES)
            CONTAINS { tag }
            MADE_OF  { board_name }
            ~SAVES (orderasc: username) { username }
            ~LIKES (orderasc: username) { username }
        }
    }
    """
 
    res = client.txn(read_only=True).query(query, variables={'$image_url': image_url})
    print(json.dumps(json.loads(res.json), indent=2, ensure_ascii=False))


# Eliminaciones
def delete_by_condition(client):
    """Eliminar datos que cumplan una condición específica."""
    value = input("Eliminar usuarios con menos de cuántos seguidores: ")
    try:
        value = str(int(value))
    except ValueError:
        print("Valor inválido")
        return

    query = """
    query q($n: int) {
        usuarios(func: lt(follower_count, $n)) @filter(type(User)) {
            uid
            username
            follower_count
        }
    }
    """

    txn = client.txn()
    try:
        res = txn.query(query, variables={'$n': value})
        users = json.loads(res.json)["usuarios"]

        if not users:
            print("No hay usuarios que cumplan la condición")
            return

        txn.mutate(del_obj=[{"uid": u["uid"]} for u in users])
        txn.commit()
        print("Usuarios eliminados:", [u["username"] for u in users])
    finally:
        txn.discard()


# DROP ALL
def delete_all(client):
    op = pydgraph.Operation(drop_all=True)
    client.alter(op)