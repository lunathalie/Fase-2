# campus_uvg_interactivo_v2.py

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

PLAZAS = ["Plaza del CIT", "Plaza Paiz Rivera"]

# ----------------- Baños (generados) -----------------
banos = []
# CIT: 7 niveles; 4 baños por nivel (Izq-H, Izq-M, Der-H, Der-M)
for nivel in range(1, 8):
    banos.append({"id": f"CIT{nivel}-IZQ-H", "edificio": "CIT", "nivel": nivel, "lado": "Izq", "genero": "H", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-IZQ-M", "edificio": "CIT", "nivel": nivel, "lado": "Izq", "genero": "M", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-DER-H", "edificio": "CIT", "nivel": nivel, "lado": "Der", "genero": "H", "en_limpieza": False})
    banos.append({"id": f"CIT{nivel}-DER-M", "edificio": "CIT", "nivel": nivel, "lado": "Der", "genero": "M", "en_limpieza": False})
# Otros edificios: 2 baños (nivel 1): H y M
for edif in EDIFICIOS:
    if edif == "CIT":
        continue
    base = edif.replace(" ", "")
    banos.append({"id": f"{base}-H", "edificio": edif, "nivel": 1, "genero": "H", "en_limpieza": False})
    banos.append({"id": f"{base}-M", "edificio": edif, "nivel": 1, "genero": "M", "en_limpieza": False})

# ----------------- Docentes (dinámicos) -----------------
docentes = []  # {"nombre":..., "edificio":..., "oficina":..., "disponible":bool}

# ----------------- Biblioteca (solo HAY/NO HAY) -----------------
biblioteca = {"workspaces_hay": True, "ipads_hay": True}

# ----------------- Actividades (fechas DD-MM-YYYY) -----------------
actividades = []  # {"fecha": "DD-MM-YYYY", "plaza": ..., "titulo": ..., "hora": "HH:MM-HH:MM"}

# ----------------- Utilidades -----------------
def s_a_bool(s):
    return s.lower().strip() in ("s", "si", "sí")

def pedir_int(mensaje, default=None):
    txt = input(mensaje).strip()
    if txt == "" and default is not None:
        return default
    try:
        return int(txt)
    except:
        print("  Valor inválido, usando 0.")
        return 0

def asegurar_edificio(nombre):
    if nombre and nombre not in EDIFICIOS:
        EDIFICIOS.append(nombre)

def elegir_plaza():
    print("\nElige plaza:")
    for idx, pz in enumerate(PLAZAS, start=1):
        print(f"  {idx}) {pz}")
    op = input("Opción: ").strip()
    try:
        i = int(op) - 1
        if 0 <= i < len(PLAZAS):
            return PLAZAS[i]
    except:
        pass
    print("Opción inválida. Usando la primera plaza.")
    return PLAZAS[0]

def input_si_no(mensaje, default=None):
    txt = input(mensaje).strip().lower()
    if txt == "" and default is not None:
        return default
    return txt in ("s", "si", "sí")

# ----------------- BAÑOS: ver & actualizar -----------------
def ver_banos():
    print("\n--- BAÑOS ---")
    filtro = input("Filtrar por edificio (ENTER para todos, ej: CIT, Edificio F): ").strip()
    encontrados = [b for b in banos if (filtro == "" or b["edificio"].lower() == filtro.lower())]
    if not encontrados:
        print("No se encontraron baños con ese filtro.")
        return
    print("ID | Ubicación | Estado")
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
        print("No existe ese ID. Sugerencia: primero usa 'Ver baños' con filtro para encontrarlo.")
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

# ----------------- DOCENTES: ver & actualizar -----------------
def ver_docentes():
    print("\n--- DOCENTES ---")
    if not docentes:
        print("(No hay docentes cargados aún. Usa 'Agregar/actualizar docente'.)")
        return
    filtro = input("Filtrar por edificio (ENTER para todos): ").strip()
    encontrados = [d for d in docentes if (filtro == "" or d["edificio"].lower() == filtro.lower())]
    if not encontrados:
        print("No se encontraron docentes con ese filtro.")
        return
    print("Nombre | Ubicación | Estado")
    for d in encontrados:
        estado = "Disponible" if d["disponible"] else "Ocupado/No disponible"
        ubic = f"{d['edificio']} - Oficina {d['oficina']}"
        print(f"{d['nombre']} | {ubic} | {estado}")

def agregar_actualizar_docente():
    print("\n--- AGREGAR / ACTUALIZAR DOCENTE ---")
    nombre = input("Nombre del docente: ").strip()
    edif = input("Edificio (texto libre, ej: CIT, Edificio E, ...): ").strip()
    oficina = input("Oficina (ej: E-203): ").strip()
    disp = s_a_bool(input("¿Está disponible ahora? (si/no): "))

    asegurar_edificio(edif)

    existente = next((d for d in docentes if d["nombre"].lower() == nombre.lower()), None)
    if existente:
        existente["edificio"] = edif or existente["edificio"]
        existente["oficina"] = oficina or existente["oficina"]
        existente["disponible"] = disp
        print("Docente ACTUALIZADO.")
    else:
        docentes.append({
            "nombre": nombre if nombre else f"Docente {len(docentes)+1}",
            "edificio": edif if edif else "SIN-EDIF",
            "oficina": oficina if oficina else "SI/NO",
            "disponible": disp,
        })
        print("Docente AGREGADO.")

def marcar_docente():
    print("\n--- MARCAR ESTADO DE DOCENTE ---")
    if not docentes:
        print("(Aún no hay docentes. Usa 'Agregar/actualizar docente'.)")
        return
    nombre = input("Nombre del docente EXACTO (como aparece en la lista): ").strip()
    d = next((x for x in docentes if x["nombre"].lower() == nombre.lower()), None)
    if not d:
        print("No se encontró ese docente.")
        return
    print(f"Estado actual: {'Disponible' if d['disponible'] else 'Ocupado/No disponible'}")
    if input_si_no("¿Marcar DISPONIBLE? (si/no): "):
        d["disponible"] = True
        print("Marcado como DISPONIBLE.")
    elif input_si_no("¿Marcar OCUPADO/No disponible? (si/no): "):
        d["disponible"] = False
        print("Marcado como OCUPADO/No disponible.")
    else:
        print("Sin cambios.")

# ----------------- BIBLIOTECA: ver & actualizar (solo HAY/NO HAY) -----------------
def ver_biblioteca():
    print("\n--- BIBLIOTECA ---")
    ws_hay = biblioteca["workspaces_hay"]
    ip_hay = biblioteca["ipads_hay"]
    print(f"Workspaces: {'HAY' if ws_hay else 'NO HAY'}")
    print(f"iPads: {'HAY' if ip_hay else 'NO HAY'}")

def actualizar_biblioteca():
    print("\n--- ACTUALIZAR BIBLIOTECA ---")
    biblioteca["workspaces_hay"] = s_a_bool(input("¿Hay workspaces disponibles? (si/no): "))
    biblioteca["ipads_hay"] = s_a_bool(input("¿Hay iPads disponibles? (si/no): "))
    print("Biblioteca ACTUALIZADA.")

# ----------------- ACTIVIDADES: ver & agregar (DD-MM-YYYY) -----------------
def ver_actividades():
    print("\n--- ACTIVIDADES ---")
    if not actividades:
        print("No hay actividades registradas.")
        return
    print("Fecha (DD-MM-YYYY) | Plaza | Título | Hora")
    for a in actividades:
        print(f"{a['fecha']} | {a['plaza']} | {a['titulo']} | {a['hora']}")

def agregar_actividad():
    print("\n--- AGREGAR ACTIVIDAD ---")
    fecha = input("Fecha (DD-MM-YYYY): ").strip()
    plaza = elegir_plaza()
    titulo = input("Título: ").strip()
    hora = input("Hora (HH:MM-HH:MM): ").strip()
    actividades.append({"fecha": fecha, "plaza": plaza, "titulo": titulo, "hora": hora})
    print("Actividad AGREGADA.")

# ----------------- Menú principal -----------------
def menu():
    while True:
        print("\n===== SERVICIOS DEL CAMPUS (UVG – Interactivo v2) =====")
        print("1) Ver baños")
        print("2) Marcar baño (en limpieza / disponible)")
        print("3) Ver docentes")
        print("4) Agregar/actualizar docente")
        print("5) Marcar docente (disponible / ocupado)")
        print("6) Ver biblioteca (HAY/NO HAY)")
        print("7) Actualizar biblioteca (HAY/NO HAY)")
        print("8) Ver actividades (DD-MM-YYYY)")
        print("9) Agregar actividad (DD-MM-YYYY)")
        print("10) Salir")
        op = input("Elige una opción: ").strip()
        if op == "1":
            ver_banos()
        elif op == "2":
            marcar_bano()
        elif op == "3":
            ver_docentes()
        elif op == "4":
            agregar_actualizar_docente()
        elif op == "5":
            marcar_docente()
        elif op == "6":
            ver_biblioteca()
        elif op == "7":
            actualizar_biblioteca()
        elif op == "8":
            ver_actividades()
        elif op == "9":
            agregar_actividad()
        elif op == "10":
            print("¡Adiós!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu()
