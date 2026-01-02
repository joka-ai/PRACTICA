## Tema

**Análisis completo de ventas y comportamiento de clientes en la tienda**

Este análisis busca entender la performance de la tienda a través de indicadores clave como ventas totales, categorías más rentables, medios de pago preferidos, distribución geográfica de clientes, evolución mensual de ventas y patrones de actividad según los días de la semana.

La información obtenida permitirá tomar decisiones basadas en datos para mejorar estrategias de venta, inventario y marketing.

---

## Algunos Problemas Planteados
*Rendimiento Financiero:*
¿Cuál fue el total recaudado?
*Rentabilidad del Producto:*
¿Qué categorías de productos generan más ingresos? (Esto ayuda a optimizar el inventario y las promociones).
*Comportamiento del Cliente:*
¿Cuál es la distribución geográfica de ventas por ciudad o localidad? (Esto informa sobre posibles expansiones o estrategias de marketing localizado).
*Tendencias y Estacionalidad:*
¿Cómo evolucionan las ventas mes a mes? (Para identificar estacionalidad, tendencias de crecimiento o caída).
¿Qué días de la semana concentran más ventas? (Para optimizar la dotación de personal, horarios o promociones específicas).

---

## Dataset de referencia

**Fuente:** Datos generados con fines educativos.

**Definición:** Base que representa una tienda con catálogo de productos, clientes registrados, ventas y detalle de ventas.

---

## Estructura de datos

### CLIENTES

| Campo          | Tipo de dato | Escala / Definición                   |
| -------------- | ------------ | ------------------------------------- |
| id_cliente     | INT          | Identificador único (clave primaria)  |
| nombre_cliente | VARCHAR      | Nombre completo del cliente (nominal) |
| email          | VARCHAR      | Correo electrónico único (nominal)    |
| ciudad         | VARCHAR      | Ciudad de residencia (nominal)        |
| fecha_alta     | DATE         | Fecha de registro (temporal, ordinal) |

### DETALLE_VENTAS

| Campo           | Tipo de dato | Escala / Definición                  |
| --------------- | ------------ | ------------------------------------ |
| id_venta        | INT          | Identificador de venta (nominal)     |
| id_producto     | INT          | Identificador del producto (nominal) |
| nombre_producto | VARCHAR      | Nombre descriptivo (nominal)         |
| cantidad        | INT          | Unidades vendidas (razón)            |
| precio_unitario | DECIMAL      | Precio por unidad (razón)            |
| importe         | DECIMAL      | Total de la venta (razón)            |

### PRODUCTOS

| Campo           | Tipo de dato | Escala / Definición                  |
| --------------- | ------------ | ------------------------------------ |
| id_producto     | INT          | Identificador único (clave primaria) |
| nombre_producto | VARCHAR      | Nombre descriptivo (nominal)         |
| categoria       | VARCHAR      | Clasificación del producto (nominal) |
| precio_unitario | DECIMAL      | Precio por unidad (razón)            |

### VENTAS

| Campo          | Tipo de dato | Escala / Definición                      |
| -------------- | ------------ | ---------------------------------------- |
| id_venta       | INT          | Identificador único (clave primaria)     |
| fecha          | DATE         | Fecha de la venta (temporal, ordinal)    |
| id_cliente     | INT          | FK hacia clientes (nominal)              |
| nombre_cliente | VARCHAR      | Nombre del cliente (nominal, redundante) |
| email          | VARCHAR      | Email del cliente (nominal, redundante)  |
| medio_pago     | VARCHAR      | Medio de pago (nominal)                  |

---

## Escalas de medición

* **Nominal:** Categorías sin orden (ej: ciudad, nombre de producto).
* **Ordinal:** Categorías con orden (ej: fechas, rankings).
* **Razón:** Valores numéricos con cero absoluto (ej: cantidad, importe).
* **Intervalo:** Valores numéricos sin cero absoluto real (ej: temperatura).

---

## Proceso de limpieza de datos
* Normalización de columnas
* Conversión de tipos de datos
* Validación de valores nulos y formatos
* correcion de productos en categoria equivocada 
---

## Análisis estadístico y visualizaciones

El módulo de análisis realiza un estudio descriptivo completo sobre la base depurada:

### Estadísticas
- **Numéricas:** count, mean, std, min, max y percentiles 25%, 50%, 75% para entender la dispersión.
- **Categóricas:** count, unique, top y freq para identificar los valores más frecuentes.

### Indicadores de negocio
- **Ventas Totales:** suma de todos los importes de venta.
- **Venta Promedio:** promedio de importe por transacción.
- **Top 5 Productos por Ventas:** productos con mayor facturación acumulada.
- **Ventas por Ciudad:** distribución de ventas agregadas por ciudad.

### Visualizaciones
- **Evolución Mensual de Ventas:** gráfico de línea mostrando la tendencia de ventas por mes.
- **Mapa de Correlaciones Numéricas:** heatmap para identificar relaciones entre variables numéricas.

- El gráfico confirma que el importe (los ingresos totales) tiene una relación fuerte y positiva con las otras dos variables, pero con matices distintos: 
-**Con el Precio Unitario (0.68):** Existe una correlación positiva moderada-alta. Esto indica que, en general, las ventas de mayor valor monetario en este dataset están más impulsadas por el precio de los productos que por la cantidad vendida. 
- **Con la Cantidad (0.60):** También hay una relación sólida. Los aumentos en el volumen de unidades vendidas impactan directamente en el crecimiento del importe. 
- **Correlación de -0.07:** Este es un hallazgo clave. Indica que no hay una relación entre el precio del producto y cuántas unidades compra el cliente. 
- **Interpretación de negocio:** Los clientes no parecen comprar menos unidades solo porque el precio sube, ni compran muchas más unidades porque el precio sea muy bajo. Esto sugiere una demanda inelástica o que los productos se compran por necesidad independientemente de su costo unitario. 

---

## Machine Learning aplicado a la tienda

### Objetivo
Predecir la probabilidad de que un cliente compre un producto determinado, con el fin de generar **recomendaciones personalizadas** para aumentar la venta cruzada y mejorar la experiencia del cliente.

---

### Algoritmo
Se utiliza **RandomForestClassifier**, un algoritmo de ensamble de árboles de decisión que:

- Maneja datos categóricos y numéricos.
- Captura relaciones no lineales entre variables.
- Es robusto frente a sobreajuste cuando se ajusta adecuadamente.
- Permite obtener la probabilidad de compra para cada cliente-producto.

---

### Variables

**Entradas (features):**  

1. **Cliente**
   - `ciudad`: Ciudad del cliente
   - `antiguedad_cliente_dias`: Antigüedad del cliente en días desde la fecha de alta
   - `total_compras`: Total de compras realizadas por el cliente
   - `gasto_total`: Gasto total del cliente
   - `medio_pago_frecuente`: Medio de pago más usado por el cliente

2. **Producto**
   - `categoria`: Categoría del producto
   - `precio_unitario`: Precio del producto

3. **Historial de compras por cliente-categoría**
   - `cantidad_categoria`: Cantidad comprada en esa categoría
   - `gasto_categoria`: Gasto realizado en esa categoría

4. **Variables temporales**
   - `mes`: Mes de la compra
   - `dia_semana`: Día de la semana de la compra
   - `fin_de_semana`: Booleano, indica si la compra fue en fin de semana
   - `trimestre`: Trimestre de la compra

**Salida (target):**  
- `comprado`: binaria (1 si el cliente compró el producto, 0 si no)

---

### Evaluación
- **Accuracy:** Proporción de predicciones correctas sobre el total de observaciones.
- **ROC-AUC:** Capacidad del modelo para discriminar entre productos comprados y no comprados.
- Evaluación realizada sobre un conjunto de prueba separado (20% del dataset).

---

### Resultados
- Modelo: **RandomForestClassifier** con 300 árboles (`n_estimators=300`) y características codificadas automáticamente.
- Se generan **probabilidades de compra** para cada cliente-producto, permitiendo crear un **ranking de productos recomendados**.
- Ejemplo de recomendaciones para un cliente específico (`id_cliente = 1`):

