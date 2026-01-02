import pandas as pd
from pathlib import Path


def generar_analisis_descriptivo(
    path_excel: str,
    path_salida_txt: str
):
    
    # Carga de datos
    xls = pd.ExcelFile(path_excel)

    clientes = pd.read_excel(xls, "CLIENTES")
    productos = pd.read_excel(xls, "PRODUCTOS")
    ventas = pd.read_excel(xls, "VENTAS")
    detalle = pd.read_excel(xls, "DETALLE_VENTAS")

    # =========================
    # Modelo analítico
    # Nivel: línea de venta
    # =========================
    df = (
        detalle
        .merge(ventas, on="id_venta", how="left")
        .merge(clientes, on="id_cliente", how="left")
        .merge(productos, on="id_producto", how="left")
    )

   
    # Normalización
    if "nombre_producto_x" in df.columns:
        df = df.rename(columns={"nombre_producto_x": "nombre_producto"})

    df["fecha"] = pd.to_datetime(df["fecha"])
    df["fecha_alta"] = pd.to_datetime(df["fecha_alta"])

    # Estadísticas descriptivas
    desc_num = df.describe(percentiles=[0.25, 0.5, 0.75])
    desc_cat = df.select_dtypes(include="object").describe()

    # KPIs – NIVEL LÍNEA
    ventas_totales = df["importe"].sum()
    ventas_promedio_linea = df["importe"].mean()

   
    # KPIs – NIVEL VENTA 
    ventas_por_venta = (
        df.groupby("id_venta", as_index=False)["importe"]
        .sum()
        .rename(columns={"importe": "total_venta"})
    )

    total_ventas = ventas_por_venta["id_venta"].nunique()
    ticket_promedio = ventas_por_venta["total_venta"].mean()
    venta_maxima = ventas_por_venta["total_venta"].max()
    venta_minima = ventas_por_venta["total_venta"].min()


    # KPIs de negocio
    top_productos = (
        df.groupby("nombre_producto")["importe"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    ventas_ciudad = (
        df.groupby("ciudad")["importe"]
        .sum()
        .sort_values(ascending=False)
    )


    # Output TXT
    Path(path_salida_txt).parent.mkdir(parents=True, exist_ok=True)

    with open(path_salida_txt, "w", encoding="utf-8") as f:
        f.write("## ANALISIS DESCRIPTIVO DE VENTAS\n\n")

        f.write("### Estadisticas Numericas (Nivel Línea)\n")
        f.write(desc_num.to_string())

        f.write("\n\n### Estadisticas Categoricas\n")
        f.write(desc_cat.to_string())

        f.write("\n\n### KPIs – Nivel Línea\n")
        f.write(f"Ventas Totales: {ventas_totales:,.2f}\n")
        f.write(f"Venta Promedio por Línea: {ventas_promedio_linea:,.2f}\n")

        f.write("\n\n### KPIs – Nivel Venta (Corregido)\n")
        f.write(f"Total de Ventas: {total_ventas}\n")
        f.write(f"Ticket Promedio: {ticket_promedio:,.2f}\n")
        f.write(f"Venta Máxima: {venta_maxima:,.2f}\n")
        f.write(f"Venta Mínima: {venta_minima:,.2f}\n")

        f.write("\n\n### Top 5 Productos por Ventas\n")
        f.write(top_productos.to_string())

        f.write("\n\n### Ventas por Ciudad\n")
        f.write(ventas_ciudad.to_string())
