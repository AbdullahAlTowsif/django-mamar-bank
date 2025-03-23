from django.contrib.auth.forms import UserCreationForm
from . constants import GENDER_TYPE, ACCOUNT_TYPE
from django import forms
from django.contrib.auth.models import User
from . models import UserBankAccount, UserAddress


# combined three models (django built-in user, UserBankAccount, UserAddress) data and converted to one form
class UserRegistrationForm(UserCreationForm):
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'account_type', 'birth_date', 'gender', 'postal_code', 'city', 'country', 'street_address']
        
    def save(self, commit = True):
        the_user = super().save(commit=False) # ami database e data save korbona ekhn
        if commit == True:
            the_user.save() # user model e data save krlam
            # user theke data nichhi
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
            
            UserAddress.objects.create(
                user = the_user,
                postal_code = postal_code,
                country = country,
                city = city,
                street_address = street_address,
            )
            UserBankAccount.objects.create(
                user = the_user,
                account_type = account_type,
                gender = gender,
                birth_date = birth_date,
                account_no = 100000 + the_user.id,
            )
        return the_user