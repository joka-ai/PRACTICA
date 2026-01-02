import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import FuncFormatter


def formato_miles(x, pos):
    return f"{int(x):,}".replace(",", ".")


def formato_moneda(x, pos):
    return f"${int(x):,}".replace(",", ".")


def generar_graficos(path_excel: str, path_salida: str):

    xls = pd.ExcelFile(path_excel)

    clientes = pd.read_excel(xls, "CLIENTES")
    productos = pd.read_excel(xls, "PRODUCTOS")
    ventas = pd.read_excel(xls, "VENTAS")
    detalle = pd.read_excel(xls, "DETALLE_VENTAS")

    df = (
        detalle
        .merge(ventas, on="id_venta", how="left")
        .merge(clientes, on="id_cliente", how="left")
        .merge(productos, on="id_producto", how="left")
    )

    if "nombre_producto_x" in df.columns:
        df = df.rename(columns={"nombre_producto_x": "nombre_producto"})

    df["fecha"] = pd.to_datetime(df["fecha"])
    Path(path_salida).mkdir(parents=True, exist_ok=True)

    # =========================
    # Línea – Ventas mensuales
    # =========================
    ventas_mensual = (
        df
        .groupby(df["fecha"].dt.to_period("M"))["importe"]
        .sum()
        .sort_index()
    )

    plt.figure(figsize=(8, 4))
    plt.plot(ventas_mensual.index.astype(str), ventas_mensual.values, marker="o")
    plt.title("Evolución Mensual de Ventas")
    plt.xlabel("Mes")
    plt.ylabel("Importe total")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(formato_moneda))
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)

    for x, y in enumerate(ventas_mensual.values):
        plt.text(x, y, f"${int(y):,}".replace(",", "."), 
                 ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{path_salida}/ventas_mensuales.png")
    plt.close()

    # =========================
    # Heatmap – Correlaciones 
    # =========================

    # 1. Eliminar columnas duplicadas
    cols_a_eliminar = [
        "precio_unitario_y",  # duplicada
    ]

    df_corr = df.drop(columns=[c for c in cols_a_eliminar if c in df.columns])

    # 2. Excluir identificadores
    ids = ["id_venta", "id_cliente", "id_producto"]
    df_corr = df_corr.drop(columns=[c for c in ids if c in df_corr.columns])

    # 3. Seleccionar solo variables numéricas relevantes
    df_corr = df_corr.select_dtypes(include="number")

    # 4. Calcular correlación
    corr = df_corr.corr()

    # 5. Graficar
    plt.figure(figsize=(7, 6))
    im = plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    plt.colorbar(im, fraction=0.046, pad=0.04)

    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)

    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            plt.text(
                j, i,
                f"{corr.iloc[i, j]:.2f}",
                ha="center", va="center",
                fontsize=8
            )

    plt.title(
        "Correlación entre Variables de Negocio\n"
        "Relación con el Importe de Ventas"
    )
    plt.tight_layout()
    plt.savefig(f"{path_salida}/heatmap_correlaciones.png")
    plt.close()
