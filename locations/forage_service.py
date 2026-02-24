import random

from django.core.exceptions import ValidationError
from django.db import transaction

from locations.models import FoodEvent

STAT_FIELD_MAP= {
    'MAX_HP': 'max_health_points',
    'ARMOR': 'armor',
    'STRENGTH': 'strength',
    'MOBILITY': 'mobility',
    'HEALING_FACTOR': 'healing_factor',
}

def forage(bug, location):
    foods = list(location.foods.all())
    if not foods:
        return None

    food = random.choice(foods)
    stat_field = STAT_FIELD_MAP.get(food.stat)

    with transaction.atomic():
        current_value = getattr(bug, stat_field)
        setattr(bug, stat_field, current_value + food.increase_amount)
        bug.save()

        FoodEvent.objects.create(
            bug=bug,
            location=location,
            food=food,
        )
    return food