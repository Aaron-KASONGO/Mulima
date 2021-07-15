from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row
from django import forms
from django.contrib.auth.hashers import check_password
from django.forms import ModelForm
from django.contrib.auth.models import User


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
            result = User.objects.filter(username=username)
            clean_password = False
            if len(result) == 1:
                clean_password = check_password(password, result[0].password)
            if len(result) != 1 and not clean_password:
                raise forms.ValidationError("Adresse de courriel ou mot de passe erroné.")
        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '%' in username:
            raise forms.ValidationError("Ne doit pas contenir des %")
        return username


class PersonForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_person'
        self.helper.form_action = 'register'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.layout = Layout(
            Fieldset('<stong>Créer</strong> un compte', Row('username', css_class="mb-3"), Row('email', css_class="mb-3"), Row('password', css_class="mb-3"))
        )


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
