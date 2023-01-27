from django.urls import path
from .views_front import (
    ThingCreateView,
    ThingDeleteView,
    ThingDetailView,
    ThingListView,
    ThingUpdateView,
)

urlpatterns = [
    path("", ThingListView.as_view(), name="thing_list"),
    path("<int:pk>/", ThingDetailView.as_view(), name="thing_detail"),
    path("create/", ThingCreateView.as_view(), name="thing_create"),
    path("<int:pk>/update/", ThingUpdateView.as_view(), name="thing_update"),
    path("<int:pk>/delete/", ThingDeleteView.as_view(), name="thing_delete"),
]
