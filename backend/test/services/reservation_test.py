import pytest
from sqlalchemy.orm import Session
from ...models import User, Reservation, Reservable, PaginationParams, Paginated, ReservationForm
from ...entities import UserEntity, RoleEntity, PermissionEntity, ReservableEntity, ReservationEntity
from ...services import ReservationService
from datetime import datetime, timedelta, timezone
from pydantic import ValidationError

# Mock Models
root = User(id = 1, pid=99999999, onyen='root', email='root@unc.edu')
student = User(id=2, pid=111111111, onyen='sol',
                  email='sol@unc.edu')

reservable = Reservable(id=1, name='Laptop #1', type='Laptop', description='The first laptop')

time = (datetime.now(timezone.utc) + timedelta(days = 1))

start_time = time.replace(hour=10, minute=0, second=0, microsecond=0)
reservation = ReservationForm(start_time=start_time, end_time=start_time + timedelta(hours=3), reservable_id=1)

start_time_2 = start_time + timedelta(days = 1)
reservation_2 = ReservationForm(start_time=start_time_2, end_time=start_time_2 + timedelta(hours=3), reservable_id=1)

pagination_params = PaginationParams(page=0, page_size=10, order_by='start_time', filter='')

@pytest.fixture(autouse=True)
def setup_teardown(test_session: Session):
    root_entity = UserEntity.from_model(root)
    test_session.add(root_entity)
    student_entity = UserEntity.from_model(student)
    test_session.add(student_entity)
    reservable_entity = ReservableEntity.from_model(reservable)
    test_session.add(reservable_entity)
    reservation_entity = ReservationEntity.from_form_model(reservation)
    reservation_entity.reservable = reservable_entity
    reservation_entity.user = student_entity
    test_session.add(reservation_entity)
    reservation_entity_2 = ReservationEntity.from_form_model(reservation_2)
    reservation_entity_2.reservable = reservable_entity
    reservation_entity_2.user = student_entity
    test_session.add(reservation_entity_2)
    test_session.commit()
    yield

@pytest.fixture()
def reservation_service(test_session: Session):
    return ReservationService(test_session)

def test_single_reservation(reservation_service: ReservationService):
    assert reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=True).items[0] == Reservation(id=1, start_time=reservation.start_time, end_time=reservation.end_time)

def test_zero_reservations(reservation_service: ReservationService):
    assert len(reservation_service.list_user_reservations(user=root, pagination_params=pagination_params, upcoming=True).items) == 0

def test_reservation_history(reservation_service: ReservationService):
    assert len(reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=False).items) == 0

def test_reservation_order(reservation_service: ReservationService):
    res_list = reservation_service.list_user_reservations(user=student, pagination_params=pagination_params, upcoming=True).items
    assert res_list[0].start_time < res_list[1].start_time

def test_get_reservable(reservation_service: ReservationService):
    assert reservation_service.get_reservable(1) == reservable
    assert reservation_service.get_reservable(2) == reservable


def test_get_reservation(reservation_service: ReservationService):
    assert reservation_service.get_reservation(1) == Reservation(id=1, start_time=reservation.start_time, end_time=reservation.end_time)
    assert reservation_service.get_reservation(3) == None

def test_delete_reservation(reservation_service: ReservationService):
    reservation_service.delete_reservation(2)
    assert reservation_service.get_reservation(2) == None

def test_get_reservations_by_reservable(reservation_service: ReservationService):
    assert reservation_service.get_reservations_by_reservable(1, start_time) == [Reservation(id=1, start_time=reservation.start_time, end_time=reservation.end_time)]
    assert reservation_service.get_reservations_by_reservable(1, start_time_2) == [Reservation(id=2, start_time=reservation_2.start_time, end_time=reservation_2.end_time)]

def test_get_reservations_by_reservable_empty(reservation_service: ReservationService):
    assert reservation_service.get_reservations_by_reservable(1, start_time_2 + timedelta(days=1)) == []

def test_create_reservation(reservation_service: ReservationService):
    time = datetime.now(timezone.utc) + timedelta(days=4)
    start_time = datetime(year=time.year, day=time.day, month=time.month, hour=12, tzinfo=time.tzinfo)
    end_time = start_time + timedelta(hours=2)
    res = reservation_service.create_reservation(reservation_form=ReservationForm(start_time=start_time, end_time=end_time, reservable_id=reservable.id), user_id=student.id)
    assert res == Reservation(id=3, start_time=start_time, end_time=end_time)

def test_create_reservation_at_invalid_time():
    time = datetime.now(timezone.utc) + timedelta(days=1)
    start_time = datetime(year=time.year, day=time.day, month=time.month, hour=12)
    end_time = start_time + timedelta(hours=2)
    
    with pytest.raises(ValidationError):
        ReservationForm(start_time=start_time.replace(microsecond=1), end_time=end_time, reservable_id=reservable.id)
    
    with pytest.raises(ValidationError):
        ReservationForm(start_time=start_time.replace(second=1), end_time=end_time, reservable_id=reservable.id)

    with pytest.raises(ValidationError):
        ReservationForm(start_time=start_time.replace(minute=1), end_time=end_time, reservable_id=reservable.id)

def test_reservation_validate_end_time():
    time = datetime.now(timezone.utc) + timedelta(days=2)
    start_time = datetime(year=time.year, month=time.month, day=time.day, hour=12)
    end_time = start_time - timedelta(hours=1)
    with pytest.raises(ValidationError):
        ReservationForm(start_time=start_time, end_time=end_time, reservable_id=reservable.id)

    with pytest.raises(ValidationError):
        ReservationForm(start_time=start_time, end_time=start_time+timedelta(days=2))

def test_cannot_create_overlapping_reservation(reservation_service: ReservationService):
    reservation_form = ReservationForm(start_time=reservation.start_time + timedelta(minutes=30), end_time=reservation.end_time + timedelta(minutes=30), reservable_id=reservation.reservable_id)
    with pytest.raises(ValueError):
        reservation_service.create_reservation(reservation_form=reservation_form, user_id=student.id)

    reservation_form = ReservationForm(start_time=reservation.start_time + timedelta(minutes=30), end_time=reservation.end_time - timedelta(minutes=30), reservable_id=reservation.reservable_id)
    with pytest.raises(ValueError):
        reservation_service.create_reservation(reservation_form=reservation_form, user_id=student.id)

    reservation_form = ReservationForm(start_time=reservation.start_time - timedelta(minutes=30), end_time=reservation.end_time - timedelta(minutes=30), reservable_id=reservation.reservable_id)
    with pytest.raises(ValueError):
        reservation_service.create_reservation(reservation_form=reservation_form, user_id=student.id)

    reservation_form = ReservationForm(start_time=reservation.end_time, end_time=reservation.end_time + timedelta(minutes=30), reservable_id=reservation.reservable_id)
    reservation_service.create_reservation(reservation_form=reservation_form, user_id=student.id)

    reservation_form = ReservationForm(start_time=reservation.start_time - timedelta(minutes=30), end_time=reservation.start_time, reservable_id=reservation.reservable_id)
    reservation_service.create_reservation(reservation_form=reservation_form, user_id=student.id)

def test_created_reservation_saved_to_db(reservation_service: ReservationService):
    time = datetime.now(timezone.utc) + timedelta(days=5)
    start_time = datetime(year=time.year, day=time.day, month=time.month, hour=12)
    end_time = start_time + timedelta(hours=2)
    res = reservation_service.create_reservation(reservation_form=ReservationForm(start_time=start_time, end_time=end_time, reservable_id=reservable.id), user_id=student.id)
    assert reservation_service.get_reservation(res.id) == res

def test_get_end_times(reservation_service: ReservationService):
    res = reservation_service.get_available_end_times(reservable.id, start_time - timedelta(hours=1))
    assert res == [start_time - timedelta(minutes=30), start_time]

def test_get_end_times_with_no_reservations_that_day(reservation_service: ReservationService):
    start_time = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0, hour=12)
    start_time += timedelta(days=5)
    res = reservation_service.get_available_end_times(reservable.id, start_time)
    expected = [start_time + timedelta(minutes=30 * i) for i in range(1,7)]
    assert res == expected    

def test_get_end_times_validation(reservation_service: ReservationService):
    time = datetime.now(timezone.utc)
    with pytest.raises(ValueError):
        reservation_service.get_available_end_times(reservable.id, time + timedelta(days=1))

    time = time.replace(second=0, microsecond=1, minute=0)
    with pytest.raises(ValueError):
        reservation_service.get_available_end_times(reservable.id, time - timedelta(days=1))

def test_get_end_times_at_existing_time(reservation_service: ReservationService):
    assert reservation_service.get_available_end_times(reservable.id, start_time) == []