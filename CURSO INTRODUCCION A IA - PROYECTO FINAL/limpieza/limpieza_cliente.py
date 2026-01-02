import pandas as pd
import re

def limpiar_clientes(path: str) -> pd.DataFrame:
    clientes = pd.read_csv(path)

    # --- id_cliente numérico ---
    clientes["id_cliente"] = pd.to_numeric(
        clientes["id_cliente"],
        errors="coerce"
    )

    # --- fecha_alta a formato fecha ---
    clientes["fecha_alta"] = pd.to_datetime(
    clientes["fecha_alta"],
    errors="coerce"
    ).dt.date


    # --- nombre_cliente y ciudad en minúscula ---
    for col in ["nombre_cliente", "ciudad"]:
        clientes[col] = (
            clientes[col]
            .astype(str)
            .str.strip()
            .str.lower()
        )

    # --- limpieza y validación de email ---
    clientes["email"] = (
        clientes["email"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

    clientes["email_valido"] = clientes["email"].apply(
        lambda x: True if re.match(email_regex, x) else False
    )

    # anular emails inválidos ---
    clientes.loc[
        clientes["email_valido"] == False,
        "email"
    ] = None

    # --- eliminar duplicados por email ---
    clientes = clientes.drop_duplicates(
        subset="email",
        keep="first"
    )

    return clientes
