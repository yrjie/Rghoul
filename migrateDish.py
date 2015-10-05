from Rghoul.models import Dish, Dish0

props = [
'name',
'booth',
'ingredient',
'price',
'date',
'mealTime',
'floor',
'like',
'dislike'
]

allD0 = Dish0.objects.all()
cnt = 0
for d0 in allD0:
    d=Dish()
    for x in props:
        setattr(d, x, getattr(d0, x))
    d.energy = 0
    d.save()
    cnt += 1
    print cnt
