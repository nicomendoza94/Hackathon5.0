# El Impostor en el Congreso (PY) 🇵🇾

Juego **single-player** hecho en **Python + Pygame** para hackathon.  
Inspirado en la idea de *“impostor vs tareas”*, ambientado en el **Congreso paraguayo** con un tono **humorístico y satírico**.

---

## 🎮 Gameplay

### 🎭 Roles

#### 🏛️ Diputado
- Vos hacés todas las tareas (minijuegos).
- Debés manejar **Estrés** y **Sospecha**.
- **Ganás** si completás todas las tareas antes de que termine el timer.

#### 🕵️ Impostor
- No podés hacer tareas.
- Los NPCs avanzan tareas automáticamente.
- Tu objetivo es **sabotear** para que no terminen a tiempo.
- **Perdés** si los NPCs completan todas las tareas.

---

## 🕹️ Controles

### Global
- **ESC**: volver al menú (desde cualquier pantalla)

### Diputado
- **WASD / Flechas**: moverse
- **E**: iniciar tarea (si estás cerca de una estación)
- **M**: reunión extraordinaria

### Impostor
- **WASD / Flechas**: moverse
- **1**: sabotaje Luces
- **2**: sabotaje Puertas
- **3**: sabotaje Comunicaciones  
*(Los sabotajes manuales tienen cooldown)*

---

## ⚠️ Sabotajes

- **Luces apagadas**  
  Reduce la velocidad de NPCs (más tensión).

- **Puertas bloqueadas**  
  Cierra pasos del mapa (nadie puede atravesarlos).

- **Comunicaciones caídas**
  - Oculta información de tareas en el HUD.
  - Impide iniciar tareas (solo Diputado).

📌 Los sabotajes automáticos ocurren cada **15s** (si existe impostor).  
😂 Los eventos graciosos aparecen cada **5s**.

---

## 🧠 Mecánicas principales

### Estrés (0–100)
- Sube por caos, sabotajes y efectos de NPCs.

### Sospecha (0–100)
- **Diputado**: sube con sabotajes activos.
- **Impostor**: sube si te acercás demasiado a NPCs  
  (puede disparar una *reunión automática*).

### 🗣️ Reunión extraordinaria (`M`)
- Opción 1: limpia sabotajes + baja **25 de estrés**
- Costo: **30s de tiempo**
- **ESC**: volver al juego

---

## ▶️ Cómo correr el juego

### Requisitos
- Python **3.10+** (recomendado **3.11**)
- Pygame

### Instalación
```bash
pip install pygame

Ejecutar
python main.py

🗂️ Estructura del proyecto
HACKATHON5.0/
├── main.py              # Entrada del juego
├── core/
│   ├── game.py          # Loop principal y reglas win/lose
│   ├── state_manager.py # Estados (MENU / PLAYING / MEETING / WIN / GAME_OVER)
│   └── clock.py         # Control de FPS y dt
├── entities/            # Player, NPC, Task, Sabotage
├── systems/             # Input, movimiento, IA, tareas, sabotajes
├── ui/                  # Menú, HUD, reunión
├── data/                # JSON de NPCs y tareas
└── assets/              # Imágenes y recursos

🧾 Datos (JSON)
NPCs

data/npcs.json define:

nombre

posición inicial

Tareas

data/tasks.json define:

nombre

tipo (task_type)

coordenadas

👉 Modificando estos JSON se puede ajustar el gameplay sin tocar código.

🖼️ Assets usados

assets/images/Fondo_menu_Jeremy.png — menú

assets/images/run_jeremy.png — reunión

assets/images/map_open.png / map_closed.png — mapas

assets/images/player.png / npc.png — sprites

🧪 Debug

F3: mostrar colliders de paredes y puertas (modo debug)

📌 Notas de balance

Cuando sos Impostor, los NPCs completan tareas con ritmo prudencial:

Máximo max_workers NPCs trabajando al mismo tiempo

Cada tarea tarda aprox. 35s – 50s por NPC

Las puertas tienen mayor probabilidad de sabotaje automático (weighted)
