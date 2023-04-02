from ...models import Reservation
from . import users, reservables
from datetime import datetime

res_1 =  Reservation(id=1,
                    start_time=datetime(2023, 3, 25, 12, 0, 0, 0),
                    end_time= datetime(2023, 3, 25, 15, 0, 0, 0))

res_2 =  Reservation(id=2, 
                     start_time=datetime(2023, 4, 12, 12, 0, 0, 0), 
                     end_time=datetime(2023, 4, 12, 14, 30, 0, 0)
                     )

res_3 = Reservation(id=3, 
                     start_time=datetime(2023, 3, 26, 15, 0, 0, 0), 
                     end_time=datetime(2023, 3, 26, 16, 0, 0, 0)
                     )
res_4 = Reservation(id=4, 
                     start_time=datetime(2023, 4, 13, 9, 0, 0, 0), 
                     end_time=datetime(2023, 4, 13, 12, 0, 0, 0)
                     )

triplets = [
    (res_1, reservables.room_1, users.sol_student),
    (res_2, reservables.laptop_1, users.sol_student),
    (res_3, reservables.pc_1, users.arden_ambassador),
    (res_4, reservables.room_1, users.sol_student)
]

