from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
from .models import UserDetails, ClaimCase

# Define the admin class
class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('useruuid', 'firstname', 'lastname', 'dateofbirth', 'AlgoAddress')
    #fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

# Register the admin class with the associated model
admin.site.register(UserDetails, UserDetailsAdmin)

class ClaimCaseAdmin(admin.ModelAdmin):
    list_display = ('casenumber', 'claimuseruuid', 'casestatus', 'policynumber', 'value', 'riskscore', 'casecategory', 'reporteddate', 'claimnature')

# Register the admin class with the associated model
admin.site.register(ClaimCase, ClaimCaseAdmin)