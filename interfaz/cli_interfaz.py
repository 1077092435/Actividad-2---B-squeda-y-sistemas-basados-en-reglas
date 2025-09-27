# Contiene el mapa de estaciones cargado en busqueda_grafo para mostrar nombres
from logica.busqueda_grafo import ESTACIONES_MAP

def solicitar_datos_usuario():
    """Solicita el origen, destino y preferencias del usuario."""
    
    print("--- 🗺️ SISTEMA INTELIGENTE DE RUTAS DE TRANSPORTE MASIVO 🚄 ---")
    
    print("\nEstaciones disponibles (Código - Nombre):")
    for codigo, data in ESTACIONES_MAP.items():
        accesibilidad = " (Accesible)" if data.get('accessible') else " (¡NO Accesible!)"
        print(f"  {codigo}: {data['nombre']}{accesibilidad}")

    # Solicitud de Origen y Destino
    while True:
        punto_a = input("\nIngrese el código de la ESTACIÓN DE ORIGEN: ").upper()
        if punto_a in ESTACIONES_MAP:
            break
        print("Código no válido. Intente de nuevo.")

    while True:
        punto_b = input("Ingrese el código de la ESTACIÓN DE DESTINO: ").upper()
        if punto_b in ESTACIONES_MAP and punto_b != punto_a:
            break
        elif punto_b == punto_a:
            print("El origen y el destino no pueden ser el mismo.")
        else:
            print("Código no válido. Intente de nuevo.")
            
    # Solicitud de Preferencias (Reglas Lógicas)
    while True:
        accesibilidad_input = input("¿Necesita una ruta completamente accesible? (S/N): ").upper()
        if accesibilidad_input in ('S', 'N'):
            requiere_accesibilidad = (accesibilidad_input == 'S')
            break
        print("Respuesta no válida. Por favor, ingrese 'S' o 'N'.")
        
    return punto_a, punto_b, requiere_accesibilidad

def presentar_resultados(ruta_detallada, costo_total, punto_a, punto_b):
    """Muestra la ruta y el costo total al usuario."""

    # Si no hay ruta (None)
    if ruta_detallada is None:
        print("\n--- RESULTADO DE LA RUTA INTELIGENTE 💡 ---")
        print("❌ ¡RUTA NO ENCONTRADA!")
        print(f"No fue posible encontrar una ruta entre {ESTACIONES_MAP[punto_a]['nombre']} y {ESTACIONES_MAP[punto_b]['nombre']} que cumpla con las reglas.")
        return

    print("\n--- RESULTADO DE LA RUTA INTELIGENTE 💡 ---")
    print(f"✅ ¡Ruta óptima encontrada!")
    print(f"Costo Total de la Ruta (Tiempo ajustado por Reglas): **{costo_total} unidades**.")
    print("\n--- DETALLE PASO A PASO ---")
    
    linea_actual = None
    transferencias = 0
    
    for i, tramo in enumerate(ruta_detallada):
        print(f"\nPASO {i+1}:")
        
        # Detección y reporte de Transferencia
        if linea_actual is not None and linea_actual != tramo['linea']:
            print(f"  ⚠️ **TRANSFERENCIA:** Cambie de Línea {linea_actual} a Línea {tramo['linea']} (Penalización: {tramo['penalizacion_reglas']})")
            transferencias += 1
            
        print(f"  ➡️ Salir de: **{tramo['origen_nom']}**")
        print(f"  🚌 Tomar Línea: **{tramo['linea']}**")
        print(f"  📍 Destino del tramo: **{tramo['destino_nom']}**")
        print(f"  ⏱️ Tiempo Base: {tramo['tiempo_base']} min. | Costo Ajustado: {tramo['costo_total_tramo']} unidades.")
        
        linea_actual = tramo['linea']

    print(f"\n--- RESUMEN FINAL ---")
    print(f"Origen: {ESTACIONES_MAP[punto_a]['nombre']}")
    print(f"Destino: {ESTACIONES_MAP[punto_b]['nombre']}")
    print(f"Total de Transferencias: {transferencias}")
    print(f"Costo Total (ajustado): {costo_total} unidades.")