import pytest

from sqlalchemy import text
from sqlalchemy.orm import Session
from ...models import User, Reservation, Reservable, PaginationParams, Paginated, ReservableForm
from ...entities import UserEntity, RoleEntity, PermissionEntity, ReservableEntity, ReservationEntity
from ...services import ReservationService, ReservableService
from datetime import datetime, timedelta

# Mock Models

reservable = Reservable(id=1, name='Laptop #1', type='Laptop', description='The first laptop')
reservable_2 = Reservable(id=2, name='Room #1', type='Room', description='Small study room, adjacent to entrance')
reservable_3 = ReservableForm(name='Laptop #2', type='Laptop', description='The second laptop')
reservable_3_true = Reservable(id=3, name='Laptop #2', type='Laptop', description='The second laptop')

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    reservable_entity = ReservableEntity.from_model(reservable)
    test_session.add(reservable_entity)
    reservable_entity_2 = ReservableEntity.from_model(reservable_2)
    test_session.add(reservable_entity_2)
    test_session.commit()
    test_session.execute(text(f'ALTER SEQUENCE {ReservableEntity.__table__}_id_seq RESTART WITH {3}'))
    yield

@pytest.fixture()
def reservable_service(test_session: Session):
    return ReservableService(test_session)

def test_list_reservable(reservable_service: ReservableService):
    assert reservable_service.list_reservables() == [reservable, reservable_2]

def test_delete_reservable(reservable_service: ReservableService):
    reservable_service.delete_reservable(2)
    assert reservable_service.list_reservables() == [reservable]

def test_delete_all_reservables(reservable_service: ReservableService):
    reservable_service.delete_reservable(1)
    reservable_service.delete_reservable(2)
    assert reservable_service.list_reservables() == []

def test_add_reservable(reservable_service: ReservableService):
    reservable_service.add_reservable(reservable_3)
    assert reservable_service.list_reservables() == [reservable, reservable_2, reservable_3_true]