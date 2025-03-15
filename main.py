from flask import Flask, request, jsonify, abort, render_template
from models import db, Estudiante
import connexion

# Instanciamos la aplicación
app = Flask(__name__)


# Configuramos el acceso a la base de datos SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api_developer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Iniciamos la aplicación
db.init_app(app)

# Creamos la base de datos de acuerdo al modelo
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template('home.html')
    


# Método GET – lista de estudiantes
@app.route('/estudiantes', methods=['GET'])
def get_estudiantes():
    estudiantes = Estudiante.query.all()
    return jsonify([{'id': estudiante.id, 
                     'nombres': estudiante.nombres, 
                     'apellido_paterno': estudiante.apellido_paterno, 
                     'apellido_materno': estudiante.apellido_materno, 
                     'email': estudiante.email} for estudiante in estudiantes])
    
# Método GET <id> - estudiante por id
@app.route('/estudiantes/<int:id>', methods=['GET'])
def get_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    return jsonify({'id': estudiante.id, 
                    'nombres': estudiante.nombres, 
                    'apellido_paterno': estudiante.apellido_paterno, 
                    'apellido_materno': estudiante.apellido_materno, 
                    'email': estudiante.email})
    
# Método POST – crear estudiante nuevo 
@app.route('/estudiantes', methods=['POST'])
def create_estudiante():
    if not request.json or not 'nombres' in request.json or not 'apellido_paterno' in request.json or not 'apellido_materno' in request.json:
        abort(400, description="Bad Request: Hacen falta campos obligatorios")
    data = request.get_json()
    new_estudiante = Estudiante(
        nombres=data['nombres'],
        apellido_paterno=data['apellido_paterno'],
        apellido_materno=data['apellido_materno'],
        email=data['email']
    )
    db.session.add(new_estudiante)
    db.session.commit()
    return jsonify({'id': new_estudiante.id, 
                    'nombres': new_estudiante.nombres, 
                    'apellido_paterno': new_estudiante.apellido_paterno, 
                    'apellido_materno': new_estudiante.apellido_materno,
                    'email': new_estudiante.email}), 201

# Método PUT <id> - actualizar estudiante 
@app.route('/estudiantes/<int:id>', methods=['PUT'])
def update_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    if not request.json:
        abort(400, description="Bad Request: Hace falta el cuerpo(body) de la solicitud")
    data = request.get_json()
    if 'nombres' in data and type(data['nombres']) is not str:
        abort(400, description="Bad Request: Nombres debe ser de tipo string")
    if 'apellido_paterno' in data and type(data['apellido_paterno']) is not str:
        abort(400, description="Bad Request: Apellido Paterno debe ser de tipo string")
    if 'apellido_materno' in data and type(data['apellido_materno']) is not str:
        abort(400, description="Bad Request: Apellido Materno debe ser de tipo string")
    if 'email' in data and data['email'] is not None and type(data['email']) is not str:
        abort(400, description="Bad Request: Email debe ser de tipo string con formato de correo")
    estudiante.nombres = data.get('nombres', estudiante.nombres)
    estudiante.apellido_paterno = data.get('apellido_paterno', estudiante.apellido_paterno)
    estudiante.apellido_materno = data.get('apellido_materno', estudiante.apellido_materno)
    estudiante.email = data.get('email', estudiante.email)
    db.session.commit()
    return jsonify({'id': estudiante.id, 
                    'nombres': estudiante.nombres, 
                    'apellido_paterno': estudiante.apellido_paterno, 
                    'apellido_materno': estudiante.apellido_materno, 
                    'email': estudiante.email})

# Método DELETE <>id – eliminar estudiante
@app.route('/estudiantes/<int:id>', methods=['DELETE'])
def delete_estudiante(id):
    estudiante = Estudiante.query.get_or_404(id)
    db.session.delete(estudiante)
    db.session.commit()
    return jsonify({'message': 'Estudiante eliminado correctamente'}), 204

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': 'Recurso no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)