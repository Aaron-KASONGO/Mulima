from django import forms
from .models import Person


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'floatingInput', 'placeholder': 'username'}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'floatingPassword', 'placeholder': 'password'}))

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
    class Meta:
        model = Person
        exclude = ('friends',)



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