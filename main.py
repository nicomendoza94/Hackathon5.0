import pygame
import sys
import json
import os
import random

from ui.menu import Menu
from ui.hud import HUD
from ui.meeting import Meeting

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 1280, 720
FPS = 60

# --- FUNCIONES DE DATA (Tu Rol: Jeremy) ---

def cargar_datos_json(ruta):
    """Carga datos de forma segura desde la carpeta data [cite: 124-127]."""
    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return [] if "npcs" in ruta else {}
    return [] if "npcs" in ruta else {}

def asignar_roles_aleatorios(lista_npcs):
    """Asigna roles por probabilidad: 30% Impostor / 70% Ciudadano ."""
    for npc in lista_npcs:
        npc["is_impostor"] = False

    if random.randint(1, 100) <= 30:
        rol_jugador = "Impostor"
    else:
        rol_jugador = "Ciudadano"
        if lista_npcs:
            random.choice(lista_npcs)["is_impostor"] = True
            
    return rol_jugador, lista_npcs

def guardar_puntaje(nombre, puntos, rol, victoria=False):
    """Guarda la persistencia del nivel y resultado [cite: 71-75]."""
    ruta = "data/scores.json"
    datos = cargar_datos_json(ruta)
    if not datos or not isinstance(datos, dict):
        datos = {"high_scores": [], "total_games_played": 0}

    nueva_entrada = {
        "player": nombre,
        "points": puntos,
        "date": "2026-02-03",
        "role": rol,
        "victory": victoria,
        "level_reached": 1
    }

    datos["high_scores"].append(nueva_entrada)
    datos["total_games_played"] += 1
    datos["high_scores"] = sorted(datos["high_scores"], key=lambda x: x["points"], reverse=True)[:10]

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4)

# --- BUCLE PRINCIPAL ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("El Impostor en el Congreso - Hackathon 5.0")
    clock = pygame.time.Clock()

    menu_vista = Menu(screen)
    hud_vista = HUD(screen)
    meeting_vista = Meeting(screen)

    npcs_base = cargar_datos_json("data/npcs.json")
    datos_completos = cargar_datos_json("data/tasks.json")
    lista_tareas = datos_completos.get("tasks", [])
    lista_sabotajes = datos_completos.get("sabotages", [])

    estado = "MENU"
    role = "Ciudadano"
    score = 0
    timer = 300
    progress = 0.0
    tarea_actual_idx = 0
    selected_npc_idx = 0
    npcs_partida = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                # 1. CAMBIO: Comenzar juego con ESPACIO en lugar de '2' 
                if estado == "MENU" and event.key == pygame.K_SPACE:
                    role, npcs_partida = asignar_roles_aleatorios(list(npcs_base))
                    estado = "PLAYING"
                
                # 2. SALIR al menú con ESCAPE
                if event.key == pygame.K_ESCAPE: 
                    estado = "MENU"
                
                # 3. INTERACCIÓN (Solo Ciudadano)
                if estado == "PLAYING" and role == "Ciudadano" and event.key == pygame.K_e:
                    progress += 0.25
                    if progress >= 1.0:
                        progress = 0.0
                        score += lista_tareas[tarea_actual_idx].get("value", 10)
                        tarea_actual_idx = (tarea_actual_idx + 1) % len(lista_tareas)

                # 4. VOTACIÓN con ENTER [cite: 62]
                if estado == "MEETING" and event.key == pygame.K_RETURN:
                    elegido = npcs_partida[selected_npc_idx]
                    es_victoria = elegido["is_impostor"]
                    guardar_puntaje("Jeremy", score, role, es_victoria)
                    estado = "MENU"

                # 5. NAVEGACIÓN EN REUNIÓN
                if estado == "MEETING":
                    if event.key == pygame.K_DOWN:
                        selected_npc_idx = (selected_npc_idx + 1) % len(npcs_partida)
                    if event.key == pygame.K_UP:
                        selected_npc_idx = (selected_npc_idx - 1) % len(npcs_partida)

        # LÓGICA DE TIEMPO
        if estado == "PLAYING":
            if timer > 0:
                timer -= 1/FPS
                
                # REUNIÓN AUTOMÁTICA: Cada 60 segundos (opcional para el PDF) 
                # if int(timer) % 60 == 0 and int(timer) != 300:
                #     estado = "MEETING"

            else:
                guardar_puntaje("Jeremy", score, role)
                estado = "MENU"
                timer = 300

        # RENDERIZADO
        screen.fill((0, 0, 0))

        if estado == "MENU":
            menu_vista.draw()
            
        elif estado == "PLAYING":
            label_tarea = lista_tareas[tarea_actual_idx]["label"] if role == "Ciudadano" else ""
            hud_vista.draw(role, progress, int(timer), score, label_tarea, lista_sabotajes)
            
        elif estado == "MEETING":
            meeting_vista.draw(npcs_partida, selected_npc_idx)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()