import pandas as pd
from pathlib import Path
import xlsxwriter

def exportar_excel_con_pestanias(
    path_salida: str,
    clientes: pd.DataFrame,
    productos: pd.DataFrame,
    ventas: pd.DataFrame,
    detalle: pd.DataFrame
) -> None:
   
    # Crear carpeta si no existe
    Path(path_salida).parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(path_salida, engine="xlsxwriter") as writer:
        clientes.to_excel(writer, sheet_name="CLIENTES", index=False)
        productos.to_excel(writer, sheet_name="PRODUCTOS", index=False)
        ventas.to_excel(writer, sheet_name="VENTAS", index=False)
        detalle.to_excel(writer, sheet_name="DETALLE_VENTAS", index=False)
