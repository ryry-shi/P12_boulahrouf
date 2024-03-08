import os
from unittest.mock import MagicMock
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Collaborator, Contract, EpicClient, Event
from models import Base


engine = create_engine(f"{os.getenv("PROTOCOL")}://{os.getenv("USERNAME")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}/test")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()
current_user = None


@pytest.fixture(autouse=True)
def monkeypatch_read(monkeypatch):
    monkeypatch.setattr("models.read", lambda key: session if key == "session" else current_user)


@pytest.fixture(autouse=True)
def monkeypatch_create_or_update(monkeypatch):
    def create_or_update_mocked(obj):
        session.add(obj)
        session.commit()
    monkeypatch.setattr("models.create_or_update", create_or_update_mocked)


@pytest.fixture(autouse=True)
def monkeypatch_get_permission_from_affiliation(monkeypatch):
    monkeypatch.setattr("models.Collaborator.get_permission_from_affiliation", lambda x: {1: "commercial", 2: "support", 3: "gestion"}[x])


def test_create_collaborator(monkeypatch):
    # Mocks
    mock_get_permission_from_affiliation = MagicMock()
    mock_get_permission_from_affiliation.return_value = 3
    monkeypatch.setattr("models.Collaborator.get_permission_from_affiliation", mock_get_permission_from_affiliation)
    # Création d'un utilisateur
    gestionnaire = Collaborator.create(
        name="test",
        password="passwordtest",
        email="test@test.fr",
        affiliation=3
    )

    assert gestionnaire.name is not None
    assert type(gestionnaire) == Collaborator
    assert gestionnaire.name == "test"
    assert gestionnaire.email == "test@test.fr"
    assert gestionnaire.affiliation == 3

    # Assurez-vous que la méthode create_or_update a été appelée avec le collaborateur créé
    assert len(list(session.query(Collaborator).all())) == 1


def test_update_collaborator(monkeypatch):
    # création du collaborateur
    collaborator = Collaborator(name="John Doe", password="password", email="john@example.com", affiliation=2, permission="support")
    session.add(collaborator)
    session.commit()
    # Mock
    mock_get_by_email = MagicMock()
    mock_get_by_email.return_value = collaborator
    monkeypatch.setattr("models.Collaborator.get_by_email", mock_get_by_email)
    # MAJ
    collaborator = Collaborator.update("john@example.com", "doe", "aaaaaaaaaa", "doe@example.com", 3)
    session.add(collaborator)
    session.commit()
    # Tests
    assert collaborator is not None
    assert type(collaborator) == Collaborator
    in_base_collaborator = session.query(Collaborator).filter(Collaborator.email == "doe@example.com")[0]
    assert collaborator == in_base_collaborator
    assert collaborator.name == "doe"
    assert collaborator.affiliation == 3


def test_str_collaborator(mocker):
    collaborator_mock = Collaborator(name="Antoine", email="antoine@example.com", affiliation=2, permission="support")
    mocker.patch("models.Collaborator.get_by_email", return_value=collaborator_mock)
    assert str(collaborator_mock) == f"Collaborator: {collaborator_mock.id} | {collaborator_mock.name} | {collaborator_mock.email} | {collaborator_mock.affiliation} | {collaborator_mock.permission}"


def test_repr_collaborator(mocker):
    collaborator_mock = Collaborator(name="Antoine", email="antoine@example.com", affiliation=2, permission="support")
    mocker.patch("models.Collaborator.get_by_email", return_value=collaborator_mock)
    assert str(collaborator_mock) == f"Collaborator: {collaborator_mock.id} | {collaborator_mock.name} | {collaborator_mock.email} | {collaborator_mock.affiliation} | {collaborator_mock.permission}"

    
def test_get_by_name_collaborator():
    # création du collaborateur
    created_collaborator = Collaborator(name="Johntest", password="Johntest", email="Johntest@example.com", affiliation=2, permission="support")
    session.add(created_collaborator)
    session.commit()
    # fonction
    collaborator = Collaborator.get_by_name(created_collaborator.name)
    # asserts
    assert collaborator == created_collaborator


def test_get_by_email_collaborator():
    # création du collaborateur
    created_collaborator = Collaborator(name="Joaaaaaaaaaaahntest", password="Joaaaaaahntest", email="Johntesaaaaaaaat@example.com", affiliation=2, permission="support")
    session.add(created_collaborator)
    session.commit()
    # fonction
    collaborator = Collaborator.get_by_email(created_collaborator.email)
    assert collaborator.email == "Johntesaaaaaaaat@example.com"
    
    
def test_create_epic():
    name = "John Doee"
    email = "john.doe@edadadaple.com"
    phone = "0103030405"
    entreprise = "john.doe@eaxaaaaaaaample.com"
    creation_date = "2000-10-10"
    contact_id = 1
    client = EpicClient.create(name, email, phone, entreprise, creation_date, contact_id)
    session.add(client)
    session.commit()
    assert len(list(session.query(EpicClient).filter_by(email=email))) == 1


def test_create_contract():
    epic_client = 1
    contact_id = 2
    amount = 50
    remaining_amount = 0
    creation_date = "2000-10-10"
    contract = Contract.create(epic_client, contact_id, amount, remaining_amount, creation_date)
    session.add(contract)
    session.commit()
    assert len(list(session.query(EpicClient).filter_by(creation_date=creation_date))) == 1


def test_update_epic(monkeypatch):
    # création du collaborateur
    collaborator = Collaborator(name="johntestpass", password="johntestpass", email="johntesttest@example.com", affiliation=1, permission="commercial")
    session.add(collaborator)
    session.commit()
    # création du client
    client = EpicClient(name="John Doetest", email="johnnew@example.com", phone="0201030409", entreprise="johnentreprise", creation_date="2000-10-11", contact_id=collaborator.id)
    session.add(client)
    session.commit()
    # mocks
    mock_get_by_email = MagicMock()
    mock_get_by_email.return_value = client
    monkeypatch.setattr("models.Collaborator.get_by_email", mock_get_by_email)
    global current_user
    current_user = collaborator
    # function call
    client = EpicClient.update("johnnew@example.com", "doe", "doe@example.com", "0102030405", "star wars")
    session.add(client)
    session.commit()
    # Tests
    assert client is not None
    assert type(client) == EpicClient
    in_base_client = session.query(EpicClient).filter(EpicClient.email == client.email)[0]
    
    assert client == in_base_client


def test_create_event(monkeypatch):
    # creation du collaborateur support
    commercial = Collaborator(name="commercial", password="password123456!", email="commercial@example.com", affiliation=2, permission="commercial")
    session.add(commercial)
    session.commit()
    # creation du client
    epic_client = EpicClient.create(
        name="Client",
        entreprise="entreprise",
        phone="0122030405",
        creation_date="2000-10-10",
        contact_id=commercial.id,
        email="client@example.com"
    )
    session.add(epic_client)
    session.commit()
    # # creation du contrat
    contract = Contract.create(epic_client.id, 1, 10, 0, "2009-10-10")
    session.add(contract)
    session.commit()
    # creation des mocks
    mock_contract_get_by_id = MagicMock()
    mock_contract_get_by_id.return_value = contract
    monkeypatch.setattr(Contract, "get_by_id", mock_contract_get_by_id)
    mock_client_get_by_id = MagicMock()
    mock_client_get_by_id.return_value = epic_client
    monkeypatch.setattr(EpicClient, "get_by_id", mock_client_get_by_id)
    # creation de l'évènement
    event = Event.create(
        contract_id=contract.id,
        event_start="2024-03-07",
        event_end="2024-03-08",
        location="Salle de réunion",
        attendes=10,
        notes="Meeting notes",
    )
    session.add(event)
    session.commit()
    # assertion
    assert event is not None
    assert type(event) == Event
    event_in_base = session.query(Event).get(event.id)
    assert event == event_in_base
    assert event.event_start.isoformat() == "2024-03-07T00:00:00"
    assert event.event_end.isoformat() == "2024-03-08T00:00:00"
    assert event.location == "Salle de réunion"
    assert event.attendes == 10
    assert event.notes == "Meeting notes"
