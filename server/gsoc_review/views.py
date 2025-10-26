from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import (
    Organization, UserProfile, Project, Proposal,
    Review, Comment, ProjectTimeline, Notification
)
from .serializers import (
    OrganizationSerializer, UserProfileSerializer, UserProfileCreateSerializer,
    ProjectListSerializer, ProjectDetailSerializer,
    ProposalListSerializer, ProposalDetailSerializer,
    ReviewSerializer, CommentSerializer, ProjectTimelineSerializer,
    NotificationSerializer
)


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Organization CRUD operations.

    list: Get all organizations
    retrieve: Get a specific organization
    create: Create a new organization (admin only)
    update: Update an organization (admin only)
    destroy: Delete an organization (admin only)
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'description', 'tech_stack']
    ordering_fields = ['name', 'year_joined', 'created_at']
    filterset_fields = ['is_active', 'year_joined']

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """Get all projects for this organization"""
        organization = self.get_object()
        projects = organization.projects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members (mentors/admins) of this organization"""
        organization = self.get_object()
        members = organization.members.all()
        serializer = UserProfileSerializer(members, many=True)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile CRUD operations.

    list: Get all user profiles
    retrieve: Get a specific user profile
    create: Create a new user profile with user account
    update: Update a user profile
    destroy: Delete a user profile
    """
    queryset = UserProfile.objects.select_related('user', 'organization').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'bio']
    ordering_fields = ['created_at', 'user__username']
    filterset_fields = ['role', 'organization', 'is_verified']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserProfileCreateSerializer
        return UserProfileSerializer

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        try:
            profile = request.user.profile
            serializer = self.get_serializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(
                {'error': 'Profile not found for current user'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        """Get all proposals by this user (if student)"""
        profile = self.get_object()
        if profile.role != 'student':
            return Response(
                {'error': 'Only students have proposals'},
                status=status.HTTP_400_BAD_REQUEST
            )
        proposals = profile.proposals.all()
        serializer = ProposalListSerializer(proposals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews given by this user (if mentor)"""
        profile = self.get_object()
        if profile.role not in ['mentor', 'org_admin', 'admin']:
            return Response(
                {'error': 'Only mentors can give reviews'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reviews = profile.reviews_given.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Project CRUD operations.

    list: Get all projects
    retrieve: Get a specific project
    create: Create a new project
    update: Update a project
    destroy: Delete a project
    """
    queryset = Project.objects.select_related('organization').prefetch_related('mentors').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'description', 'skills_required']
    ordering_fields = ['created_at', 'year', 'title']
    filterset_fields = ['organization', 'difficulty', 'status', 'year']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectDetailSerializer

    @action(detail=True, methods=['get'])
    def proposals(self, request, pk=None):
        """Get all proposals for this project"""
        project = self.get_object()
        proposals = project.proposals.all()
        serializer = ProposalListSerializer(proposals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_year(self, request):
        """Get projects filtered by year"""
        year = request.query_params.get('year')
        if not year:
            return Response(
                {'error': 'Year parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        projects = self.queryset.filter(year=year)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)


class ProposalViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Proposal CRUD operations.

    list: Get all proposals
    retrieve: Get a specific proposal
    create: Create a new proposal
    update: Update a proposal
    destroy: Delete a proposal
    """
    queryset = Proposal.objects.select_related('project', 'student').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'abstract', 'detailed_description']
    ordering_fields = ['created_at', 'submitted_at', 'status']
    filterset_fields = ['project', 'student', 'status']

    def get_serializer_class(self):
        if self.action == 'list':
            return ProposalListSerializer
        return ProposalDetailSerializer

    def get_queryset(self):
        """Filter proposals based on user role"""
        user = self.request.user
        if not hasattr(user, 'profile'):
            return Proposal.objects.none()

        profile = user.profile

        # Students see only their own proposals
        if profile.role == 'student':
            return self.queryset.filter(student=profile)

        # Mentors see proposals for their projects
        elif profile.role in ['mentor', 'org_admin']:
            return self.queryset.filter(
                project__mentors=profile
            ).distinct()

        # Admins see all proposals
        elif profile.role == 'admin':
            return self.queryset

        return Proposal.objects.none()

    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a proposal (change status from draft to submitted)"""
        proposal = self.get_object()

        # Only the student who created it can submit
        if proposal.student != request.user.profile:
            return Response(
                {'error': 'You can only submit your own proposals'},
                status=status.HTTP_403_FORBIDDEN
            )

        if proposal.status != 'draft':
            return Response(
                {'error': 'Only draft proposals can be submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        proposal.submit()
        serializer = self.get_serializer(proposal)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for this proposal"""
        proposal = self.get_object()
        reviews = proposal.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for this proposal"""
        proposal = self.get_object()
        comments = proposal.comments.filter(parent__isnull=True)  # Top-level comments only
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def timeline(self, request, pk=None):
        """Get timeline/milestones for this proposal"""
        proposal = self.get_object()
        if proposal.status != 'accepted':
            return Response(
                {'error': 'Only accepted proposals have timelines'},
                status=status.HTTP_400_BAD_REQUEST
            )
        milestones = proposal.milestones.all()
        serializer = ProjectTimelineSerializer(milestones, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review CRUD operations.

    list: Get all reviews
    retrieve: Get a specific review
    create: Create a new review
    update: Update a review
    destroy: Delete a review
    """
    queryset = Review.objects.select_related('proposal', 'reviewer').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at', 'overall_score']
    filterset_fields = ['proposal', 'reviewer', 'recommendation', 'is_final']

    def get_queryset(self):
        """Filter reviews based on user role"""
        user = self.request.user
        if not hasattr(user, 'profile'):
            return Review.objects.none()

        profile = user.profile

        # Mentors and admins see all reviews
        if profile.role in ['mentor', 'org_admin', 'admin']:
            return self.queryset

        # Students see reviews for their proposals
        elif profile.role == 'student':
            return self.queryset.filter(proposal__student=profile)

        return Review.objects.none()

    def perform_create(self, serializer):
        """Ensure only mentors can create reviews"""
        if self.request.user.profile.role not in ['mentor', 'org_admin', 'admin']:
            raise PermissionError('Only mentors can create reviews')
        serializer.save()


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment CRUD operations.

    list: Get all comments
    retrieve: Get a specific comment
    create: Create a new comment
    update: Update a comment
    destroy: Delete a comment
    """
    queryset = Comment.objects.select_related('author', 'proposal').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    filterset_fields = ['proposal', 'author', 'is_internal', 'parent']

    def get_queryset(self):
        """Filter comments based on visibility"""
        user = self.request.user
        if not hasattr(user, 'profile'):
            return Comment.objects.none()

        profile = user.profile

        # Mentors and admins see all comments including internal
        if profile.role in ['mentor', 'org_admin', 'admin']:
            return self.queryset

        # Students see only non-internal comments on their proposals
        elif profile.role == 'student':
            return self.queryset.filter(
                proposal__student=profile,
                is_internal=False
            )

        return Comment.objects.none()

    @action(detail=True, methods=['get'])
    def replies(self, request, pk=None):
        """Get all replies to this comment"""
        comment = self.get_object()
        replies = comment.replies.all()
        serializer = self.get_serializer(replies, many=True)
        return Response(serializer.data)


class ProjectTimelineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ProjectTimeline CRUD operations.

    list: Get all milestones
    retrieve: Get a specific milestone
    create: Create a new milestone
    update: Update a milestone
    destroy: Delete a milestone
    """
    queryset = ProjectTimeline.objects.select_related('proposal').all()
    serializer_class = ProjectTimelineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['order', 'expected_completion_date', 'created_at']
    filterset_fields = ['proposal', 'status']

    def get_queryset(self):
        """Filter milestones based on user access to proposal"""
        user = self.request.user
        if not hasattr(user, 'profile'):
            return ProjectTimeline.objects.none()

        profile = user.profile

        # Students see milestones for their accepted proposals
        if profile.role == 'student':
            return self.queryset.filter(proposal__student=profile)

        # Mentors see milestones for proposals they're mentoring
        elif profile.role in ['mentor', 'org_admin']:
            return self.queryset.filter(
                proposal__project__mentors=profile
            ).distinct()

        # Admins see all milestones
        elif profile.role == 'admin':
            return self.queryset

        return ProjectTimeline.objects.none()

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        """Get all overdue milestones"""
        today = timezone.now().date()
        milestones = self.get_queryset().filter(
            expected_completion_date__lt=today,
            status__in=['pending', 'in_progress', 'delayed']
        )
        serializer = self.get_serializer(milestones, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        """Mark a milestone as completed"""
        milestone = self.get_object()
        milestone.status = 'completed'
        milestone.actual_completion_date = timezone.now().date()
        milestone.progress_percentage = 100
        milestone.save()
        serializer = self.get_serializer(milestone)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Notification CRUD operations.

    list: Get all notifications for current user
    retrieve: Get a specific notification
    create: Create a new notification (admin only)
    update: Update a notification
    destroy: Delete a notification
    """
    queryset = Notification.objects.select_related('recipient').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['created_at']
    filterset_fields = ['notification_type', 'is_read']

    def get_queryset(self):
        """Users see only their own notifications"""
        user = self.request.user
        if hasattr(user, 'profile'):
            return self.queryset.filter(recipient=user.profile)
        return Notification.objects.none()

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read for current user"""
        notifications = self.get_queryset().filter(is_read=False)
        count = notifications.count()
        for notification in notifications:
            notification.mark_as_read()
        return Response({'marked_read': count})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})
