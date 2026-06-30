"""OffsideVentures CRM data model.

A pragmatic, generalized B2B sales CRM: Companies (accounts), Contacts (people),
Deals moving through a Pipeline of Stages, plus Tasks, Notes and an Activity
timeline. AgentAction records the audit trail for AI/agent-proposed changes.

v1 keeps things deliberately simple: a single workspace, owner-based record
attribution, embedded address fields (no separate Address table), and
lightweight nullable FKs instead of generic relations for cross-object links.
"""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base adding created/updated timestamps to every record."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---------------------------------------------------------------------------
# Auth & users
# ---------------------------------------------------------------------------
class CustomUser(AbstractUser):
    # Email is the login identifier; username is kept for Django compatibility.
    email = models.EmailField(unique=True)
    is_deactivated = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Profile(TimeStampedModel):
    REGULAR, MANAGER, ADMIN = 'regular', 'manager', 'admin'
    ROLE_CHOICES = [(REGULAR, 'Regular'), (MANAGER, 'Manager'), (ADMIN, 'Admin')]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=REGULAR)
    job_title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    avatar_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.email} profile'


# ---------------------------------------------------------------------------
# CRM core
# ---------------------------------------------------------------------------
class Company(TimeStampedModel):
    PROSPECT, ACTIVE, CUSTOMER, CHURNED = 'prospect', 'active', 'customer', 'churned'
    STATUS_CHOICES = [
        (PROSPECT, 'Prospect'),
        (ACTIVE, 'Active'),
        (CUSTOMER, 'Customer'),
        (CHURNED, 'Churned'),
    ]
    SIZE_CHOICES = [
        ('1-10', '1-10'),
        ('11-50', '11-50'),
        ('51-200', '51-200'),
        ('201-1000', '201-1000'),
        ('1000+', '1000+'),
    ]

    name = models.CharField(max_length=200)
    domain = models.CharField(max_length=200, blank=True, help_text='Website domain, e.g. acme.com')
    industry = models.CharField(max_length=120, blank=True)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROSPECT)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    annual_revenue = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)

    # Embedded address (kept simple for v1 — no separate Address table)
    street = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=120, blank=True)
    state = models.CharField(max_length=120, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=120, blank=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='owned_companies',
    )

    class Meta:
        verbose_name_plural = 'companies'
        ordering = ['name']

    def __str__(self):
        return self.name


class Contact(TimeStampedModel):
    LEAD, ACTIVE, CUSTOMER, ARCHIVED = 'lead', 'active', 'customer', 'archived'
    STATUS_CHOICES = [
        (LEAD, 'Lead'),
        (ACTIVE, 'Active'),
        (CUSTOMER, 'Customer'),
        (ARCHIVED, 'Archived'),
    ]

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    job_title = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=LEAD)
    linkedin_url = models.URLField(blank=True)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='contacts'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='owned_contacts',
    )

    class Meta:
        ordering = ['first_name', 'last_name']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def __str__(self):
        return self.full_name or self.email or f'Contact {self.pk}'


class Pipeline(TimeStampedModel):
    name = models.CharField(max_length=120)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Stage(TimeStampedModel):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=120)
    order = models.PositiveIntegerField(default=0)
    probability = models.PositiveSmallIntegerField(default=0, help_text='Win probability, 0-100')
    is_won = models.BooleanField(default=False)
    is_lost = models.BooleanField(default=False)

    class Meta:
        ordering = ['pipeline', 'order']
        unique_together = [('pipeline', 'name')]

    def __str__(self):
        return f'{self.pipeline.name} · {self.name}'


class Deal(TimeStampedModel):
    OPEN, WON, LOST = 'open', 'won', 'lost'
    STATUS_CHOICES = [(OPEN, 'Open'), (WON, 'Won'), (LOST, 'Lost')]

    name = models.CharField(max_length=200)
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals'
    )
    primary_contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name='deals'
    )
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, related_name='deals')
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name='deals')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OPEN)
    close_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='owned_deals',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Task(TimeStampedModel):
    TODO, IN_PROGRESS, DONE = 'todo', 'in_progress', 'done'
    STATUS_CHOICES = [(TODO, 'To do'), (IN_PROGRESS, 'In progress'), (DONE, 'Done')]
    LOW, MEDIUM, HIGH = 'low', 'medium', 'high'
    PRIORITY_CHOICES = [(LOW, 'Low'), (MEDIUM, 'Medium'), (HIGH, 'High')]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=TODO)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=MEDIUM)
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='assigned_tasks',
    )
    # Lightweight links to the record this task is about (nullable FKs for v1).
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')

    class Meta:
        ordering = ['status', 'due_date', '-created_at']

    def __str__(self):
        return self.title


class Note(TimeStampedModel):
    body = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='notes',
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='notes')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Note {self.pk}'


class Activity(TimeStampedModel):
    """A timeline entry attached to a Company, Contact and/or Deal."""

    NOTE, CALL, EMAIL, MEETING, TASK, STAGE_CHANGE, SYSTEM = (
        'note', 'call', 'email', 'meeting', 'task', 'stage_change', 'system',
    )
    TYPE_CHOICES = [
        (NOTE, 'Note'),
        (CALL, 'Call'),
        (EMAIL, 'Email'),
        (MEETING, 'Meeting'),
        (TASK, 'Task'),
        (STAGE_CHANGE, 'Stage change'),
        (SYSTEM, 'System'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=NOTE)
    summary = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='activities',
    )
    occurred_at = models.DateTimeField(default=timezone.now)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, null=True, blank=True, related_name='activities')

    class Meta:
        verbose_name_plural = 'activities'
        ordering = ['-occurred_at']

    def __str__(self):
        return f'{self.get_type_display()}: {self.summary}'


# ---------------------------------------------------------------------------
# AI / agent audit trail
# ---------------------------------------------------------------------------
class AgentAction(TimeStampedModel):
    """Records every AI/agent suggestion and whether a human approved/applied it.

    Write actions proposed by the AI are stored as `proposed_payload` with status
    `suggested` until a human confirms, at which point they become `applied`.
    """

    SUGGESTED, APPROVED, APPLIED, REJECTED, FAILED = (
        'suggested', 'approved', 'applied', 'rejected', 'failed',
    )
    STATUS_CHOICES = [
        (SUGGESTED, 'Suggested'),
        (APPROVED, 'Approved'),
        (APPLIED, 'Applied'),
        (REJECTED, 'Rejected'),
        (FAILED, 'Failed'),
    ]

    action_type = models.CharField(
        max_length=80, help_text='e.g. summarize_record, draft_email, create_task, score_lead'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SUGGESTED)
    prompt = models.TextField(blank=True)
    result = models.JSONField(default=dict, blank=True)
    # What the AI proposed to write, pending human confirmation.
    proposed_payload = models.JSONField(default=dict, blank=True)
    target_type = models.CharField(max_length=40, blank=True, help_text='company|contact|deal|task|note')
    target_id = models.PositiveIntegerField(null=True, blank=True)
    model = models.CharField(max_length=120, blank=True)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='agent_actions',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.action_type} ({self.status})'


class BlacklistedAccessToken(models.Model):
    """JTIs of access tokens revoked via logout (checked by core.authentication)."""

    token_jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Blacklisted JTI: {self.token_jti}'
