import pandas as pd

def limpiar_productos(path: str) -> pd.DataFrame:
    productos = pd.read_csv(path)

    # --- id_producto numérico ---
    productos["id_producto"] = pd.to_numeric(
        productos["id_producto"],
        errors="coerce"
    )

    # --- nombre_producto en minúscula ---
    productos["nombre_producto"] = (
        productos["nombre_producto"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # --- precio_unitario decimal ---
    productos["precio_unitario"] = (
        productos["precio_unitario"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    productos["precio_unitario"] = pd.to_numeric(
        productos["precio_unitario"],
        errors="coerce"
    )

    # =============================
    # REGLAS DE CATEGORIZACIÓN
    # =============================

    palabras_limpieza = [
        "detergente", "lavandina", "jabón", "shampoo",
        "papel", "servilleta", "toalla", "desodorante",
        "crema dental", "cepillo", "hilo dental",
        "suavizante", "limpiavidrios", "desengrasante",
        "esponja", "trapo", "mascarilla"
    ]

    palabras_alimentos = [
        "cola", "pepsi", "sprite", "fanta", "agua",
        "jugo", "yerba", "café", "té", "leche", "yogur",
        "queso", "manteca", "pan", "medialuna",
        "galletita", "alfajor", "papa", "maní",
        "chocolate", "turrón", "dulce", "mermelada",
        "helado", "aceite", "vinagre", "salsa",
        "arroz", "fideo", "lenteja", "garbanzo",
        "poroto", "harina", "azúcar", "sal",
        "miel", "granola", "avena", "cerveza",
        "vino", "sidra", "fernet", "vodka", "ron",
        "gin", "whisky", "licor", "pizza", "empanada",
        "hamburguesa", "verdura", "aceituna",
        "sopa", "caldo", "chicle", "caramelo"
    ]

    def clasificar_categoria(nombre):
        for palabra in palabras_limpieza:
            if palabra in nombre:
                return "limpieza"
        for palabra in palabras_alimentos:
            if palabra in nombre:
                return "alimentos"
        return "alimentos"  # default de negocio

    productos["categoria"] = productos["nombre_producto"].apply(clasificar_categoria)

    # --- Limpieza de categoría: minúsculas y quitar acentos ---
    productos["categoria"] = (
        productos["categoria"]
        .str.lower()
        .str.normalize('NFKD')  # Descompone caracteres con acentos
        .str.encode('ascii', errors='ignore')  # Elimina lo que no sea ASCII (los acentos)
        .str.decode('utf-8')  # Lo vuelve a convertir a texto
    )

    # --- eliminar duplicados ---
    productos = productos.drop_duplicates(
        subset=["nombre_producto"],
        keep="first"
    )

    # --- eliminar registros inválidos ---
    productos = productos.dropna(
        subset=["id_producto", "precio_unitario"]
    )

    return productos
