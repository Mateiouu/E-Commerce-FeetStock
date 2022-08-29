from re import template
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from store.forms import EditProfileForm
from store.models import *
import json
from django.views.generic import CreateView
from store.forms import CreateUserForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views import generic

# Create your views here.


def loginView(request):
    if request.method =='POST':
           miFormulario=AuthenticationForm(request, data=request.POST)#aquí mellega toda la información del html
           

           if miFormulario.is_valid():#Si pasó la validación de Django
                data=miFormulario.cleaned_data

                usuario = data['username']
                psw = data['password']
               
                user = authenticate(username=usuario, password=psw)
                if user:
                    login(request,user)
                    return render(request, 'store/homee.html', {'mensaje': f'Bienvenido {usuario}'})
                
                else:

                    return render(request, 'store/homee.html', {'mensaje': 'No se ha podido iniciar sesion, revise sus datos'})
           return render(request, 'store/homee.html', {'mensaje': 'Formulario invalido'})
    else:
        miFormulario=AuthenticationForm()

    return render(request, 'login.html', {'miFormulario': miFormulario})

def registerView(request):
   
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            context = {'form': form}
            return render(request, 'store/homee.html', context)
    else:

        form = CreateUserForm()

    return render(request, 'register.html', {'form': form})


class CambiarContraView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'editar_perfil.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user


@login_required(login_url = 'login')
def userpage(request):
    customer=Customer.objects.get(user=request.user)
    orders = customer.order_set.all()
    


    context = {'orders': orders}
    return render(request, 'orders.html', context)

