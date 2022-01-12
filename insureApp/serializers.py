from rest_framework import serializers

from .models import ClaimCase, UserDetails

class ClaimCaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ClaimCase
        fields = ('casenumber', 'casestatus', 'policynumber', 'value', 'riskscore', 'casecategory', 'reporteddate', 'claimnature')

class UserDetailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('useruuid', 'firstname', 'middlename', 'lastname', 'dateofbirth', 'gender', 'driver_licence_state', 'driver_licence_number')