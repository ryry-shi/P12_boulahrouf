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
    # Mock la fonction get_by_email pour retourner un collaborateur fictif
    mocker.patch('models.Collaborator.get_by_email', return_value=mocker.Mock())

    # Mock la fonction get_register_form pour retourner des données fictives
    mocker.patch('models.get_register_form', return_value={
        'name': 'John Doe',
        'password': 'password123',
        'email': 'john.doe@example.com',
        'affiliation': 1
    })

    # Mock la session SQLAlchemy
    mock_session = mocker.Mock()
    mocker.patch('models.read', return_value=mock_session)

    mocker.patch('misc.create_or_update', return_value=mock_session)

    # Appel de la méthode update avec une adresse e-mail fictive
    Collaborator.update(email='john.doe@example.com')

    # Vérification que la méthode get_by_email a été appelée avec les bons arguments
    Collaborator.get_by_email.assert_called_once_with(mock_session, 'john.doe@example.com')

    # Vérification que la méthode add et commit de la session ont été appelées
    assert mock_session.add.called
    assert mock_session.commit.called
    
# def test_delete_collaborator(mocker):
#     mocker.patch('models.Collaborator.get_by_email', return_value = mocker.Mock())
    
#     mocker.patch('models.get_register_form', return_value={
#         'name': 'John Doe',
#         'password': 'password123',
#         'email': 'john.doe@example.com',
#         'affiliation': 1
#     })
#     mock_session = mocker.Mock()
#     mocker.patch('models.read', return_value=mock_session)
#     Collaborator.delete(email='john.doe@example.com',)

# def test_create_epic_client(mocker):
#         # Mock la méthode create de Collaborator
#     mocker.patch.object(EpicClient, 'create')

#     # Appel de la méthode create
#     EpicClient.create(name='John', email='john@example.com', phone='0102030405', entreprise="johnentreprise",
#                       creation_date="2000-01-01")

#     # Vérification que la méthode create a été appelée avec les bons arguments
#     EpicClient.create.assert_called_once_with(name='John', email='john@example.com', phone='0102030405', entreprise="johnentreprise",
#                       creation_date="2000-01-01")
    
    
# def test_update_epic_clien (mocker):
#     # Mock la fonction get_by_email pour retourner un collaborateur fictif
#     mocker.patch('models.EpicClient.get_by_email', return_value=mocker.Mock())

#     # Mock la fonction get_register_form pour retourner des données fictives
#     mocker.patch('models.get_update_epic_client_form', return_value={
#         'name': 'John unknow',
#         'email': 'john@client.fr',
#         'phone': '0102030405',
#         'entreprise': 'joentreprise',
#         'contact_id': 1,
#     })

#     # Mock la session SQLAlchemy
#     mock_session = mocker.Mock()
#     mocker.patch('models.read', return_value=mock_session)

#     # Appel de la méthode update avec une adresse e-mail fictive
#     EpicClient.update(email='john@client.fr')

#     # Vérification que la méthode get_by_email a été appelée avec les bons arguments
#     EpicClient.get_by_email.assert_called_once_with(mock_session, 'john@client.fr')

#     # Vérification que la méthode add et commit de la session ont été appelées
#     assert mock_session.add.called
#     assert mock_session.commit.called
    
    
# def test_delete_epic(mocker):
#     mocker.patch('models.EpicClient.get_by_email', return_value={
#         mocker.Mock()
#     })

#     mocker.patch('forms.get_create_epic_client_form', return_value={
#         'name':'John',
#         'email':'john@client.com',
#         'phone':'0102030405',
#         'entreprise':"johnentreprise",
#         'creation_date':"2000-01-01",
#         'contact_id':1,
#         'last_update':"2005-10-10"
#     })
#     mock_session = mocker.Mock()
#     mocker.patch('models.read', return_value=mock_session)
#     EpicClient.delete(email='john@client.com')