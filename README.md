# 🐛 BattleBugz

A Django-powered creature-collecting game where you raise bugs, send them out to explore locations, forage for stat-boosting foods, and battle other bugs.

---

## Table of Contents

- [Overview](#overview)
- [Core Features](#core-features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)
- [Docker Deployment](#docker-deployment)
- [Environment Variables](#environment-variables)
- [Game Mechanics](#game-mechanics)
- [URL Reference](#url-reference)

---

## Overview

BattleBugz is a single-player web game built with Django. You manage a roster of bugs, each with unique stats and elemental types. As a user, you own your bugs and can activate one at a time — this is the bug you take with you to explore locations, forage for food, and challenge other bugs to combat. Battles are fully simulated server-side and their round-by-round logs are stored and viewable after the fact.

The project includes a robust user account system with role-based permissions, an asynchronous foraging mechanic, and a RESTful API for bug management.

---

## Core Features

### 👤 Accounts & Profiles
- **User Registration & Authentication**: Secure sign-up and login system.
- **Profiles**: Each user has a profile with a bio, date of birth, and an **active bug**.
- **Role-Based Access Control (RBAC)**:
  - **Global Moderators**: Full administrative control.
  - **Location Moderators**: Manage locations and their resident bugs.
  - **User Managing Moderators**: Manage user profiles and permissions.
- **Administrative Tools**: Ability to ban users by setting an unusable password or assign users to specific groups.

### 🐝 Bugs
- **Ownership**: Bugs are owned by users. Only the owner can activate, edit, or delete their bug.
- **Creation**: Create bugs with a **10-point stat allocation system** (HP, Armor, Strength, Mobility, Healing Factor).
- **Elemental Types**: Fire 🔥 · Water 💧 · Earth 🪨 · Grass 🌿.
- **API Access**: Full REST API endpoints for listing, creating, and managing bugs.
- **Filtering**: View "My Bugs" or browse "All Bugs" with built-in search and pagination.

### 📍 Locations & Foraging
- **Resident Bugs**: Each location serves as a natural habitat for specific bugs.
- **Inhabitants Management**: Location moderators can add or remove resident bugs.
- **Asynchronous Foraging**: Send your active bug to forage. This is handled via Django's **async views**, simulating a time-delayed search for food.
- **Stat Boosts**: Foraging rewards you with food that permanently boosts your bug's stats.

### ⚔️ Battles
- **Dynamic Challenges**: Challenge any resident bug at a location to a battle.
- **Server-Side Simulation**: Battles are fully simulated using a deterministic formula considering stats like armor, strength, and mobility.
- **Detailed Logs**: View round-by-round logs of every battle, showing attacker/defender actions, damage, and health regeneration.
- **Battle History**: Access a full history of all battles with outcomes and timestamps.

---

## Project Structure

```
BattleBugz/
├── BattleBugz/          # Django project config (settings, urls, wsgi)
├── accounts/            # User profiles, registration, and RBAC logic
├── bugs/                # Bug model, views, forms, urls, and REST API
│   ├── api_views.py     # DRF API views
│   ├── serializers.py   # Bug serializers for API
├── locations/           # Location, Food, FoodEvent models, views, forms
│   ├── forage_service.py    # Forage logic (random food selection + stat boost)
├── battles/             # Battle model, views, and simulation engine
│   ├── battle_system.py     # Battle simulation engine
├── common/              # Shared logic: base template, homepage, mixins, templatetags
├── templates/           # Organized by app (accounts, bugs, locations, battles)
├── static/              # CSS, images (served via WhiteNoise)
└── media/               # User-uploaded bug images
```

---

## Tech Stack

| Layer          | Technology                                   |
|----------------|----------------------------------------------|
| **Backend**    | Python 3.12, Django 5.2                      |
| **API**        | Django REST Framework 3.17                   |
| **Database**   | PostgreSQL (`psycopg2-binary`)               |
| **Frontend**   | Bootstrap 5.3 (CDN), Vanilla CSS             |
| **Async**      | Python `asyncio` & `asgiref`                 |
| **Static Files**| WhiteNoise                                  |
| **Deployment** | Docker, Gunicorn                             |

---

## Installation & Setup

### Prerequisites

- Python 3.12+
- PostgreSQL server
- `git`

### 1. Clone & Environment

```bash
git clone https://github.com/<your-username>/BattleBugz.git
cd BattleBugz
python -m venv .venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configuration

Copy the template and fill in your values:

```bash
cp .env.template .env
```

### 3. Database & Static Files

```bash
python manage.py migrate
python manage.py collectstatic
python manage.py createsuperuser  # Optional
```

### 4. Start Server

```bash
python manage.py runserver
```

---

## Docker Deployment

The project is containerized for easy deployment:

```bash
# Build and run with Docker
docker build -t battlebugz .
docker run -p 8000:8000 --env-file .env battlebugz
```

The `entrypoint.sh` script handles static file collection, migrations, and starts the server using `gunicorn`.

---

## Environment Variables

| Variable                | Description                                        | Example             |
|-------------------------|----------------------------------------------------|---------------------|
| `SECRET_KEY`            | Django secret key                                  | `django-insecure-…` |
| `DEBUG`                 | Debug mode (True/False)                            | `True`              |
| `ALLOWED_HOSTS`         | List of allowed hostnames                          | `localhost,127.0.0.1`|
| `CSRF_TRUSTED_ORIGINS`  | Trusted origins for CSRF                           | `http://localhost:8000`|
| `DB_NAME`               | PostgreSQL database name                           | `battlebugz`        |
| `DB_USER`               | PostgreSQL username                                | `postgres`          |
| `DB_PASSWORD`           | PostgreSQL password                                | `yourpassword`      |
| `DB_HOST`               | Database host                                      | `db`                |
| `DB_PORT`               | Database port                                      | `5432`              |

---

## Game Mechanics

### Stat Allocation (Bug Creation)
Each bug starts with base stats of **20 HP / 3 Armor / 3 Strength / 3 Mobility / 3 Healing Factor**. You then allocate **10 points** (max 5 per stat).

### Battle Formula
- **Dodge Chance**: `mobility / (mobility + 100)`
- **Damage**: `max(attacker.strength − defender.armor × 0.5, 0)`
- **Regeneration**: `healing_factor × 0.5` per hit survived (capped at max HP).
- **Max Rounds**: 50 (Defender wins if both survive).

### Foraging
Picking "Forage" at a location triggers an async process. After a short delay, your bug finds a random food associated with that location, permanently boosting its stats.

---

## URL Reference

| URL Pattern                               | Description                          |
|-------------------------------------------|--------------------------------------|
| `/`                                       | Homepage                              |
| `/accounts/register/`                     | User registration                     |
| `/accounts/login/`                        | User login                            |
| `/accounts/profile/<pk>/`                 | User profile & moderation tools       |
| `/bugs/`                                  | Bug list (My Bugs / All Bugs)         |
| `/bugs/api/`                              | **REST API**: Bug List/Create         |
| `/bugs/api/<pk>/`                         | **REST API**: Bug Detail/Update/Delete|
| `/locations/`                             | Location list                         |
| `/locations/<pk>/forage/`                 | Async forage action                   |
| `/battles/`                               | Battle history                        |
| `/battles/<pk>/`                          | Battle round logs                     |

---

If you encounter any bugs in the app - feedback is greatly appreciated!  
Happy bug battling! 🐛⚔️
