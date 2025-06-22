import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from models.customer import Customer
from models.case import Case
from services.database import db
from datetime import datetime

class TestUserModel:
    """Tests para el modelo User."""
    
    def test_user_creation(self):
        """Test para crear un usuario."""
        user = User(
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password',
            preferred_language='es'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.preferred_language == 'es'
        assert user.is_active == True
    
    def test_user_repr(self):
        """Test para la representación del usuario."""
        user = User(username='testuser', email='test@example.com', password_hash='hash')
        assert str(user) == '<User testuser>'

class TestCustomerModel:
    """Tests para el modelo Customer."""
    
    def test_customer_creation(self):
        """Test para crear un cliente."""
        customer = Customer(
            name='Juan Pérez',
            email='juan@example.com',
            phone='123456789'
        )
        assert customer.name == 'Juan Pérez'
        assert customer.email == 'juan@example.com'
        assert customer.phone == '123456789'
    
    def test_customer_relationships(self):
        """Test para las relaciones del cliente."""
        customer = Customer(name='Test Customer', email='test@example.com')
        assert hasattr(customer, 'cases')

class TestCaseModel:
    """Tests para el modelo Case."""
    
    def test_case_creation(self):
        """Test para crear un caso."""
        case = Case(
            title='Test Case',
            description='Test Description',
            status='abierto',
            customer_id=1,
            user_id=1
        )
        assert case.title == 'Test Case'
        assert case.description == 'Test Description'
        assert case.status == 'abierto'
        assert case.customer_id == 1
        assert case.user_id == 1
    
    def test_case_timestamps(self):
        """Test para los timestamps del caso."""
        case = Case(title='Test Case', customer_id=1, user_id=1)
        assert case.created_at is not None
        assert case.updated_at is not None
    
    def test_case_repr(self):
        """Test para la representación del caso."""
        case = Case(title='Test Case', customer_id=1, user_id=1)
        assert str(case) == '<Case Test Case>'

class TestModelRelationships:
    """Tests para las relaciones entre modelos."""
    
    def test_customer_case_relationship(self):
        """Test para la relación cliente-caso."""
        customer = Customer(name='Test Customer', email='test@example.com')
        case = Case(title='Test Case', customer_id=1, user_id=1)
        
        # Simular la relación
        case.customer = customer
        assert case.customer.name == 'Test Customer'
    
    def test_user_case_relationship(self):
        """Test para la relación usuario-caso."""
        user = User(username='testuser', email='test@example.com', password_hash='hash')
        case = Case(title='Test Case', customer_id=1, user_id=1)
        
        # Simular la relación
        case.user = user
        assert case.user.username == 'testuser'

if __name__ == "__main__":
    pytest.main([__file__]) 