from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django import forms
from .models import Person
from django.contrib.auth.hashers import make_password


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'username'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'id': 'floatingPassword', 'placeholder': 'password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-loginForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'login'
        self.helper.add_input(Submit('submit', 'login', css_class='btn-success'))

        self.helper.layout = Layout(
            Fieldset('Login', 'username', 'password', style="color: grey;"))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            result = Person.objects.filter(password=password, username=username)
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")
        return cleaned_data


class PersonForm(forms.ModelForm):
    cellphone_number = forms.CharField(label='Numero de téléphone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-personForm'
        self.helper.form_method = 'post'
        self.helper.form_action = 'register'
        self.helper.add_input(Submit('submit', 'register', css_class='btn-success'))

        self.helper.layout = Layout(
            Fieldset('User Information', 'first_name', 'last_name', 'username', 'password', 'birth_date', style="color: grey;"),
            Fieldset('Contact Information', 'email', 'cellphone_number', 'avatar', style="color: grey;"))

    class Meta:
        model = Person
        exclude = ('friends',)

    def save(self, commit=True, *args, **kwargs):
        m = super().save(commit=False)
        m.password = make_password(self.cleaned_data.get('password'))

        if commit:
            m.save()
        return m


"""class AddFriendForm(forms.Form):
    email = forms.EmailField(label='Courriel')

    def clean(self):
        cleaned_data = super(AddFriendForm, self).clean()
        email = cleaned_data.get("email")

        #Verify the field is valid
        if email:
            result = Person.objects.filter(email=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse de courriel erronée.")
        return cleaned_data"""
