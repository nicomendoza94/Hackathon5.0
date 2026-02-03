"""
Paquete de datos del juego.

Responsabilidad:
- Cargar NPCs desde JSON
- Cargar tareas desde JSON
- Proveer datos a los sistemas
"""
import json
import os
from entities.task import Task
from entities.npc import NPC

def load_tasks():
    """
    Carga las tareas desde data/tasks.json
    
    Returns:
        Lista de objetos Task
    """
    try:
        path = os.path.join("data", "tasks.json")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        tasks_list = []
        
        # El JSON tiene una clave "tasks" con una lista
        for task_data in data.get("tasks", []):
            task = Task(
                name=task_data["name"],
                x=task_data["x"],
                y=task_data["y"],
                task_type=task_data["task_type"],
                difficulty=task_data.get("difficulty", 1)
            )
            tasks_list.append(task)
        
        print(f"✅ Cargadas {len(tasks_list)} tareas desde {path}")
        return tasks_list
    
    except FileNotFoundError:
        print(f"⚠️ No se encontró data/tasks.json. Usando lista vacía.")
        return []
    except Exception as e:
        print(f"❌ Error al cargar tareas: {e}")
        return []

def load_npcs():
    """
    Carga los NPCs desde data/npcs.json
    
    Returns:
        Lista de objetos NPC
    """
    try:
        path = os.path.join("data", "npcs.json")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        npcs_list = []
        
        # El JSON tiene una clave "npcs" con una lista
        for npc_data in data.get("npcs", []):
            npc = NPC(
                name=npc_data["name"],
                x=npc_data["x"],
                y=npc_data["y"]
            )
            # Asignar si es impostor (viene del JSON)
            npc.is_impostor = npc_data.get("is_impostor", False)
            npcs_list.append(npc)
        
        print(f"✅ Cargados {len(npcs_list)} NPCs desde {path}")
        return npcs_list
    
    except FileNotFoundError:
        print(f"⚠️ No se encontró data/npcs.json. Usando lista vacía.")
        return []
    except Exception as e:
        print(f"❌ Error al cargar NPCs: {e}")
        return []