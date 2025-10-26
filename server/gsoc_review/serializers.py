from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Organization, UserProfile, Project, Proposal, 
    Review, Comment, ProjectTimeline, Notification
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for Organization model"""
    projects_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'website', 'logo_url', 
            'tech_stack', 'contact_email', 'is_active', 'year_joined',
            'projects_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_projects_count(self, obj):
        return obj.projects.count()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model"""
    user = UserSerializer(read_only=True)
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'role', 'bio', 'avatar_url', 'github_username',
            'linkedin_url', 'portfolio_url', 'university', 'degree', 
            'graduation_year', 'organization', 'organization_name', 'expertise',
            'phone_number', 'country', 'timezone', 'is_verified', 
            'full_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username


class UserProfileCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating UserProfile with User"""
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = UserProfile
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'role', 'bio', 'avatar_url', 'github_username', 'linkedin_url',
            'portfolio_url', 'university', 'degree', 'graduation_year',
            'organization', 'expertise', 'phone_number', 'country', 'timezone'
        ]
    
    def create(self, validated_data):
        # Extract user data
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile
        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile


class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Project list view"""
    organization_name = serializers.CharField(source='organization.name', read_only=True)
    mentors_count = serializers.SerializerMethodField()
    proposals_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'title', 'organization', 'organization_name', 'difficulty',
            'duration_weeks', 'status', 'year', 'mentors_count', 
            'proposals_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_mentors_count(self, obj):
        return obj.mentors.count()
    
    def get_proposals_count(self, obj):
        return obj.proposals.count()


class ProjectDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Project with all information"""
    organization = OrganizationSerializer(read_only=True)
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(),
        source='organization',
        write_only=True
    )
    mentors = UserProfileSerializer(many=True, read_only=True)
    mentor_ids = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.filter(role__in=['mentor', 'org_admin']),
        source='mentors',
        many=True,
        write_only=True
    )
    
    class Meta:
        model = Project
        fields = [
            'id', 'organization', 'organization_id', 'title', 'description',
            'expected_outcomes', 'skills_required', 'difficulty', 'duration_weeks',
            'mentors', 'mentor_ids', 'status', 'year', 'max_proposals',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ProposalListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for Proposal list view"""
    project_title = serializers.CharField(source='project.title', read_only=True)
    student_name = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()
    average_score = serializers.SerializerMethodField()
    
    class Meta:
        model = Proposal
        fields = [
            'id', 'project', 'project_title', 'student', 'student_name',
            'title', 'status', 'submitted_at', 'reviews_count', 
            'average_score', 'created_at'
        ]
        read_only_fields = ['id', 'submitted_at', 'created_at']
    
    def get_student_name(self, obj):
        return obj.student.user.get_full_name() or obj.student.user.username
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()
    
    def get_average_score(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(r.overall_score for r in reviews) / len(reviews), 2)
        return None


class ProposalDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Proposal with all information"""
    project = ProjectListSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
        source='project',
        write_only=True
    )
    student = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Proposal
        fields = [
            'id', 'project', 'project_id', 'student', 'title', 'abstract',
            'detailed_description', 'implementation_plan', 'timeline',
            'deliverables', 'prior_experience', 'why_this_project',
            'availability', 'status', 'submitted_at', 'reviewed_at',
            'proposal_document_url', 'github_repo_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'student', 'submitted_at', 'reviewed_at', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set student from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'profile'):
            validated_data['student'] = request.user.profile
        return super().create(validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model"""
    reviewer = UserProfileSerializer(read_only=True)
    proposal_title = serializers.CharField(source='proposal.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'proposal', 'proposal_title', 'reviewer', 
            'technical_feasibility', 'understanding_of_project',
            'implementation_quality', 'timeline_realism', 'student_capability',
            'overall_score', 'recommendation', 'strengths', 'weaknesses',
            'suggestions', 'private_notes', 'is_final', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'reviewer', 'overall_score', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set reviewer from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'profile'):
            validated_data['reviewer'] = request.user.profile
        return super().create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model"""
    author = UserProfileSerializer(read_only=True)
    author_name = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'proposal', 'author', 'author_name', 'parent', 'content',
            'is_internal', 'is_edited', 'replies_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'is_edited', 'created_at', 'updated_at']
    
    def get_author_name(self, obj):
        return obj.author.user.get_full_name() or obj.author.user.username
    
    def get_replies_count(self, obj):
        return obj.replies.count()
    
    def create(self, validated_data):
        # Set author from request user
        request = self.context.get('request')
        if request and hasattr(request.user, 'profile'):
            validated_data['author'] = request.user.profile
        return super().create(validated_data)


class ProjectTimelineSerializer(serializers.ModelSerializer):
    """Serializer for ProjectTimeline model"""
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = ProjectTimeline
        fields = [
            'id', 'proposal', 'title', 'description', 'expected_completion_date',
            'actual_completion_date', 'status', 'progress_percentage',
            'deliverables', 'notes', 'pull_request_url', 'documentation_url',
            'order', 'is_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model"""
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'title', 'message',
            'related_proposal', 'related_review', 'related_comment',
            'is_read', 'read_at', 'created_at'
        ]
        read_only_fields = ['id', 'recipient', 'read_at', 'created_at']

