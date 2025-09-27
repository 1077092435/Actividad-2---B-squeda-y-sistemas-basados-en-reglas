import json
import os

# Cargar la configuración de las reglas y datos estáticos
RUTA_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(RUTA_BASE, 'datos', 'reglas_config.json'), 'r') as f:
    CONFIG = json.load(f)

PENALIZACION_INACCESIBILIDAD = float('inf')
COSTO_TRANSFERENCIA = CONFIG['COSTO_TRANSFERENCIA']
COSTO_PENALIZACION_CONGESTION = CONFIG['COSTO_PENALIZACION_CONGESTION']
LINEAS_CONGESTIONADAS = set(CONFIG['LINEAS_CONGESTIONADAS'])

def peso_con_reglas(u, v, data, estaciones_map, requiere_accesibilidad):
    costo = data.get('tiempo_transito', 0)
    
    if requiere_accesibilidad and not estaciones_map.get(v, {}).get('accessible', True):
        return PENALIZACION_INACCESIBILIDAD
        
    # 2. Regla de Congestión (Regla de Optimización/Penalización)
    if data.get('linea') in LINEAS_CONGESTIONADAS:
        costo += COSTO_PENALIZACION_CONGESTION
        
    return costo

def calcular_penalizacion_transferencia(linea_anterior, linea_actual):
    if linea_anterior is not None and linea_anterior != linea_actual:
        return COSTO_TRANSFERENCIA
    return 0