#sayeed - sayeed -- > superuser
#john - john@123
#testuser - test@123

from django.shortcuts import render ,redirect
from django.http import HttpResponse
from django.views.generic import ListView ,DetailView , CreateView,UpdateView ,DeleteView,FormView
from platformdirs import user_config_path
from .models import *
from django.contrib.auth.views import LoginView,LogoutView 
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import * 
# Create your views here.

class TaskList(LoginRequiredMixin , ListView) : # by default looks for modelname_list.html if not specified
    model = Task
    context_object_name = 'tasks'
    template_name = 'base/task.html'

    def get_context_data(self  ,**kwargs): #overriding method to ensure user see's only his tasks
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(completed = False).count()
        search_text =''
        if 'search-area' in self.request.GET :  # or can do search_text = self.req.GET.get('search-area')
            search_text = self.request.GET['search-area'] 
        print("Search text  =  " ,  str(search_text))
        if search_text is not None : 
            context['tasks'] = context['tasks'].filter(title__icontains=search_text)
        return context

class TaskDetail(LoginRequiredMixin, DetailView) : # will look for TaskList_detail
    model = Task
    context_object_name = 'task'

class TaskCreate( LoginRequiredMixin , CreateView) : # by default looks for model_form.html
    model = Task
    fields  =['title' ,'description']
    # template_name = 'base/task_create.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self , form) : 
        form.instance.user = self.request.user
        return super(TaskCreate ,self) .form_valid(form) 

class TaskUpdate( LoginRequiredMixin ,UpdateView):
    model = Task 
    fields ='__all__'
    success_url = reverse_lazy('tasks')

class TaskDelete( LoginRequiredMixin,DeleteView): #default template model_confirm_deletes
    model = Task
    context_object_name ='task'
    # template_name ='base/task_delete.html'
    success_url = reverse_lazy('tasks')

class CustomLoginView(LoginView) : 
    fields ='__all__'
    template_name ='base/login.html'
    redirect_authenticated_user = True
    # success_url = reverse_lazy('tasks') # doesnt_work

    # def get_success_url(self) : 
    #     return reverse_lazy('tasks')
    
    def form_valid(self ,form) : 
        messages.success(self.request , "Logged in successfully" )
        return super(CustomLoginView , self).form_valid(form)
    
    def form_invalid(self ,form) : 
        name = form.cleaned_data.get('username')
        set = User.objects.filter(username = name)
        if len(set) == 0: 
            messages.warning(self.request , "Incorrect Username ")
        else : 
            messages.warning(self.request , "Incorrect Password")
        return super(CustomLoginView ,self).form_invalid(form)


class CustomLogoutView(LogoutView) : 
    next_page ='login'


class RegisterPage(FormView) : 
    template_name = 'base/register.html'
    form_class = UserForm
    success_url = reverse_lazy('login')

    def form_valid(self ,form) : 
        user  = form.save()
        print("Registered with username " , str(user))
        if user is not None : 
            login(self.request ,user)            
        return super(RegisterPage , self).form_valid(form)

    def get(self ,*args , **kwargs) : 
        if self.request.user.is_authenticated : 
            return redirect('tasks')
        return super(RegisterPage ,self).get(*args ,**kwargs)
    
    def form_invalid(self, form):
        return super(RegisterPage ,self).form_invalid(form)