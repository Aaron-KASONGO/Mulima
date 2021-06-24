from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Row, Column
from django import forms
from django.forms import ModelForm
from .models import Person
from django.contrib.auth.hashers import make_password, check_password


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
            result = Person.objects.filter(username=username)
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
    date = forms.DateField(label='Date de naissance')

    class Meta:
        model = Person
        exclude = ('friends',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id_person'
        self.helper.form_action = 'register'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Register'))
        self.helper.layout = Layout(
            Column(Row(Column('first_name', css_class='col-sm-4 form-group'),
                       Column('last_name', css_class='col-sm-4 form-group'),
                       Column('username', css_class='col-sm-4 form-group'),
                       css_class='row'),
                   Row(Column('password', css_class='col-sm-6 form-group'),
                       Column('date', css_class='col-sm-6 form-group'),
                       css_class='row'),
                   Row(Column('email', css_class='col-sm-6 form-group'),
                       Column('cellphone_number', css_class='col-sm-6 form-group'),
                       css_class='row'),
                   'avatar',
                   css_class='col-sm-12')
        )

    def clean_username(self):
        query = Person.objects.all().values('username')
        username = self.cleaned_data.get('username')
        if len(query) != 0:
            usernames = [value for key, value in query[0].items()]
            if username in usernames:
                raise forms.ValidationError("Ce nom est déjà pris!")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if '%' in first_name:
            raise forms.ValidationError("Pas de % dans le nom!")
        return first_name

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
