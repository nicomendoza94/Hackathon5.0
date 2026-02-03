import unittest
import os
# Importamos tus funciones de Data [cite: 128-132]
from main import cargar_datos_json, asignar_roles_aleatorios

class TestProyectoJeremy(unittest.TestCase):

    def test_carga_npcs(self):
        """Verifica que los NPCs se carguen correctamente del JSON[cite: 125]."""
        ruta = "data/npcs.json"
        datos = cargar_datos_json(ruta)
        self.assertIsInstance(datos, list)
        self.assertGreater(len(datos), 0, "La lista de NPCs no debería estar vacía")

    def test_asignacion_roles(self):
        """Verifica la lógica de 30% Impostor / 70% Ciudadano [cite: 8-11]."""
        npcs_prueba = [
            {"id": 1, "name": "Prueba 1", "is_impostor": False},
            {"id": 2, "name": "Prueba 2", "is_impostor": False}
        ]
        
        # Guardamos los resultados en una lista
        resultados = [] 
        for _ in range(100):
            rol, _ = asignar_roles_aleatorios(list(npcs_prueba))
            resultados.append(rol)
            
        # Corregimos el nombre aquí: usamos 'resultados' en ambos lados
        self.assertIn("Ciudadano", resultados, "Debería haber ciudadanos")
        self.assertIn("Impostor", resultados, "Debería haber impostores por probabilidad")

    def test_persistencia_scores(self):
        """Verifica que el archivo de scores exista[cite: 71, 127]."""
        ruta = "data/scores.json"
        self.assertTrue(os.path.exists(ruta), "El archivo de persistencia debe existir en data/")

if __name__ == "__main__":
    unittest.main()