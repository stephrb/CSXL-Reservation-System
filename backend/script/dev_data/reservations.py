from ...models import Reservation, ReservationForm
from . import users, reservables
from datetime import datetime, timedelta

time_1 = datetime.now() + timedelta(days = 6)
time_1 = time_1.replace(hour=15, minute=0, second=0, microsecond=0)

time_2 = datetime.now() + timedelta(days = 5)
time_2 = time_1.replace(hour=12, minute=0, second=0, microsecond=0)

res_1 =  ReservationForm(start_time=datetime(2023, 3, 25, 12, 0, 0, 0),
                    end_time= datetime(2023, 3, 25, 15, 0, 0, 0))

res_2 =  ReservationForm(start_time=time_1, 
                     end_time=time_1 + timedelta(hours=3)
                     )

res_3 = ReservationForm(start_time=datetime(2023, 3, 26, 15, 0, 0, 0), 
                     end_time=datetime(2023, 3, 26, 16, 0, 0, 0)
                     )
res_4 = ReservationForm(start_time=time_2, 
                     end_time=time_2 + + timedelta(hours=2)
                     )

triplets = [
    (res_1, reservables.room_1, users.sol_student),
    (res_2, reservables.laptop_1, users.sol_student),
    (res_3, reservables.pc_1, users.arden_ambassador),
    (res_4, reservables.room_1, users.sol_student)
]

