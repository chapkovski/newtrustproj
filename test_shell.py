from trust.models import Player, City
p = Player.objects.first()
city = City.objects.first()
for i in range(10000):
    p.decisions.create(decision_type='sender_decision', answer=666, city=city)
    print(i)
print(p.decisions.all().count())
