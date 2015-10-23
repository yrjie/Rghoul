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
'dislike',
'energy'
]

allD0 = Dish0.objects.all()
cnt = 0
for d0 in allD0:
    d=Dish()
    for x in props:
        setattr(d, x, getattr(d0, x))
    d.pid = d0.id
    d.save()
    cnt += 1
print cnt
