import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from .models import UserDetails, ClaimCase
from django.core.exceptions import ValidationError


# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserDetailsForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = ('firstname', 'lastname')


class UserDetailsUpdateForm(ModelForm):
    class Meta:
        model = UserDetails
        fields = ('firstname', 'lastname', 'dateofbirth', 'gender', 'driver_licence_state', 'driver_licence_number')

#    def clean_dateofbirth(self):
#        data = self.cleaned_data['dateofbirth']

        # Check if a date is not in the past.
#        if data > datetime.date.today():
#            raise ValidationError(_('Date of Birth can not be future dated'))

        # Remember to always return the cleaned data.
#        return data

class ClaimCaseForm(ModelForm):
    class Meta:
        model = ClaimCase
        fields = '__all__'
        exclude = ['claimuseruuid','casestatus','value','riskscore']
        #fields = ['insurer', 'policynumber', 'casestatus', 'value', 'casecategory', 'reporteddate', 'claimnature']
    """
    def save(self, commit=True):
        claimcase = super(ClaimCaseForm, self).save(commit=False)
        #user.email = self.cleaned_data['email']
        if commit:
            claimcase.save()
        return claimcase
    """