from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet, UserProfileViewSet, ProjectViewSet,
    ProposalViewSet, ReviewViewSet, CommentViewSet,
    ProjectTimelineViewSet, NotificationViewSet
)

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'proposals', ProposalViewSet, basename='proposal')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'timelines', ProjectTimelineViewSet, basename='timeline')
router.register(r'notifications', NotificationViewSet, basename='notification')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

