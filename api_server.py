# api_server.py - Servidor API separado para el bot
from flask import Flask, request, jsonify
import threading
import time

app = Flask(__name__)

# Simulación de datos (usa tus funciones reales)
def simular_mantenimiento(equipo, horas_uso):
    """Función de simulación - adapta con tu lógica real"""
    return {
        'condicion': 'Óptima',
        'vida_util': '85%',
        'recomendacion': 'Mantenimiento preventivo en 30 días',
        'equipo': equipo,
        'horas_uso': horas_uso
    }

@app.route('/simulate', methods=['POST'])
def api_simulate():
    """Endpoint para el bot de Telegram"""
    try:
        data = request.get_json()
        
        resultado = simular_mantenimiento(
            data.get('equipo', 'motor_principal'),
            data.get('horas_uso', 500)
        )
        
        resultado['usuario'] = data.get('telegram_user', 'anonimo')
        resultado['status'] = 'success'
        
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar que el API está funcionando"""
    return jsonify({'status': 'active', 'service': 'maintenance-api'})

def run_api_server():
    """Ejecuta el servidor API en un hilo separado"""
    print("🚀 Starting API server on http://localhost:5001")
    app.run(host='0.0.0.0', port=5001, debug=False, use_reloader=False)

# Ejecutar solo si se llama directamente
if __name__ == '__main__':
    run_api_server()
    python api_server.py
