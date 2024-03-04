import pytest
from models import Collaborator, EpicClient

def test_create_collaborator(mocker):
    # Mock la méthode create de Collaborator
    mocker.patch.object(Collaborator, 'create')

    # Appel de la méthode create
    Collaborator.create(name='John', email='john@example.com', password='password', affiliation=1)

    # Vérification que la méthode create a été appelée avec les bons arguments
    Collaborator.create.assert_called_once_with(name='John', email='john@example.com', password='password', affiliation=1)
    
def test_update_collaborator(mocker):
    # Mock la méthode get_by_email pour retourner un collaborateur fictif
    mocker.patch.object(Collaborator, 'get_by_email', return_value=mocker.Mock())

    # Mock la fonction get_register_form pour retourner des données fictives
    mocker.patch('models.get_register_form', return_value={
        'name': 'John Doe',
        'password': 'password123',
        'email': 'john.doe@example.com',
        'affiliation': 3,
    })

    # Mock la session SQLAlchemy
    mock_session = mocker.Mock()
    mocker.patch('models.read', return_value=mock_session)

    # Appel de la méthode update avec une adresse e-mail fictive
    Collaborator.update(email='john.doe@example.com')

    # Vérification que la méthode get_by_email a été appelée avec les bons arguments
    Collaborator.get_by_email.assert_called_once_with('john.doe@example.com')

    # Vérification que la méthode add et commit de la session ont été appelées
    assert mock_session.add.called
    assert mock_session.commit.called
    
def test_delete_collaborator(mocker):
    mocker.patch.object(Collaborator, 'get_by_email', return_value=mocker.Mock())

    # Mock la fonction get_register_form pour retourner des données fictives
    mocker.patch('models.get_register_form', return_value={
        'name': 'John Doe',
        'password': 'password123',
        'email': 'john.doe@example.com',
        'affiliation': 3,
    })

    # Mock la session SQLAlchemy
    mock_session = mocker.Mock()
    mocker.patch('state.read', return_value=mock_session)

    # Appel de la méthode update avec une adresse e-mail fictive
    Collaborator.delete(email='john.doe@example.com')

    # Vérification que la méthode get_by_email a été appelée avec les bons arguments
    Collaborator.get_by_email.assert_called_once_with('john.doe@example.com')

    # Vérification que la méthode add et commit de la session ont été appelées
    assert mock_session.add.called
    assert mock_session.commit.called