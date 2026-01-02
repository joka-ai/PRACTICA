import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score
import os

def entrenar_modelo_recomendacion_avanzado(path_excel, path_graficos="ml/outputs/"):
    os.makedirs(path_graficos, exist_ok=True)

    # Cargar datos
    clientes = pd.read_excel(path_excel, sheet_name="CLIENTES")
    productos = pd.read_excel(path_excel, sheet_name="PRODUCTOS")
    ventas = pd.read_excel(path_excel, sheet_name="VENTAS")
    detalle = pd.read_excel(path_excel, sheet_name="DETALLE_VENTAS")

    # Merge para obtener información completa de cada venta
    df = detalle.merge(
        ventas[['id_venta', 'id_cliente', 'fecha', 'medio_pago']], on='id_venta', how='left'
    ).merge(
        clientes[['id_cliente', 'ciudad', 'fecha_alta']], on='id_cliente', how='left'
    ).merge(
        productos[['id_producto', 'categoria', 'precio_unitario']], on='id_producto', how='left'
    )

    # Variables temporales
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['fecha_alta'] = pd.to_datetime(df['fecha_alta'])
    df['mes'] = df['fecha'].dt.month
    df['dia_semana'] = df['fecha'].dt.dayofweek
    df['fin_de_semana'] = (df['dia_semana'] >= 5).astype(int)
    df['trimestre'] = df['fecha'].dt.quarter
    df['antiguedad_cliente_dias'] = (df['fecha'] - df['fecha_alta']).dt.days

    # Features de historial de compras por cliente
    historial_cliente = df.groupby('id_cliente').agg(
        total_compras=('id_venta', 'count'),
        gasto_total=('importe', 'sum'),
        medio_pago_frecuente=('medio_pago', lambda x: x.mode()[0] if not x.mode().empty else np.nan)
    ).reset_index()

    # Features de historial por cliente-categoría
    historial_categoria = df.groupby(['id_cliente','categoria']).agg(
        cantidad_categoria=('cantidad', 'sum'),
        gasto_categoria=('importe', 'sum')
    ).reset_index()

    # Generar dataset cliente-producto
    clientes_unicos = clientes['id_cliente'].unique()
    productos_unicos = productos['id_producto'].unique()
    dataset = pd.MultiIndex.from_product([clientes_unicos, productos_unicos], names=['id_cliente', 'id_producto']).to_frame(index=False)

    # Etiqueta de compra
    df['comprado'] = 1
    dataset = dataset.merge(df[['id_cliente','id_producto','comprado']], on=['id_cliente','id_producto'], how='left')
    dataset['comprado'] = dataset['comprado'].fillna(0)

    # Merge con clientes y productos
    dataset = dataset.merge(clientes[['id_cliente','ciudad']], on='id_cliente', how='left')
    dataset = dataset.merge(productos[['id_producto','categoria','precio_unitario']], on='id_producto', how='left')
    dataset = dataset.merge(historial_cliente, on='id_cliente', how='left')

    # Merge con historial por categoría
    dataset = dataset.merge(
        historial_categoria, 
        left_on=['id_cliente','categoria'], 
        right_on=['id_cliente','categoria'], 
        how='left'
    )
    dataset['cantidad_categoria'] = dataset['cantidad_categoria'].fillna(0)
    dataset['gasto_categoria'] = dataset['gasto_categoria'].fillna(0)

    # Codificación de variables categóricas
    X = pd.get_dummies(dataset[['ciudad','categoria','precio_unitario','medio_pago_frecuente']], drop_first=True)
    y = dataset['comprado']

    # Separar train/test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Entrenar RandomForest
    modelo = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    modelo.fit(X_train, y_train)

    # Evaluación
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:,1]
    accuracy = accuracy_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    print(f"Accuracy: {accuracy:.3f}")
    print(f"ROC-AUC: {auc:.3f}")

    # Probabilidades para recomendaciones
    dataset['probabilidad'] = modelo.predict_proba(pd.get_dummies(dataset[['ciudad','categoria','precio_unitario','medio_pago_frecuente']], drop_first=True))[:,1]

    return modelo, dataset
