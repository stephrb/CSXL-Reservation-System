import pytest

from sqlalchemy import text
from sqlalchemy.orm import Session
from ...models import User, Reservation, Reservable, PaginationParams, Paginated, ReservableForm, Role
from ...entities import UserEntity, RoleEntity, PermissionEntity, ReservableEntity, ReservationEntity
from ...services import ReservationService, ReservableService, PermissionService, UserPermissionError
from datetime import datetime, timedelta

# Mock Models

reservable = Reservable(id=1, name='Laptop #1', type='Laptop', description='The first laptop')
reservable_2 = Reservable(id=2, name='Room #1', type='Room', description='Small study room, adjacent to entrance')
reservable_1_updated = Reservable(id=1, name='Room #2', type='Room', description='The second room')
reservable_2_updated = Reservable(id=2, name="Room #8", type='Room', description='THE 8th ROOM')
reservable_3 = ReservableForm(name='Laptop #2', type='Laptop', description='The second laptop')
reservable_3_true = Reservable(id=3, name='Laptop #2', type='Laptop', description='The second laptop')

root = User(id=1, pid=999999999, onyen='root', email='root@unc.edu')
root_role = Role(id=1, name='root')

user = User(id=3, pid=111111111, onyen='user', email='user@unc.edu')

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    root_user_entity = UserEntity.from_model(root)
    test_session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    test_session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action='reservable.*', resource='*', role=root_role_entity)
    test_session.add(root_permission_entity)

    reservable_entity = ReservableEntity.from_model(reservable)
    test_session.add(reservable_entity)
    reservable_entity_2 = ReservableEntity.from_model(reservable_2)
    test_session.add(reservable_entity_2)
    test_session.commit()
    test_session.execute(text(f'ALTER SEQUENCE {ReservableEntity.__table__}_id_seq RESTART WITH {3}'))

    user_entity = UserEntity.from_model(user)
    test_session.add(user_entity)

    test_session.commit()

    yield

@pytest.fixture()
def reservable_service(test_session: Session):
    return ReservableService(test_session, PermissionService(test_session))

def test_list_reservable(reservable_service: ReservableService):
    assert reservable_service.list_reservables() == [reservable, reservable_2]

def test_delete_reservable(reservable_service: ReservableService):
    reservable_service.delete(2, root)
    assert reservable_service.list_reservables() == [reservable]

def test_delete_all_reservables(reservable_service: ReservableService):
    reservable_service.delete(1, root)
    reservable_service.delete(2, root)
    assert reservable_service.list_reservables() == []

def test_add_reservable(reservable_service: ReservableService):
    reservable_service.add(reservable_3, root)
    assert reservable_service.list_reservables() == [reservable, reservable_2, reservable_3_true]

def test_add_with_permission_error(reservable_service: ReservableService):
    with pytest.raises(UserPermissionError):
        reservable_service.add(reservable_3, user)

def test_delete_with_permission_error(reservable_service: ReservableService):
    with pytest.raises(UserPermissionError):
        reservable_service.delete(2, user)

def test_update_reservable(reservable_service: ReservableService):
    reservable_service.update(reservable_1_updated)
    assert reservable_service.list_reservables() == [reservable_1_updated, reservable_2]

def test_update_reservable_order(reservable_service: ReservableService):
    reservable_service.update(reservable_2_updated)
    reservable_service.update(reservable_1_updated)
    assert reservable_service.list_reservables() == [reservable_1_updated, reservable_2_updated]

def test_filter_by_one_type(reservable_service: ReservableService):
    assert reservable_service.filter_by_type(["Room"]) == [reservable_2]

def test_filter_by_multiple_types(reservable_service: ReservableService):
    assert reservable_service.filter_by_type(["Laptop", "Room"]) == [reservable, reservable_2]

def test_filter_by_type_with_no_reservables(reservable_service: ReservableService):
    assert reservable_service.filter_by_type(["PC"]) == []

def test_get_types(reservable_service: ReservableService):
    assert reservable_service.get_types() == ['Room', 'Laptop']

def test_get_types_all_unique(reservable_service: ReservableService):
    reservable_service.add(reservable_3, root)
    assert reservable_service.get_types() == ['Room', 'Laptop']

