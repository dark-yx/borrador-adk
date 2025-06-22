from services.database import db
from models.customer import Customer
from models.case import Case
from typing import Dict, Any
from flask import current_app

def create_client(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un nuevo cliente en la base de datos.
    Requiere 'nombre' y 'email' en el diccionario de datos.
    """
    with current_app.app_context():
        nombre = datos.get('nombre')
        email = datos.get('email')
        if not nombre or not email:
            return {'error': 'Nombre y email son requeridos para crear un cliente.'}

        if Customer.query.filter_by(email=email).first():
            return {'error': f'Ya existe un cliente con el email {email}.'}

        try:
            cliente = Customer(name=nombre, email=email, phone=datos.get('phone'))
            db.session.add(cliente)
            db.session.commit()
            return {'mensaje': f'Cliente {nombre} creado exitosamente con ID {cliente.id}.'}
        except Exception as e:
            db.session.rollback()
            return {'error': 'Ocurrió un error en la base de datos.', 'detalle': str(e)}

def find_client(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Busca un cliente por su email.
    Requiere 'email' en el diccionario de datos.
    """
    with current_app.app_context():
        email = datos.get('email')
        if not email:
            return {'error': 'Se requiere un email para buscar al cliente.'}
        
        cliente = Customer.query.filter_by(email=email).first()
        if cliente:
            return {'id': cliente.id, 'nombre': cliente.name, 'email': cliente.email, 'phone': cliente.phone}
        else:
            return {'error': 'Cliente no encontrado.'}

def create_case(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Crea un nuevo caso para un cliente existente.
    Requiere 'email_cliente' y 'titulo' en el diccionario de datos.
    """
    with current_app.app_context():
        email_cliente = datos.get('email_cliente')
        titulo = datos.get('titulo')
        if not email_cliente or not titulo:
            return {'error': 'Email del cliente y título del caso son requeridos.'}

        cliente = Customer.query.filter_by(email=email_cliente).first()
        if not cliente:
            return {'error': 'Cliente no encontrado para asociar el caso.'}

        try:
            caso = Case(title=titulo, customer_id=cliente.id, status="Abierto")
            db.session.add(caso)
            db.session.commit()
            return {'mensaje': f'Caso "{titulo}" creado para {cliente.name} con ID {caso.id}.'}
        except Exception as e:
            db.session.rollback()
            return {'error': 'Ocurrió un error en la base de datos.', 'detalle': str(e)}

def find_case(datos: Dict[str, Any]) -> Dict[str, Any]:
    """
    Busca un caso por su ID.
    Requiere 'id_caso' en el diccionario de datos.
    """
    with current_app.app_context():
        id_caso = datos.get('id_caso')
        if not id_caso:
            return {'error': 'Se requiere un ID de caso para la búsqueda.'}
        
        caso = Case.query.get(id_caso)
        if caso:
            return {'id': caso.id, 'titulo': caso.title, 'status': caso.status, 'cliente': caso.customer.name}
        else:
            return {'error': 'Caso no encontrado.'} 