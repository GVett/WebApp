from django.views.generic import FormView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.conf import settings

from project.user.forms import SignInForm, ProfileForm

from project.coffee.mixins import FormMixin
    
class SignInView(FormView, FormMixin):
    form_class = SignInForm
    success_url = '/'
    
    def get_form(self, *args):
        form = super(SignInView, self).get_form(self.get_form_class())
        fields = form.fields
        
        field = 'username' if 'username' in fields.keys() else 'email'
        
        placeholders = {
            field: field.title(),
            'password': 'Password',
        }
        
        self.construct_widgets(fields, placeholders)
        
        return form
        
    def form_valid(self, form):
        response = super(SignInView, self).form_valid(form)
        
        auth_login(self.request, form.get_user())
        
        message = getattr(
                settings,
                'USER_MESSAGE_SIGN_IN',
                'Signed In!')
                
        messages.add_message(self.request, messages.SUCCESS, message)
        
        return HttpResponseRedirect(self.request.POST.get('next') or self.request.GET.get('next') or reverse('profile'))
        
        
class SignUpView(FormView, FormMixin):
    form_class = UserCreationForm
    success_url = '/'
    
    def get_form(self, *args):
        form = super(SignUpView, self).get_form(self.get_form_class())
        fields = form.fields
        
        placeholders = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        
        self.construct_widgets(fields, placeholders)
        
        return form
        
    def form_valid(self, form):
        form.save()
        
        self.success_url = reverse('profile')
        
        response = super(SignUpView, self).form_valid(form)
        
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
                            
        auth_login(self.request, user)
        
        message = getattr(
                settings,
                'USER_MESSAGE_SIGN_UP',
                'Signed up!')
                
        messages.add_message(self.request, messages.SUCCESS, message)
        
        return response
 
 
class ProfileView(FormView, FormMixin):
    form_class = ProfileForm
    success_url = '/'
    
    def get_form(self, *args):
        self.success_url = reverse('profile')
        form = super(ProfileView, self).get_form(self.get_form_class())
        fields = form.fields
        user = self.request.user
        
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address'
        }
        
        initial = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username
        }
        
        form.initial = initial
        
        self.construct_widgets(fields, placeholders)
        
        return form
    
    
    def form_valid(self, form):
        response = super(ProfileView, self).form_valid(form)
        
        form.save(self.request.user)
        
        message = getattr(
                settings,
                'USER_MESSAGE_PROFILE',
                'Profile changed!')
                
        messages.add_message(self.request, messages.SUCCESS, message)
        
        return response

class PasswordChangeView(FormView, FormMixin):
    form_class = PasswordChangeForm
    success_url = '/'
    
    def get_form(self, *args):
        self.success_url = reverse('profile')
        form = self.get_form_class()(self.request.user, self.request.POST if self.request.POST else None)
        fields = form.fields
        user = self.request.user
        
        placeholders = {
            'old_password': 'Old Password',
            'new_password1': 'New Password',
            'new_password2': 'Confirm New Password'
        }
        
        self.construct_widgets(fields, placeholders)
        
        return form
    
    def form_valid(self, form):
        response = super(PasswordChangeView, self).form_valid(form)
        
        form.save()
        
        message = getattr(
                settings,
                'USER_MESSAGE_CHANGE_PASSWORD',
                'Password changed!')
        
        messages.add_message(self.request, messages.SUCCESS, message)
        
        return response