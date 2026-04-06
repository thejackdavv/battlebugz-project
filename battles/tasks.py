from celery import shared_task
from battles.battle_system import create_battle
from bugs.models import Bug
from locations.models import Location
from django.shortcuts import get_object_or_404

@shared_task
def run_battle_async(attacker_id, defender_id, location_id):
    attacker = Bug.objects.get(pk=attacker_id)
    defender = Bug.objects.get(pk=defender_id)
    location = Location.objects.get(pk=location_id)
    
    battle = create_battle(attacker, defender, location)
    return battle.pk
