from pathlib import Path
import re

DOC_PATH = Path("documentacion_tienda.md")


# =========================
# Cargar secciones (solo ##)
# =========================
def cargar_secciones():
    if not DOC_PATH.exists():
        raise FileNotFoundError("No se encontró documentacion_tienda.md")

    with open(DOC_PATH, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    secciones = {}
    buffer = []
    indice = 0

    for linea in lineas:
        if re.match(r"^##\s(?!#)", linea):
            if buffer:
                secciones[indice] = "".join(buffer).strip()
                buffer = []
            indice += 1
        buffer.append(linea)

    if buffer:
        secciones[indice] = "".join(buffer).strip()

    return secciones


# =========================
# Mostrar menú
# =========================
def mostrar_menu(secciones):
    print("\n===== MENU =====")
    for k, v in secciones.items():
        titulo = v.splitlines()[0].replace("##", "").strip()
        print(f"{k}. {titulo}")

    print("E. Exportar sección")
    print("B. Búsqueda")
    print("0. Salir")
    print("----------------")


# =========================
# Exportar sección
# =========================
def exportar_seccion(secciones):
    try:
        num = int(input("Ingrese número de sección a exportar: "))
        if num not in secciones:
            print("Sección inválida.")
            return

        nombre = input("Nombre de archivo (sin extensión): ").strip()
        with open(f"{nombre}.txt", "w", encoding="utf-8") as f:
            f.write(secciones[num])

        print(f"Sección exportada como {nombre}.txt")

    except ValueError:
        print("Debe ingresar un número válido.")


# =========================
# Búsqueda
# =========================
def buscar(secciones):
    palabra = input("Ingrese palabra clave: ").lower().strip()
    resultados = []

    for k, texto in secciones.items():
        if palabra in texto.lower():
            titulo = texto.splitlines()[0].replace("##", "").strip()
            resultados.append(f"{k}. {titulo}")

    if resultados:
        print("\nCoincidencias encontradas:")
        print("\n".join(resultados))
    else:
        print("No se encontraron coincidencias.")


# =========================
# Menú principal
# =========================
def menu_interactivo():
    secciones = cargar_secciones()

    while True:
        mostrar_menu(secciones)
        opcion = input("Seleccione una opción: ").strip().lower()

        if opcion == "0":
            print("Saliendo del menú...")
            break

        elif opcion.isdigit():
            num = int(opcion)
            if num in secciones:
                print("\n" + secciones[num])
            else:
                print("Sección inválida.")

        elif opcion == "e":
            exportar_seccion(secciones)

        elif opcion == "b":
            buscar(secciones)

        else:
            print("Opción inválida.")
