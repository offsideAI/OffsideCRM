"""Seed the database with realistic demo CRM data.

Idempotent: re-running keeps the demo user, pipeline and stages, and only
inserts sample companies/contacts/deals once (skips if companies already exist).

    python manage.py seed_demo
"""
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import (
    Activity,
    Company,
    Contact,
    Deal,
    Note,
    Pipeline,
    Profile,
    Stage,
    Task,
)

User = get_user_model()

DEMO_EMAIL = "demo@offsideventures.com"
DEMO_PASSWORD = "offside1234"

COMPANIES = [
    {"name": "Northwind Labs", "domain": "northwindlabs.com", "industry": "Biotech", "size": "51-200", "status": "active", "city": "Boston", "country": "USA"},
    {"name": "Helio Freight", "domain": "heliofreight.com", "industry": "Logistics", "size": "201-1000", "status": "customer", "city": "Rotterdam", "country": "Netherlands"},
    {"name": "Cobalt Studio", "domain": "cobalt.studio", "industry": "Design", "size": "11-50", "status": "prospect", "city": "Lisbon", "country": "Portugal"},
    {"name": "Meridian Capital", "domain": "meridiancap.com", "industry": "Finance", "size": "1000+", "status": "active", "city": "New York", "country": "USA"},
    {"name": "Tindr Robotics", "domain": "tindr.io", "industry": "Manufacturing", "size": "51-200", "status": "prospect", "city": "Munich", "country": "Germany"},
    {"name": "Vela Health", "domain": "velahealth.com", "industry": "Healthcare", "size": "11-50", "status": "customer", "city": "Austin", "country": "USA"},
]

# (company_index, first, last, title, status)
CONTACTS = [
    (0, "Ada", "Reyes", "VP Engineering", "active"),
    (0, "Marcus", "Lin", "Procurement Lead", "lead"),
    (1, "Sofia", "Okonkwo", "COO", "customer"),
    (1, "Idris", "Khan", "Ops Manager", "active"),
    (2, "Lena", "Vasquez", "Founder", "lead"),
    (3, "Tom", "Becker", "Managing Director", "active"),
    (3, "Priya", "Nair", "Analyst", "lead"),
    (4, "Hannah", "Stein", "Head of Product", "lead"),
    (5, "Diego", "Moreno", "CEO", "customer"),
    (5, "Grace", "Ahn", "Clinical Lead", "active"),
]

# (name, company_index, contact_index, stage_name, amount, status)
DEALS = [
    ("Northwind platform rollout", 0, 0, "Proposal", 48000, "open"),
    ("Helio annual renewal", 1, 2, "Closed Won", 120000, "won"),
    ("Cobalt brand retainer", 2, 4, "Qualified", 18000, "open"),
    ("Meridian data platform", 3, 5, "Negotiation", 240000, "open"),
    ("Tindr pilot program", 4, 7, "New", 32000, "open"),
    ("Vela expansion", 5, 8, "Proposal", 56000, "open"),
]


class Command(BaseCommand):
    help = "Seed the database with demo CRM data (idempotent)."

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            email=DEMO_EMAIL,
            defaults={"username": "demo", "first_name": "Demo", "last_name": "User", "is_staff": True},
        )
        if created:
            user.set_password(DEMO_PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created demo user {DEMO_EMAIL} / {DEMO_PASSWORD}"))
        Profile.objects.get_or_create(
            user=user, defaults={"role": Profile.ADMIN, "job_title": "Account Executive"}
        )

        pipeline, _ = Pipeline.objects.get_or_create(name="Sales Pipeline", defaults={"is_default": True})
        stage_defs = [
            ("New", 10, False, False),
            ("Qualified", 30, False, False),
            ("Proposal", 55, False, False),
            ("Negotiation", 75, False, False),
            ("Closed Won", 100, True, False),
            ("Closed Lost", 0, False, True),
        ]
        stages = {}
        for index, (name, probability, is_won, is_lost) in enumerate(stage_defs):
            stage, _ = Stage.objects.get_or_create(
                pipeline=pipeline,
                name=name,
                defaults={"order": index, "probability": probability, "is_won": is_won, "is_lost": is_lost},
            )
            stages[name] = stage

        if Company.objects.exists():
            self.stdout.write("Companies already present — skipping sample records.")
            return

        companies = []
        for data in COMPANIES:
            companies.append(Company.objects.create(owner=user, **data))

        contacts = []
        for company_index, first, last, title, status in CONTACTS:
            contacts.append(Contact.objects.create(
                owner=user,
                company=companies[company_index],
                first_name=first,
                last_name=last,
                job_title=title,
                status=status,
                email=f"{first.lower()}@{companies[company_index].domain}",
            ))

        now = timezone.now()
        for offset, (name, company_index, contact_index, stage_name, amount, status) in enumerate(DEALS):
            deal = Deal.objects.create(
                owner=user,
                name=name,
                company=companies[company_index],
                primary_contact=contacts[contact_index],
                pipeline=pipeline,
                stage=stages[stage_name],
                amount=amount,
                status=status,
                close_date=(now + timedelta(days=14 + offset * 7)).date(),
            )
            Activity.objects.create(
                type=Activity.SYSTEM,
                summary=f"Deal '{deal.name}' created",
                actor=user,
                company=deal.company,
                deal=deal,
            )

        # A few tasks and notes for texture.
        Task.objects.create(title="Send Northwind proposal", priority="high",
                            due_date=now + timedelta(days=2), assignee=user, company=companies[0])
        Task.objects.create(title="Prep Meridian security review", priority="medium",
                            due_date=now + timedelta(days=5), assignee=user, company=companies[3])
        Note.objects.create(body="Champion is Ada; budget confirmed for Q3.", author=user, company=companies[0])

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(companies)} companies, {len(contacts)} contacts, {len(DEALS)} deals."
        ))
