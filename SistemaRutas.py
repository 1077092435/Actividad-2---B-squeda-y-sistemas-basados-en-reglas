import networkx as nx
from logica.busqueda_grafo import crear_grafo_transporte, calcular_ruta_optima
from interfaz.cli_interfaz import solicitar_datos_usuario, presentar_resultados

def main():
    """Función principal que orquesta la ejecución del sistema."""
    
    # 1. Cargar la red de transporte (el grafo)
    G = crear_grafo_transporte()
    
    # 2. Obtener la entrada del usuario
    punto_a, punto_b, requiere_accesibilidad = solicitar_datos_usuario()
    
    print("\n--- EJECUTANDO MOTOR DE INFERENCIA DE REGALAS ---")
    
    # 3. Calcular la ruta óptima aplicando todas las reglas lógicas
    ruta_detallada, costo_total = calcular_ruta_optima(G, punto_a, punto_b, requiere_accesibilidad)
    
    # 4. Presentar los resultados
    presentar_resultados(ruta_detallada, costo_total, punto_a, punto_b)

if __name__ == "__main__":
    main()