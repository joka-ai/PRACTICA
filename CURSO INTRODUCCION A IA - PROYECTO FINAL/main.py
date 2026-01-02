import pandas as pd
from limpieza.limpieza_cliente import limpiar_clientes
from limpieza.limpieza_productos import limpiar_productos
from limpieza.limpieza_ventas import limpiar_ventas
from limpieza.limpieza_detalleventas import limpiar_detalle_ventas

from union.export_excel import exportar_excel_con_pestanias
from analysis.analisis_descriptivo import generar_analisis_descriptivo
from analysis.graficos import generar_graficos

from ml.prediccion_ventas import entrenar_modelo_recomendacion_avanzado

from menu.menu import menu_interactivo

PATH_RAW = "data/"
PATH_PROCESSED = "data/procesado/"
PATH_CURADO = PATH_PROCESSED + "ventas_curadas.xlsx"
PATH_ANALISIS_TXT = "analysis/outputs/analisis_descriptivo.txt"
PATH_GRAFICOS = "analysis/outputs/"

clientes = limpiar_clientes(PATH_RAW + "clientes.csv")
productos = limpiar_productos(PATH_RAW + "productos.csv")
ventas = limpiar_ventas(PATH_RAW + "ventas.csv")
detalle = limpiar_detalle_ventas(PATH_RAW + "detalle_ventas.csv")

exportar_excel_con_pestanias(
    path_salida=PATH_CURADO,
    clientes=clientes,
    productos=productos,
    ventas=ventas,
    detalle=detalle
)

generar_analisis_descriptivo(
    path_excel=PATH_CURADO,
    path_salida_txt=PATH_ANALISIS_TXT
)

generar_graficos(
    path_excel=PATH_CURADO,
    path_salida=PATH_GRAFICOS
)


print("Entrenando modelo de recomendación avanzado...")
modelo, dataset_recomendacion = entrenar_modelo_recomendacion_avanzado(PATH_CURADO)

# Recomendaciones para un cliente específico (por ejemplo, cliente con id_cliente=1)
id_cliente_ejemplo = 1
top5 = dataset_recomendacion[dataset_recomendacion['id_cliente']==id_cliente_ejemplo] \
        .sort_values('probabilidad', ascending=False) \
        .head(5)

print(f"Top 5 productos recomendados para el cliente {id_cliente_ejemplo}:")
print(top5[['id_producto','categoria','probabilidad']])

menu_interactivo()
