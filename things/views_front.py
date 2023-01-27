from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Thing


class ThingListView(LoginRequiredMixin, ListView):
    template_name = "things/thing_list.html"
    model = Thing
    context_object_name = "things"


class ThingDetailView(LoginRequiredMixin, DetailView):
    template_name = "things/thing_detail.html"
    model = Thing


class ThingUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "things/thing_update.html"
    model = Thing
    fields = "__all__"


class ThingCreateView(LoginRequiredMixin, CreateView):
    template_name = "things/thing_create.html"
    model = Thing
    fields = ["name", "rating", "reviewer"] # "__all__" for all of them


class ThingDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "things/thing_delete.html"
    model = Thing
    success_url = reverse_lazy("thing_list")
