from django.contrib import admin
from .models import User, Prompt

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')

@admin.register(Prompt)
class PromptAdmin(admin.ModelAdmin):
    list_display = ('title', 'username', 'status', 'is_trending', 'created')
    list_filter = ('status', 'is_trending', 'created')
    search_fields = ('title', 'username', 'text')
    list_editable = ('status', 'is_trending')
    actions = ['approve_prompts', 'reject_prompts']
    
    def approve_prompts(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"Approved {queryset.count()} prompts.")
    
    def reject_prompts(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"Rejected {queryset.count()} prompts.")
    
    approve_prompts.short_description = "Approve selected prompts"
    reject_prompts.short_description = "Reject selected prompts"
