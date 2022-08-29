
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.forms import ModelForm
from .models import Product



# class CustomerFormulario(forms.Form):

#     user = forms.CharField(max_length = 40)
#     email = forms.EmailField(max_length = 40)
#     password = forms.PasswordInput(min_length = 8)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2', 'email']:
            self.fields[fieldname].help_text = None

    


# class PasswordChangingForm(PasswordChangeForm):

class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(widget = forms.EmailInput(attrs = {'class': 'form-control'}))
    first_name = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control'}))
    username = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control'}))
    last_name = forms.CharField(widget = forms.TextInput(attrs = {'class': 'form-control'}))
   
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProductoFormulario(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
   
     
