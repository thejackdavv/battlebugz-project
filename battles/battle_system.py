import random

from django.db import transaction

from battles.models import Battle

MAX_ROUND = 100

def simulate_battle(attacker, defender):

    attacker_hp = attacker.max_health_points
    defender_hp = defender.max_health_points

    log = []
    round_number = 1

    while (
        attacker_hp > 0
        and defender_hp > 0
        and round_number <= MAX_ROUND
    ):
        round_data = {
            'round': round_number,
            'attacker': attacker.name,
            'defender': defender.name,
        }

        dodge_chance = defender.mobility / (defender.mobility + 100)

        if random.random() < dodge_chance:
            damage = 0
            round_data['dodged'] = True
        else:
            damage = max(attacker.strength - defender.armor, 0)
            defender_hp -= damage
            round_data['dodged'] = False

        round_data['damage'] = damage

        if defender_hp > 0:
            defender_hp += defender.healing_factor * 0.5
            defender_hp = min(defender_hp, defender.max_health_points)

        round_data['attacker_hp'] = attacker_hp
        round_data['defender_hp'] = max(defender_hp, 0)

        log.append(round_data)

        attacker, defender = defender, attacker
        attacker_hp, defender_hp = defender_hp, attacker_hp
        round_number += 1

    winner = defender if defender_hp > 0 else attacker

    return winner, round_number - 1, log

def create_battle(attacker, defender, location):

    winner, round_number, log = simulate_battle(attacker, defender)

    with transaction.atomic():
        battle = Battle.objects.create(
            attacker=attacker,
            defender=defender,
            winner=winner,
            location=location,
            rounds=round_number,
            log=log,
        )
    return battle