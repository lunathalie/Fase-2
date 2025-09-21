# campus_uvg_interactivo_v4.py

# ----------------- EDIFICIOS UVG PREDEFINIDOS -----------------
EDIFICIOS = [
    "CIT",
    "Edificio A",
    "Edificio C",
    "Edificio Ca",
    "Edificio C1",
    "Edificio D",
    "Edificio E",
    "Edificio F",
    "Edificio G",
    "Edificio H",
    "Edificio I",
    "Edificio J",
    "Edificio J1",
    "Edificio K",
    "Edificio II-1",
    "Edificio II-2",
    "Casita Roja",
    "Invernadero",
]

# ----------------- Baños (generados) -----------------
banos = []

for nivel in range(1, 8):
    banos.append({"id": f"CIT{nivel}-IZQ-H", "edificio": "CIT", "nivel": nivel, "lado": "Izq", "genero": "H", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-IZQ-M", "edificio": "CIT", "nivel": nivel, "lado": "Izq", "genero": "M", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-DER-H", "edificio": "CIT", "nivel": nivel, "lado": "Der", "genero": "H", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-DER-M", "edificio": "CIT", "nivel": nivel, "lado": "Der", "genero": "M", "en_limpieza": False})

for edif in EDIFICIOS:
    if edif == "CIT":
        continue
    base = edif.replace(" ", "")
    banos.append({"id": f"{base}-H", "edificio": edif, "nivel": 1, "genero": "H", "en_limpieza": False})
    banos.append({"id": f"{base}-M", "edificio": edif, "nivel": 1, "genero": "M", "en_limpieza": False})

# ----------------- Biblioteca (con cantidades) -----------------
biblioteca = {
    "ipads": 30,
    "audifonos": 20,
    "cargadores": 50,
    "kindles": 10
}

# ----------------- Utilidades -----------------
def input_int(mensaje, default=None):
    txt = input(mensaje).strip()
    if txt == "" and default is not None:
        return default
    try:
        return int(txt)
    except:
        print("  Valor inválido, usando 0.")
        return 0

def input_si_no(mensaje, default=None):
    txt = input(mensaje).strip().lower()
    if txt == "" and default is not None:
        return default
    return txt in ("s", "si", "sí")

# ----------------- BAÑOS: ver & actualizar -----------------
def ver_banos():
    print("\n--- BAÑOS ---")
    # Filtro 1: género
    print("Selecciona género:")
    print("1) Hombres")
    print("2) Mujeres")
    print("3) Ambos")
    gsel = input("Opción: ").strip()
    if gsel == "1":
        genero = "H"
    elif gsel == "2":
        genero = "M"
    else:
        genero = None

    # Filtro 2: edificio
    print("\nSelecciona edificio:")
    for i, e in enumerate(EDIFICIOS, 1):
        print(f"{i}) {e}")
    print(f"{len(EDIFICIOS)+1}) Todos")
    esel = input("Opción: ").strip()
    if esel.isdigit() and 1 <= int(esel) <= len(EDIFICIOS):
        edificio = EDIFICIOS[int(esel)-1]
    else:
        edificio = None

    # Filtro 3: nivel (solo aplica si edificio es CIT)
    nivel = None
    if edificio == "CIT":
        txt = input("Filtrar por nivel (1-7, ENTER = todos): ").strip()
        if txt.isdigit():
            nivel = int(txt)

    # Filtrado final
    encontrados = [b for b in banos
                   if (genero is None or b["genero"] == genero)
                   and (edificio is None or b["edificio"] == edificio)
                   and (nivel is None or b["nivel"] == nivel)]

    if not encontrados:
        print("No se encontraron baños con esos filtros.")
        return

    print("\nID | Ubicación | Estado")
    for b in encontrados:
        estado = "EN LIMPIEZA" if b["en_limpieza"] else "Disponible"
        lado_txt = f" - {b['lado']}" if "lado" in b else ""
        ubic = f"{b['edificio']}{lado_txt} - Nivel {b['nivel']} ({b['genero']})"
        print(f"{b['id']} | {ubic} | {estado}")

def marcar_bano():
    print("\n--- MARCAR ESTADO DE BAÑO ---")
    bid = input("Escribe el ID del baño (ej: CIT3-IZQ-H, EdificioF-H): ").strip()
    bano = next((b for b in banos if b["id"].lower() == bid.lower()), None)
    if not bano:
        print("No existe ese ID. Sugerencia: primero usa 'Ver baños' con filtros para encontrarlo.")
        return
    print(f"Estado actual: {'EN LIMPIEZA' if bano['en_limpieza'] else 'Disponible'}")
    if input_si_no("¿Marcar EN LIMPIEZA? (si/no): "):
        bano["en_limpieza"] = True
        print("Marcado como EN LIMPIEZA.")
    elif input_si_no("¿Marcar DISPONIBLE? (si/no): "):
        bano["en_limpieza"] = False
        print("Marcado como DISPONIBLE.")
    else:
        print("Sin cambios.")

# ----------------- BIBLIOTECA -----------------
def ver_biblioteca():
    print("\n--- BIBLIOTECA ---")
    for recurso, cantidad in biblioteca.items():
        print(f"{recurso.capitalize()}: {cantidad}")

def actualizar_biblioteca():
    print("\n--- ACTUALIZAR BIBLIOTECA ---")
    for recurso, cantidad in biblioteca.items():
        biblioteca[recurso] = input_int(f"{recurso.capitalize()} (actual: {cantidad}): ", default=cantidad)
    print("Biblioteca ACTUALIZADA.")

# ----------------- Menús por rol -----------------
def menu_estudiante():
    while True:
        print("\n===== SERVICIOS DEL CAMPUS (UVG – Estudiantes) =====")
        print("1) Ver baños")
        print("2) Ver biblioteca")
        print("3) Salir")
        op = input("Elige una opción: ").strip()
        if op == "1":
            ver_banos()
        elif op == "2":
            ver_biblioteca()
        elif op == "3":
            print("¡Adiós estudiante!")
            break
        else:
            print("Opción no válida.")

def menu_personal():
    while True:
        print("\n===== SERVICIOS DEL CAMPUS (UVG – Personal) =====")
        print("1) Marcar baño (en limpieza / disponible)")
        print("2) Actualizar biblioteca")
        print("3) Salir")
        op = input("Elige una opción: ").strip()
        if op == "1":
            marcar_bano()
        elif op == "2":
            actualizar_biblioteca()
        elif op == "3":
            print("¡Adiós personal!")
            break
        else:
            print("Opción no válida.")

def menu():
    print("Bienvenido al sistema de servicios del campus UVG")
    while True:
        print("\n¿Eres estudiante o personal?")
        print("1) Estudiante")
        print("2) Personal")
        print("3) Salir")
        rol = input("Selecciona tu rol: ").strip()
        if rol == "1":
            menu_estudiante()
        elif rol == "2":
            menu_personal()
        elif rol == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()

