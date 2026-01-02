import pandas as pd
import re
import unicodedata

def quitar_acentos(texto: str) -> str:
    if pd.isna(texto):
        return texto
    return (
        unicodedata
        .normalize("NFKD", texto)
        .encode("ascii", "ignore")
        .decode("utf-8")
    )

def limpiar_ventas(path: str) -> pd.DataFrame:
    ventas = pd.read_csv(path)

    # --- id_venta numérico ---
    ventas["id_venta"] = pd.to_numeric(
        ventas["id_venta"],
        errors="coerce"
    )

    # --- id_cliente numérico ---
    ventas["id_cliente"] = pd.to_numeric(
        ventas["id_cliente"],
        errors="coerce"
    )

    # --- fecha en formato fecha ---
    ventas["fecha"] = pd.to_datetime(
        ventas["fecha"],
        errors="coerce"
    ).dt.date

    # --- nombre_cliente en minúscula sin acentos ---
    ventas["nombre_cliente"] = (
        ventas["nombre_cliente"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(quitar_acentos)
    )

    # --- medio_pago en minúscula sin acentos ---
    ventas["medio_pago"] = (
        ventas["medio_pago"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(quitar_acentos)
    )

    # --- limpieza y validación de email ---
    ventas["email"] = (
        ventas["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

    ventas["email_valido"] = ventas["email"].apply(
        lambda x: True if re.match(email_regex, x) else False
    )

    ventas.loc[
        ventas["email_valido"] == False,
        "email"
    ] = None

    # --- eliminar registros inválidos ---
    ventas = ventas.dropna(
        subset=["id_venta", "id_cliente", "fecha"]
    )

    return ventas
