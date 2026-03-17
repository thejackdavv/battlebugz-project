# 🐛 BattleBugz

A Django-powered creature-collecting game where you raise bugs, send them out to explore locations, forage for stat-boosting foods, and battle other bugs.

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Example Data](#example-data)
- [URL Reference](#url-reference)
- [Game Mechanics](#game-mechanics)

---

## Overview

BattleBugz is a single-player web game built with Django. You manage a roster of bugs, each with unique stats and elemental types. One bug is **active** at a time — that's the bug you take with you to explore locations, forage for food, and challenge other bugs to combat. Battles are fully simulated server-side and their round-by-round logs are stored and viewable after the fact.

---

## Core Features

### 🐝 Bugs
- Create bugs with a **10-point stat allocation system** (HP, Armor, Strength, Mobility, Healing Factor)
- Four elemental types: **Fire 🔥 · Water 💧 · Earth 🪨 · Grass 🌿**
- Each bug has a natural habitat (a location), image, and description
- **Activate** any bug to make it your current active bug
- Edit name, image, and description after creation
- View full stats and battle history per bug

### 📍 Locations
- Create and manage locations, each with its own type and available foods
- Each location can have **resident bugs** (their natural habitat)
- **Forage** at a location with your active bug — a random food is selected and permanently boosts one of the bug's stats
- Challenge any resident bug to a **battle** directly from the location page

### 🍎 Food
- Foods are tied to locations and each boosts a specific stat by a set amount
- Add new foods to a location or remove them individually
- Foods can be permanently deleted or just unlinked from a specific location

### ⚔️ Battles
- Select an opponent bug at a location and start a battle
- Battles are **fully simulated** round-by-round using a deterministic formula:
  - Damage = `max(attacker.strength − defender.armor × 0.5, 0)`
  - Defenders have a **dodge chance** based on their Mobility stat
  - After surviving a hit, the defender regenerates `healing_factor × 0.5` HP (capped at max)
  - Roles **swap each round** (attacker and defender alternate)
  - Battle ends when one bug reaches 0 HP, or after 50 rounds (defender wins)
- Full round log stored in the database and displayed in a 3-column layout: attacker · log · defender
- Browse your full battle history with outcomes and timestamps

### 🏠 Homepage
- Displays your **active bug**, the **top bug** by total power, and the **top location** by resident bug count
- Quick-access buttons to all main sections

---

## Project Structure

```
BattleBugz/
├── BattleBugz/          # Django project config (settings, urls, wsgi)
├── bugs/                # Bug model, views, forms, urls
├── locations/           # Location, Food, FoodEvent models, views, forms, urls
│   ├── forage_service.py    # Forage logic (random food selection + stat boost)
├── battles/             # Battle model, views, urls
│   ├── battle_system.py     # Battle simulation engine
├── common/              # Shared: base template, homepage, mixins, templatetags, migrations
│   ├── migrations/
│   │   └── 0001_seed_example_data.py   # Example data migration
│   ├── mixins.py            # PaginatorMixin, SearchBarMixin, CombinedMixin
│   └── templatetags/
│       └── query_keeper_tag.py  # Preserves query params across paginated/filtered pages
├── templates/
│   ├── base.html
│   ├── common/          # welcome.html, bug_card.html, location_card.html, search_bar.html, paginator.html
│   ├── bugs/
│   ├── locations/
│   │   └── foods/
│   └── battles/
└── static/              # CSS, images
```

---

## Tech Stack

| Layer    | Technology                      |
|----------|---------------------------------|
| Backend  | Python 3.12, Django 6.0         |
| Database | PostgreSQL (`psycopg2-binary`)  |
| Frontend | Bootstrap 5.3 (CDN)             |
| Config   | `python-decouple` + `.env` file |

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- PostgreSQL server running locally (or remotely)
- `git`

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/BattleBugz.git
cd BattleBugz
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy the template and fill in your values:

```bash
cp .env.template .env
```

Then edit `.env` — see [Environment Variables](#environment-variables) below.

### 5. Create the PostgreSQL database

```sql
CREATE DATABASE battlebugz;
```

### 6. Run migrations

This will apply all database migrations to create or update the required tables; it does not load any example data.

```bash
python manage.py migrate
```

### 7. Create a superuser (optional, for Django Admin)

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.



### 9. (Optional) Load example data
```bash
python manage.py loaddata initial_data
```

This will load a set of example bugs, locations, foods, and battles into your database. 
For a completely clean slate, run it on a fresh database (or after `python manage.py flush`) 
so that existing records or unique constraints don't conflict with the fixture data.

---
## Environment Variables

All secrets and config live in a `.env` file (never committed). Use `.env.template` as a starting point:

| Variable      | Description                                        | Example             |
|---------------|----------------------------------------------------|---------------------|
| `SECRET_KEY`  | Django secret key (generate one below)             | `django-insecure-…` |
| `DEBUG`       | Enable debug mode (`True` in dev, `False` in prod) | `True`              |
| `DB_NAME`     | PostgreSQL database name                           | `battlebugz`        |
| `DB_USER`     | PostgreSQL username                                | `postgres`          |
| `DB_PASSWORD` | PostgreSQL password                                | `yourpassword`      |
| `DB_HOST`     | Database host                                      | `localhost`         |
| `DB_PORT`     | Database port                                      | `5432`              |

**Generate a secret key:**

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Example Data

Running `python manage.py loaddata initial_data` automatically seeds the database with example data via `common/fixtures/initial_data.json`:

**5 Locations** — Hellish Volcano, Mirror Lake, Secret Cave, Wide Pastures, Murkwood

**6 Bugs** — Infernal Wasp (Fire), River Mermaid (Water), Rock Beetle (Earth), Slicer Mantis (Grass), BumbleBee (Earth), Spiky (Grass — starts as active)

**6 Foods** — Sweet Apple, Rock Candy, Hot Pepper, Lemonade, FR E SH A VOCA DO, Strong Pineapple

**2 Sample Battles** — with full round-by-round logs

To undo the seed data:

```bash
python manage.py flush
```
Warning! This will delete all data in the database and reset it to a clean state. Use with caution.

---

## URL Reference

| URL Pattern                               | Page                      |
|-------------------------------------------|---------------------------|
| `/`                                       | Homepage                  |
| `/bugs/`                                  | Bug list                  |
| `/bugs/create/`                           | Create a new bug          |
| `/bugs/<pk>/`                             | Bug detail                |
| `/bugs/<pk>/edit/`                        | Edit bug                  |
| `/bugs/<pk>/delete/`                      | Delete bug                |
| `/bugs/<pk>/change-active/`               | Activate bug              |
| `/locations/`                             | Location list             |
| `/locations/create/`                      | Create a location         |
| `/locations/<pk>/`                        | Location detail + forage  |
| `/locations/<pk>/edit/`                   | Edit location             |
| `/locations/<pk>/delete/`                 | Delete location           |
| `/locations/<pk>/foods/create/`           | Add food to location      |
| `/locations/<pk>/foods/<food_pk>/delete/` | Delete food permanently   |
| `/locations/<pk>/foods/<food_pk>/remove/` | Remove food from location |
| `/locations/<pk>/forage/`                 | Forage action (POST)      |
| `/battles/`                               | Battle history            |
| `/battles/<pk>/`                          | Battle detail / round log |
| `/battles/start/<location_pk>/`           | Start a battle (POST)     |
| `/admin/`                                 | Django admin panel        |

---

## Game Mechanics

### Stat Allocation (Bug Creation)

Each new bug gets **10 points** to distribute across 5 stats (0–5 per stat):

| Stat                | Effect                                                      |
|---------------------|-------------------------------------------------------------|
| `max_health_points` | Total HP pool                                               |
| `armor`             | Reduces incoming damage each hit                            |
| `strength`          | Raw attack damage per round                                 |
| `mobility`          | Increases dodge chance (`mobility / (mobility + 100)`)      |
| `healing_factor`    | Regenerates `healing_factor × 0.5` HP after surviving a hit |

Base stats of **20 / 3 / 3 / 3 / 3** are applied before your allocation, so every bug starts viable.  
Each bug's elemental type gives it a small boost to one stat:  

| Bug Type | Stat Boost        |
|----------|-------------------|
| Fire     | +2 Strength       |
| Water    | +2 Mobility       |
| Earth    | +2 Armor          |
| Grass    | +2 Healing Factor |  

### Battle Formula

```
dodge_chance  = defender.mobility / (defender.mobility + 100)
damage        = max(attacker.strength - defender.armor × 0.5, 0)
regen per hit = defender.healing_factor × 0.5   (capped at max HP)
```

Attacker and defender **swap roles every round**. Maximum 50 rounds — if both bugs survive, the defender is declared the winner.

### Foraging

Foraging picks a **random food** from the location's food list and permanently increases the active bug's corresponding stat by `food.increase_amount`. The event is logged in `FoodEvent` for history tracking.

If you encounter any bugs in the app - feedback is greatly appreciated!  
Happy bug battling! 🐛⚔️