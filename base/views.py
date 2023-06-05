from asyncio import tasks
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage
from .models import Task
from django.http import HttpResponse
from django.urls import reverse_lazy
from django import template


# Create your views here.
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

class CustomLoginView(LoginView):
    fields = '__all__'
    redirect_authenticated_user = True
    template_name = 'base/login.html'

    def get_success_url(self):
        return reverse_lazy('tasklist')


class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'base/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)


    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('taskslist')
        return super(RegisterView, self).get(*args, **kwargs)



class Tasklist(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
     

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(completed=False).count()
       
       
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
            context['search_input'] = search_input
        return context
        


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task_detail.html' 


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'completed']
    success_url = reverse_lazy('tasklist')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class  TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =  ['title', 'description', 'completed']
    success_url = reverse_lazy('tasklist')


class  TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasklist')
