import logging
from flask import Flask, jsonify
from flask_cors import CORS
try:
    from config.settings import settings
except ModuleNotFoundError:
    import sys, os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from config.settings import settings
from services.database import db
from services.cache import redis_client
from config.logging import setup_logging
from api.routes import api_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = settings.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
CORS(app)
db.init_app(app)

# Importar modelos para que SQLAlchemy los registre
import models.user
import models.customer
import models.case

setup_logging()
logging.info('LegisLink API iniciada')

app.register_blueprint(api_bp)

@app.route('/api/health', methods=['GET'])
def health_check():
    logging.info('Chequeo de salud solicitado')
    return jsonify({"status": "ok"}), 200

@app.route('/api/redis-test', methods=['GET'])
def redis_test():
    try:
        redis_client.set('test_key', 'hello_redis')
        value = redis_client.get('test_key')
        logging.info(f'Valor leído de Redis: {value}')
        return jsonify({'redis_value': value}), 200
    except Exception as e:
        logging.error(f'Error en Redis: {e}')
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
