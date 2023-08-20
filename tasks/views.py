from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView

from django.db.models import Q

from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormView
from django.views.generic.list import ListView

from .models import Task


# Create your views here.


class LoginUser(LoginView):
    template_name = 'tasks/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(FormView):
    template_name = 'tasks/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
        return super(RegisterUser, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('login')
        return super(RegisterUser, self).get(self, *args, **kwargs)


class TasksList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(owner=self.request.user)
        context['count'] = context['tasks'].filter(is_complete=False).count()

        q = self.request.GET.get('q') if self.request.GET.get('q') else ''

        context['q'] = q

        context['tasks'] = context['tasks'].filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'tasks/task_actions.html'
    fields = ['name', 'description']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'is_complete']
    template_name = 'tasks/task_actions.html'
    success_url = reverse_lazy('home')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    success_url = reverse_lazy('home')
