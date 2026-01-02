import pandas as pd
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

def limpiar_detalle_ventas(path: str) -> pd.DataFrame:
    detalle = pd.read_csv(path)

    # --- id_venta numérico ---
    detalle["id_venta"] = pd.to_numeric(
        detalle["id_venta"],
        errors="coerce"
    )

    # --- id_producto numérico ---
    detalle["id_producto"] = pd.to_numeric(
        detalle["id_producto"],
        errors="coerce"
    )

    # --- cantidad numérica ---
    detalle["cantidad"] = pd.to_numeric(
        detalle["cantidad"],
        errors="coerce"
    )

    # --- precio_unitario decimal ---
    detalle["precio_unitario"] = (
        detalle["precio_unitario"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    detalle["precio_unitario"] = pd.to_numeric(
        detalle["precio_unitario"],
        errors="coerce"
    )

    # --- importe decimal ---
    detalle["importe"] = (
        detalle["importe"]
        .astype(str)
        .str.replace(",", ".", regex=False)
    )

    detalle["importe"] = pd.to_numeric(
        detalle["importe"],
        errors="coerce"
    )

    # --- nombre_producto en minúscula sin acentos ---
    detalle["nombre_producto"] = (
        detalle["nombre_producto"]
        .astype(str)
        .str.strip()
        .str.lower()
        .apply(quitar_acentos)
    )

    # --- eliminar registros inválidos ---
    detalle = detalle.dropna(
        subset=[
            "id_venta",
            "id_producto",
            "cantidad",
            "precio_unitario",
            "importe"
        ]
    )

    return detalle
