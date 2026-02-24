from django.db import migrations


LOCATIONS = [
    dict(id=1, name='Hellish Volcano', type='FIRE',
         image_url='https://www.famsf.org/storage/images/a1f4584e-b892-4148-724f-0bd42cc65aad/tavernier-volcanos-hero.jpg?crop=1800,948,x0,y0&format=jpg&quality=80',
         description='a very hot place'),
    dict(id=2, name='Mirror Lake', type='WATER',
         image_url='https://images.saatchiart.com/saatchi/2145563/art/10134515/9197285-TOUVNYXZ-7.jpg',
         description='a peaceful watery place'),
    dict(id=3, name='Secret Cave', type='EARTH',
         image_url='https://www.paintingstar.com/static/gallery/2008/05/28/52a5f346709f1.jpg',
         description='a very well hidden cave'),
    dict(id=4, name='Wide Pastures', type='GRASS',
         image_url='https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/dandelion-meadows-frank-wilson.jpg',
         description="there's a lot of grass"),
    dict(id=5, name='Murkwood', type='GRASS',
         image_url='https://cdnb.artstation.com/p/assets/images/images/002/098/717/large/will-roberts-murkwood.jpg',
         description='a very dark forest with spiders'),
]

BUGS = [
    dict(id=1, name='Infernal Wasp', type='FIRE', natural_habitat_id=1, is_active=False,
         image_url='https://cdna.artstation.com/p/assets/images/images/010/172/482/large/dave-melvin-fire-bug.jpg?1522952103',
         description='a very scary looking bad boi',
         max_health_points=20, armor=5, strength=8, mobility=6, healing_factor=3),
    dict(id=2, name='River Mermaid', type='WATER', natural_habitat_id=2, is_active=False,
         image_url='https://media.craiyon.com/2025-05-05/RbG0xQr1RxCqnQ5EyqhJxA.webp',
         description='a cute little swimmer packs a powerful punch',
         max_health_points=20, armor=3, strength=5, mobility=8, healing_factor=6),
    dict(id=3, name='Rock Beetle', type='EARTH', natural_habitat_id=3, is_active=False,
         image_url='https://pbs.twimg.com/media/F9qt9_abYAA5jzQ.jpg',
         description='sturdy little warrior, rock and stone',
         max_health_points=20, armor=8, strength=6, mobility=3, healing_factor=5),
    dict(id=4, name='Slicer Mantis', type='GRASS', natural_habitat_id=4, is_active=False,
         image_url='https://media.craiyon.com/2025-09-12/MWF1AY6RQzyvmAN_Dyy9iQ.webp',
         description="it's called a praying mantis because you should pray to it if you wanna survive",
         max_health_points=20, armor=3, strength=6, mobility=8, healing_factor=8),
    dict(id=5, name='BumbleBee', type='EARTH', natural_habitat_id=3, is_active=False,
         image_url='https://i.pinimg.com/736x/6e/01/c4/6e01c457f615804096f3dfa375a681c9.jpg',
         description='strong and fluffy, ready to fight',
         max_health_points=24, armor=10, strength=9, mobility=6, healing_factor=3),
    dict(id=6, name='Spiky', type='GRASS', natural_habitat_id=4, is_active=True,
         image_url='https://media.craiyon.com/2025-10-05/s5VjKzL3RPqWp6HgING_Yg.webp',
         description='he would do anything to protect his grass',
         max_health_points=22, armor=5, strength=5, mobility=3, healing_factor=9),
]

FOODS = [
    dict(id=1, name='Sweet Apple',      stat='MAX_HP',         increase_amount=1, location_ids=[1, 2, 3, 4]),
    dict(id=2, name='Rock Candy',       stat='ARMOR',          increase_amount=1, location_ids=[3]),
    dict(id=3, name='Hot Pepper',       stat='STRENGTH',       increase_amount=1, location_ids=[1]),
    dict(id=4, name='Lemonade',         stat='MOBILITY',       increase_amount=1, location_ids=[2]),
    dict(id=5, name='FR E SH A VOCA DO', stat='HEALING_FACTOR', increase_amount=1, location_ids=[4]),
    dict(id=6, name='Strong Pineapple', stat='STRENGTH',       increase_amount=1, location_ids=[3]),
]

BATTLE_3_LOG = [{"round": 1, "damage": 0, "dodged": True, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 20}, {"round": 2, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 20, "defender_hp": 24}, {"round": 3, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 17.5}, {"round": 4, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 17.5, "defender_hp": 24}, {"round": 5, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 15.0}, {"round": 6, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 15.0, "defender_hp": 24}, {"round": 7, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 12.5}, {"round": 8, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 12.5, "defender_hp": 24}, {"round": 9, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 10.0}, {"round": 10, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 10.0, "defender_hp": 24}, {"round": 11, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 7.5}, {"round": 12, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 7.5, "defender_hp": 24}, {"round": 13, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 5.0}, {"round": 14, "damage": 0, "dodged": True, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 5.0, "defender_hp": 24}, {"round": 15, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 2.5}, {"round": 16, "damage": 0, "dodged": False, "attacker": "Infernal Wasp", "defender": "BumbleBee", "attacker_hp": 2.5, "defender_hp": 24}, {"round": 17, "damage": 4, "dodged": False, "attacker": "BumbleBee", "defender": "Infernal Wasp", "attacker_hp": 24, "defender_hp": 0}]  # noqa: E501

BATTLE_4_LOG = [{"round": 1, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 18.0}, {"round": 2, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 18.0, "defender_hp": 20}, {"round": 3, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 16.0}, {"round": 4, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 16.0, "defender_hp": 20}, {"round": 5, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 14.0}, {"round": 6, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 14.0, "defender_hp": 20}, {"round": 7, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 12.0}, {"round": 8, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 12.0, "defender_hp": 20}, {"round": 9, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 10.0}, {"round": 10, "damage": 0, "dodged": True, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 10.0, "defender_hp": 20}, {"round": 11, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 8.0}, {"round": 12, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 8.0, "defender_hp": 20}, {"round": 13, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 6.0}, {"round": 14, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 6.0, "defender_hp": 20}, {"round": 15, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 4.0}, {"round": 16, "damage": 0, "dodged": False, "attacker": "River Mermaid", "defender": "Infernal Wasp", "attacker_hp": 4.0, "defender_hp": 20}, {"round": 17, "damage": 5, "dodged": False, "attacker": "Infernal Wasp", "defender": "River Mermaid", "attacker_hp": 20, "defender_hp": 0}]  # noqa: E501

BATTLES = [
    dict(id=1, attacker_id=5, defender_id=1, winner_id=5, location_id=1, rounds=17,
         log=BATTLE_3_LOG),
    dict(id=2, attacker_id=1, defender_id=2, winner_id=1, location_id=2, rounds=17,
         log=BATTLE_4_LOG),
]


def seed_data(apps, schema_editor):
    Location = apps.get_model('locations', 'Location')
    Bug = apps.get_model('bugs', 'Bug')
    Food = apps.get_model('locations', 'Food')
    Battle = apps.get_model('battles', 'Battle')

    # 1. Locations (bugs reference them, so create first)
    for data in LOCATIONS:
        Location.objects.get_or_create(id=data['id'], defaults={k: v for k, v in data.items() if k != 'id'})

    # 2. Bugs (battles reference them)
    for data in BUGS:
        Bug.objects.get_or_create(id=data['id'], defaults={k: v for k, v in data.items() if k != 'id'})

    # 3. Foods + M2M location links
    for data in FOODS:
        location_ids = data.pop('location_ids')
        food, _ = Food.objects.get_or_create(id=data['id'], defaults={k: v for k, v in data.items() if k != 'id'})
        food.location.set(location_ids)

    # 4. Battles
    for data in BATTLES:
        Battle.objects.get_or_create(id=data['id'], defaults={k: v for k, v in data.items() if k != 'id'})


def unseed_data(apps, schema_editor):
    Battle = apps.get_model('battles', 'Battle')
    Food = apps.get_model('locations', 'Food')
    Bug = apps.get_model('bugs', 'Bug')
    Location = apps.get_model('locations', 'Location')

    Battle.objects.filter(id__in=[d['id'] for d in BATTLES]).delete()
    Food.objects.filter(id__in=[d['id'] for d in FOODS]).delete()
    Bug.objects.filter(id__in=[d['id'] for d in BUGS]).delete()
    Location.objects.filter(id__in=[d['id'] for d in LOCATIONS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('bugs', '0002_bug_only_one_active_bug'),
        ('locations', '0002_food_foodevent'),
        ('battles', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_code=unseed_data),
    ]
