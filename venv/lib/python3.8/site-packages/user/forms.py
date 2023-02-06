from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.conf import settings
from django.forms import CharField, ValidationError
from django.contrib.auth import authenticate

class SignInForm(AuthenticationForm):
    backends = getattr(
                settings,
                'AUTHENTICATION_BACKENDS',
                [])
                
    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)
        
        self.field = 'username'
        
        if 'username' in self.fields.keys() and 'user.backends.EmailAuthBackend' in self.backends:
            del self.fields['username']
            self.field = 'email'
            
        if 'email' not in self.fields.keys() and 'user.backends.EmailAuthBackend' in self.backends:
            self.fields.insert(0, 'email', CharField(max_length=255))
            self.field = 'email'
            
    def clean(self):
        field = self.cleaned_data.get(self.field)
        password = self.cleaned_data.get('password')

        message = getattr(
                settings,
                'USER_MESSAGE_SIGN_IN_ERROR',
                'Incorrect login!')
                
        if field and password:
            if self.field == 'username':
                self.user_cache = authenticate(username=field, password=password)
            else:    
                self.user_cache = authenticate(email=field, password=password)
                
            if self.user_cache is None or not self.user_cache.is_active:
                self._errors['%s: ' % self.field] = message
                return self.cleaned_data
                
        return self.cleaned_data
        
class ProfileForm(UserChangeForm):
    def save(self, *args):
        user_session = args[0]
        
        user_session.first_name = self.cleaned_data['first_name']
        user_session.last_name = self.cleaned_data['last_name']
        user_session.email = self.cleaned_data['email']
            
        user_session.save()