import json
from entities.npc import NPC
def load_npcs(path="data/npcs.json"):
 
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        NPC(
            npc_id=n["id"],
            name=n["name"],
            x=n["x"],
            y=n["y"],
            is_impostor=n["is_impostor"]
        )
        for n in data
    ]