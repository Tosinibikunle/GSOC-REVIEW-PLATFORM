from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Organization(models.Model):
    """Model for GSoC participating organizations"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    logo_url = models.URLField(blank=True, null=True)
    tech_stack = models.JSONField(default=list, blank=True)  # List of technologies
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)
    year_joined = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year_joined', 'name']
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for students, mentors, and administrators"""
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('mentor', 'Mentor'),
        ('admin', 'Administrator'),
        ('org_admin', 'Organization Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    github_username = models.CharField(max_length=100, blank=True)
    linkedin_url = models.URLField(blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)

    # For students
    university = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    # For mentors and org admins
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    expertise = models.JSONField(default=list, blank=True)  # List of expertise areas

    # Common fields
    phone_number = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    timezone = models.CharField(max_length=50, default='UTC')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"


class Project(models.Model):
    """Model for GSoC project ideas from organizations"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    title = models.CharField(max_length=300)
    description = models.TextField()
    expected_outcomes = models.TextField()
    skills_required = models.JSONField(default=list)  # List of required skills
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    duration_weeks = models.IntegerField(default=12)
    mentors = models.ManyToManyField(
        UserProfile,
        related_name='mentoring_projects',
        limit_choices_to={'role__in': ['mentor', 'org_admin']}
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    year = models.IntegerField()
    max_proposals = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-year', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        unique_together = ['organization', 'title', 'year']

    def __str__(self):
        return f"{self.title} - {self.organization.name} ({self.year})"


class Proposal(models.Model):
    """Model for student proposals submitted to projects"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('withdrawn', 'Withdrawn'),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='proposals'
    )
    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='proposals',
        limit_choices_to={'role': 'student'}
    )
    title = models.CharField(max_length=300)
    abstract = models.TextField()
    detailed_description = models.TextField()
    implementation_plan = models.TextField()
    timeline = models.TextField()  # Detailed timeline/milestones
    deliverables = models.TextField()

    # Additional information
    prior_experience = models.TextField(blank=True)
    why_this_project = models.TextField(blank=True)
    availability = models.TextField(help_text="Weekly hours and any time constraints")

    # Proposal metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # Attachments and links
    proposal_document_url = models.URLField(blank=True, null=True)
    github_repo_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at', '-created_at']
        verbose_name = 'Proposal'
        verbose_name_plural = 'Proposals'

    def __str__(self):
        return f"{self.title} by {self.student.user.username}"

    def submit(self):
        """Mark proposal as submitted"""
        if self.status == 'draft':
            self.status = 'submitted'
            self.submitted_at = timezone.now()
            self.save()


class Review(models.Model):
    """Model for mentor reviews of student proposals"""
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_given',
        limit_choices_to={'role__in': ['mentor', 'org_admin', 'admin']}
    )

    # Rating criteria (1-5 scale)
    technical_feasibility = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="How technically feasible is the proposal?"
    )
    understanding_of_project = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Does the student understand the project?"
    )
    implementation_quality = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Quality of the implementation plan"
    )
    timeline_realism = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Is the timeline realistic?"
    )
    student_capability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Student's capability based on experience"
    )

    # Overall assessment
    overall_score = models.FloatField(editable=False)  # Calculated average
    recommendation = models.CharField(
        max_length=20,
        choices=[
            ('strongly_accept', 'Strongly Accept'),
            ('accept', 'Accept'),
            ('neutral', 'Neutral'),
            ('reject', 'Reject'),
            ('strongly_reject', 'Strongly Reject'),
        ]
    )

    # Detailed feedback
    strengths = models.TextField()
    weaknesses = models.TextField()
    suggestions = models.TextField(blank=True)
    private_notes = models.TextField(
        blank=True,
        help_text="Notes visible only to other mentors/admins"
    )

    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        unique_together = ['proposal', 'reviewer']  # One review per reviewer per proposal

    def __str__(self):
        return f"Review by {self.reviewer.user.username} for {self.proposal.title}"

    def save(self, *args, **kwargs):
        # Calculate overall score as average of all ratings
        self.overall_score = (
            self.technical_feasibility +
            self.understanding_of_project +
            self.implementation_quality +
            self.timeline_realism +
            self.student_capability
        ) / 5.0
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Model for comments on proposals (discussion thread)"""
    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    content = models.TextField()
    is_internal = models.BooleanField(
        default=False,
        help_text="Internal comments visible only to mentors/admins"
    )
    is_edited = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.proposal.title}"


class ProjectTimeline(models.Model):
    """Model for tracking project milestones and progress (for accepted proposals)"""
    MILESTONE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]

    proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        related_name='milestones',
        limit_choices_to={'status': 'accepted'}
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    expected_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=MILESTONE_STATUS_CHOICES,
        default='pending'
    )

    # Progress tracking
    progress_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    deliverables = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    # Links to work
    pull_request_url = models.URLField(blank=True, null=True)
    documentation_url = models.URLField(blank=True, null=True)

    order = models.IntegerField(default=0, help_text="Order of milestone in timeline")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['proposal', 'order', 'expected_completion_date']
        verbose_name = 'Project Timeline'
        verbose_name_plural = 'Project Timelines'

    def __str__(self):
        return f"{self.title} - {self.proposal.title}"

    @property
    def is_overdue(self):
        """Check if milestone is overdue"""
        if self.status not in ['completed', 'cancelled']:
            return timezone.now().date() > self.expected_completion_date
        return False


class Notification(models.Model):
    """Model for user notifications"""
    NOTIFICATION_TYPES = [
        ('proposal_submitted', 'Proposal Submitted'),
        ('proposal_reviewed', 'Proposal Reviewed'),
        ('comment_added', 'Comment Added'),
        ('proposal_status_changed', 'Proposal Status Changed'),
        ('milestone_due', 'Milestone Due'),
        ('mention', 'Mentioned in Comment'),
    ]

    recipient = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()

    # Link to related object
    related_proposal = models.ForeignKey(
        Proposal,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    related_review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    related_comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.title} for {self.recipient.user.username}"

    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
