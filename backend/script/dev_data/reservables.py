from ...models import Reservable, ReservableForm

room_1 = Reservable(id=1, name='Room #1', type='Room', description='First room in CSXL')
pc_1 = Reservable(id=2, name='PC #1', type='PC', description='First PC in CSXL')
laptop_1 = Reservable(id=3, name='Laptop #1', type='Laptop', description='First laptop in CSXL')

models = [room_1, pc_1, laptop_1]