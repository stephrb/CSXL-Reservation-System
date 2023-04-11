import pytest

from sqlalchemy.orm import Session
from ...models import User, Reservation, Reservable, PaginationParams, Paginated
from ...entities import UserEntity, RoleEntity, PermissionEntity, ReservableEntity, ReservationEntity
from ...services import ReservationService, ReservableService
from datetime import datetime, timedelta

# Mock Models
root = User(id = 1, pid=99999999, onyen='root', email='root@unc.edu')
student = User(id=2, pid=111111111, onyen='sol',
                  email='sol@unc.edu')

reservable = Reservable(id=1, name='Laptop #1', type='Laptop', description='The first laptop')
reservable_2 = Reservable(id=2, name='Room #1', type='Room', description='Small study room, adjacent to entrance')

time = datetime.now() + timedelta(days = 1)
start_time = time.replace(hour=15, minute=0, second=0, microsecond=0)
reservation = Reservation(id=1, start_time=start_time, end_time=start_time + timedelta(hours=3))

start_time_2 = time + timedelta(days = 1)
reservation_2 = Reservation(id=2, start_time=start_time_2, end_time=start_time_2 + timedelta(hours=3))

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    root_entity = UserEntity.from_model(root)
    test_session.add(root_entity)
    student_entity = UserEntity.from_model(student)
    test_session.add(student_entity)
    reservable_entity = ReservableEntity.from_model(reservable)
    test_session.add(reservable_entity)
    reservable_entity_2 = ReservableEntity.from_model(reservable_2)
    test_session.add(reservable_entity_2)
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
def reservable_service(test_session: Session):
    return ReservableService(test_session)

def test_list_reservable(reservable_service: ReservableService):
    assert reservable_service.list_reservables() == [reservable, reservable_2]