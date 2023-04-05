import pytest

from sqlalchemy.orm import Session
from ...models import User, Reservation, Reservable, PaginationParams, Paginated
from ...entities import UserEntity, RoleEntity, PermissionEntity, ReservableEntity, ReservationEntity
from ...services import ReservationService
from datetime import datetime, timedelta

# Mock Models
root = User(id = 1, pid=99999999, onyen='root', email='root@unc.edu')
student = User(id=2, pid=111111111, onyen='sol',
                  email='sol@unc.edu')

reservable = Reservable(id=1, name='Laptop #1', type='Laptop', description='The first laptop')

time = datetime.now() + timedelta(days = 1)
start_time = time.replace(hour=15, minute=0, second=0, microsecond=0)
reservation = Reservation(id=1, start_time=start_time, end_time=start_time + timedelta(hours=3))

start_time_2 = time + timedelta(days = 1)
reservation_2 = Reservation(id=2, start_time=start_time_2, end_time=start_time_2 + timedelta(hours=3))

pagination_params = PaginationParams(page=0, page_size=10, order_by='start_time', filter='')

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    root_entity = UserEntity.from_model(root)
    test_session.add(root_entity)
    student_entity = UserEntity.from_model(student)
    test_session.add(student_entity)
    reservable_entity = ReservableEntity.from_model(reservable)
    test_session.add(reservable_entity)
    reservation_entity = ReservationEntity.from_model(reservation)
    reservation_entity.reservable = reservable_entity
    reservation_entity.user = student_entity
    test_session.add(reservation_entity)
    reservation_entity_2 = ReservationEntity.from_model(reservation_2)
    reservation_entity_2.reservable = reservable_entity
    reservation_entity_2.user = student_entity
    test_session.add(reservation_entity_2)
    test_session.commit()
    yield

@pytest.fixture()
def reservation_service(test_session: Session):
    return ReservationService(test_session)

def test_single_reservation(reservation_service: ReservationService):
    assert reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=True).items[0] == reservation

def test_zero_reservations(reservation_service: ReservationService):
    assert len(reservation_service.list_user_reservations(user=root, pagination_params=pagination_params, upcoming=True).items) == 0

def test_reservation_history(reservation_service: ReservationService):
    assert len(reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=False).items) == 0

def test_reservation_order(reservation_service: ReservationService):
    res_list = reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=True).items
    assert res_list[0].start_time < res_list[1].start_time

def test_get_reservable(reservation_service: ReservationService):
    assert reservation_service.get_reservable(reservation.id) == reservable
    assert reservation_service.get_reservable(reservation_2.id) == reservable


def test_get_reservation(reservation_service: ReservationService):
    assert reservation_service.get_reservation(1) == reservation
    assert reservation_service.get_reservation(3) == None

def test_delete_reservation(reservation_service: ReservationService):
    assert reservation_service.get_reservation(2) == reservation_2
    reservation_service.delete_reservation(2)
    assert reservation_service.get_reservation(2) == None

def test_get_reservations_by_reservable(reservation_service: ReservationService):
    assert reservation_service.get_reservations_by_reservable(1, start_time) == [reservation]
    assert reservation_service.get_reservations_by_reservable(1, start_time_2) == [reservation_2]

def test_get_reservations_by_reservable_empty(reservation_service: ReservationService):
    assert reservation_service.get_reservations_by_reservable(1, start_time_2 + timedelta(days=1)) == []