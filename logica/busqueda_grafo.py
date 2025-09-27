import networkx as nx
from .motor_reglas import peso_con_reglas, calcular_penalizacion_transferencia
import json
import os

# Cargar datos de la red
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(RUTA_BASE, 'datos', 'red_estaciones.py'), 'r') as f:
    ESTACIONES_LIST = json.load(f)
with open(os.path.join(RUTA_BASE, 'datos', 'red_rutas.json'), 'r') as f:
    RUTAS_LINEAS = json.load(f)

# Convertir la lista de estaciones a un mapa (diccionario) para fácil acceso
ESTACIONES_MAP = {e['codigo']: e for e in ESTACIONES_LIST}

def crear_grafo_transporte():
    """Inicializa el grafo de la red de transporte usando NetworkX."""
    G = nx.DiGraph() 
    
    # Agregar nodos con atributos
    for estacion in ESTACIONES_LIST:
        G.add_node(estacion['codigo'], **estacion)
        
    # Agregar aristas con atributos
    for ruta in RUTAS_LINEAS:
        G.add_edge(ruta['origen'], ruta['destino'], **ruta)
        
    return G

def calcular_ruta_optima(G, punto_a, punto_b, requiere_accesibilidad):
    """
    Busca la ruta más corta (Dijkstra) usando un peso ajustado por reglas.
    Aplica la regla de transferencia en post-procesamiento.
    """
    
    # Función lambda para que NetworkX acceda a la función de peso inteligente
    weight_func = lambda u, v, d: peso_con_reglas(u, v, d, ESTACIONES_MAP, requiere_accesibilidad)

    try:
        # 1. Ejecutar Dijkstra con reglas de Arista-Dependencia (Accesibilidad, Congestión)
        ruta_corta = nx.shortest_path(G, source=punto_a, target=punto_b, weight=weight_func)
    except nx.NetworkXNoPath:
        # No se encontró ruta (ej. inaccesibilidad lo bloqueó)
        return None, None
        
    # 2. Post-Procesamiento para aplicar Regla de Transferencia (Ruta-Dependencia)
    tiempo_total = 0
    ruta_detallada = []
    linea_anterior = None
    
    for i in range(len(ruta_corta) - 1):
        u, v = ruta_corta[i], ruta_corta[i+1]
        data = G.get_edge_data(u, v)
        linea_actual = data.get('linea')
        
        costo_tramo_base = data.get('tiempo_transito', 0)
        
        # Penalizaciones de reglas
        penalizacion_transferencia = calcular_penalizacion_transferencia(linea_anterior, linea_actual)
        penalizacion_otra = weight_func(u, v, data) - costo_tramo_base # Recalcula congestión
        
        penalizacion_total = penalizacion_transferencia + penalizacion_otra
        costo_tramo_final = costo_tramo_base + penalizacion_total
        
        tiempo_total += costo_tramo_final
        linea_anterior = linea_actual
        
        ruta_detallada.append({
            'origen_cod': u, 'destino_cod': v,
            'origen_nom': ESTACIONES_MAP[u]['nombre'],
            'destino_nom': ESTACIONES_MAP[v]['nombre'],
            'linea': linea_actual,
            'tiempo_base': costo_tramo_base,
            'penalizacion_reglas': penalizacion_total,
            'costo_total_tramo': costo_tramo_final
        })
        
    return ruta_detallada, tiempo_total