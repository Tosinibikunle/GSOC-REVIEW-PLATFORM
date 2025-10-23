
from django.urls import path
from .views import ProposalListCreateView, ProposalDetailView

urlpatterns = [
    path('proposals/', ProposalListCreateView.as_view(), name='proposal-list-create'),
    path('proposals/<int:pk>/', ProposalDetailView.as_view(), name='proposal-detail'),
]
