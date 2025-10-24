from django.contrib import admin
from .models import (
    Organization, UserProfile, Project, Proposal,
    Review, Comment, ProjectTimeline, Notification
)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'year_joined', 'is_active', 'contact_email', 'created_at']
    list_filter = ['is_active', 'year_joined']
    search_fields = ['name', 'description', 'contact_email']
    ordering = ['-year_joined', 'name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'organization', 'is_verified', 'created_at']
    list_filter = ['role', 'is_verified', 'organization']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'bio']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role', 'bio', 'avatar_url', 'is_verified')
        }),
        ('Contact & Social', {
            'fields': ('github_username', 'linkedin_url', 'portfolio_url', 'phone_number', 'country', 'timezone')
        }),
        ('Student Information', {
            'fields': ('university', 'degree', 'graduation_year'),
            'classes': ('collapse',)
        }),
        ('Mentor/Organization Information', {
            'fields': ('organization', 'expertise'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'organization', 'year', 'difficulty', 'status', 'created_at']
    list_filter = ['status', 'difficulty', 'year', 'organization']
    search_fields = ['title', 'description', 'expected_outcomes']
    ordering = ['-year', '-created_at']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['mentors']
    fieldsets = (
        ('Basic Information', {
            'fields': ('organization', 'title', 'description', 'expected_outcomes')
        }),
        ('Project Details', {
            'fields': ('skills_required', 'difficulty', 'duration_weeks', 'year', 'max_proposals')
        }),
        ('Mentors & Status', {
            'fields': ('mentors', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'project', 'status', 'submitted_at', 'created_at']
    list_filter = ['status', 'project__organization', 'submitted_at']
    search_fields = ['title', 'abstract', 'student__user__username']
    ordering = ['-submitted_at', '-created_at']
    readonly_fields = ['submitted_at', 'reviewed_at', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'student', 'title', 'abstract', 'status')
        }),
        ('Proposal Content', {
            'fields': ('detailed_description', 'implementation_plan', 'timeline', 'deliverables')
        }),
        ('Additional Information', {
            'fields': ('prior_experience', 'why_this_project', 'availability'),
            'classes': ('collapse',)
        }),
        ('Attachments', {
            'fields': ('proposal_document_url', 'github_repo_url'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('submitted_at', 'reviewed_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['proposal', 'reviewer', 'overall_score', 'recommendation', 'is_final', 'created_at']
    list_filter = ['recommendation', 'is_final', 'created_at']
    search_fields = ['proposal__title', 'reviewer__user__username']
    ordering = ['-created_at']
    readonly_fields = ['overall_score', 'created_at', 'updated_at']
    fieldsets = (
        ('Review Information', {
            'fields': ('proposal', 'reviewer', 'recommendation', 'is_final')
        }),
        ('Ratings', {
            'fields': (
                'technical_feasibility', 'understanding_of_project',
                'implementation_quality', 'timeline_realism', 'student_capability',
                'overall_score'
            )
        }),
        ('Feedback', {
            'fields': ('strengths', 'weaknesses', 'suggestions', 'private_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['proposal', 'author', 'is_internal', 'is_edited', 'created_at']
    list_filter = ['is_internal', 'is_edited', 'created_at']
    search_fields = ['content', 'author__user__username', 'proposal__title']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(ProjectTimeline)
class ProjectTimelineAdmin(admin.ModelAdmin):
    list_display = ['title', 'proposal', 'status', 'expected_completion_date', 'progress_percentage', 'order']
    list_filter = ['status', 'expected_completion_date']
    search_fields = ['title', 'description', 'proposal__title']
    ordering = ['proposal', 'order', 'expected_completion_date']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'recipient', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'recipient__user__username']
    ordering = ['-created_at']
    readonly_fields = ['read_at', 'created_at']
