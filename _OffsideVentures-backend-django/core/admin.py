"""Django admin, styled with django-unfold, for a premium back-office UX.

Every CRM model is registered with an Unfold ``ModelAdmin`` configured with
sensible list displays, search, filters, and autocompletes so internal/admin
users get a fast, readable management surface.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin

from .models import (
    Activity,
    AgentAction,
    BlacklistedAccessToken,
    Company,
    Contact,
    Deal,
    Note,
    Pipeline,
    Profile,
    Stage,
    Task,
)
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_deactivated')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ('user', 'role', 'job_title', 'phone')
    list_filter = ('role',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'job_title')
    autocomplete_fields = ('user',)


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'status', 'industry', 'size', 'city', 'owner', 'created_at')
    list_filter = ('status', 'size', 'industry')
    search_fields = ('name', 'domain', 'email', 'city', 'country')
    autocomplete_fields = ('owner',)
    list_select_related = ('owner',)
    date_hierarchy = 'created_at'


@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('full_name', 'email', 'job_title', 'company', 'status', 'owner')
    list_filter = ('status',)
    search_fields = ('first_name', 'last_name', 'email', 'company__name')
    autocomplete_fields = ('company', 'owner')
    list_select_related = ('company', 'owner')

    @admin.display(description='Name')
    def full_name(self, obj):
        return obj.full_name


@admin.register(Pipeline)
class PipelineAdmin(ModelAdmin):
    list_display = ('name', 'is_default')
    list_filter = ('is_default',)
    search_fields = ('name',)


@admin.register(Stage)
class StageAdmin(ModelAdmin):
    list_display = ('name', 'pipeline', 'order', 'probability', 'is_won', 'is_lost')
    list_filter = ('pipeline', 'is_won', 'is_lost')
    search_fields = ('name', 'pipeline__name')
    autocomplete_fields = ('pipeline',)
    list_select_related = ('pipeline',)


@admin.register(Deal)
class DealAdmin(ModelAdmin):
    list_display = ('name', 'company', 'stage', 'amount', 'currency', 'status', 'close_date', 'owner')
    list_filter = ('status', 'pipeline', 'stage', 'currency')
    search_fields = ('name', 'company__name')
    autocomplete_fields = ('company', 'primary_contact', 'pipeline', 'stage', 'owner')
    list_select_related = ('company', 'stage', 'owner')
    date_hierarchy = 'close_date'


@admin.register(Task)
class TaskAdmin(ModelAdmin):
    list_display = ('title', 'status', 'priority', 'due_date', 'assignee')
    list_filter = ('status', 'priority')
    search_fields = ('title', 'description')
    autocomplete_fields = ('assignee', 'company', 'contact', 'deal')
    list_select_related = ('assignee',)


@admin.register(Note)
class NoteAdmin(ModelAdmin):
    list_display = ('__str__', 'author', 'company', 'contact', 'deal', 'created_at')
    search_fields = ('body',)
    autocomplete_fields = ('author', 'company', 'contact', 'deal')
    date_hierarchy = 'created_at'


@admin.register(Activity)
class ActivityAdmin(ModelAdmin):
    list_display = ('type', 'summary', 'actor', 'occurred_at')
    list_filter = ('type',)
    search_fields = ('summary', 'body')
    autocomplete_fields = ('actor', 'company', 'contact', 'deal')
    date_hierarchy = 'occurred_at'


@admin.register(AgentAction)
class AgentActionAdmin(ModelAdmin):
    list_display = ('action_type', 'status', 'target_type', 'target_id', 'model', 'actor', 'created_at')
    list_filter = ('status', 'action_type')
    search_fields = ('action_type', 'prompt')
    autocomplete_fields = ('actor',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'


@admin.register(BlacklistedAccessToken)
class BlacklistedAccessTokenAdmin(ModelAdmin):
    list_display = ('token_jti', 'user', 'created_at')
    search_fields = ('token_jti', 'user__email')
    autocomplete_fields = ('user',)
