from algosdk.constants import address_len, hash_len, max_asset_decimals, metadata_length
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.core.validators import MaxValueValidator, MinValueValidator
#from .helpers import account_balance, account_transactions, passphrase_from_private_key
from .helpers import passphrase_from_private_key
from django.urls import reverse
import uuid

# Algorand Account Model
class Account(models.Model):
    """Base model class for standalone and wallet Algorand accounts."""
    address = models.CharField(primary_key=True, max_length=address_len)
    username = models.ForeignKey('UserDetails', on_delete=models.RESTRICT, null=True)
    private_key = models.CharField(max_length=address_len + hash_len)
    accountcreated = models.DateTimeField(auto_now_add=True)

    @classmethod
    def instance_from_address(cls, address):
        """Return model instance from provided account address."""
        try:
            return cls.objects.get(address=address)
        except ObjectDoesNotExist:
            raise Http404

#    def balance(self):
#        """Return this instance's balance in microAlgos."""
#        return account_balance(self.address)

    @property
    def passphrase(self):
        """Return account's mnemonic."""
        return passphrase_from_private_key(self.private_key)

#    def transactions(self):
#        """Return all the transactions involving this account."""
#        return account_transactions(self.address)

    def __str__(self):
        """Account's human-readable string representation."""
        return self.address

# Create your User Details models here.
class UserDetails(models.Model):
    """Model representing a user credential."""
    useruuid = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for each user')
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200, null=True)
    lastname = models.CharField(max_length=200, null=True)
    dateofbirth = models.DateField(null=True, blank=True)
    AlgoAddress = models.ForeignKey(Account, on_delete=models.RESTRICT, null=True)

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER,
        blank=True,
    )

    DRIVER_LICENCE_STATE = (
        ('ACT', 'ACT'),
        ('NSW', 'NSW'),
        ('NT', 'NT'),
        ('QLD', 'QLD'),
        ('VIC', 'VIC'),
        ('WA', 'WA'),
    )

    driver_licence_state = models.CharField(
        max_length=3,
        choices=DRIVER_LICENCE_STATE,
        blank=True,
    )

    driver_licence_number = models.CharField(max_length=10, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.firstname}, {self.lastname}, {self.dateofbirth}, {self.AlgoAddress}'

    def get_absolute_url(self):
        return reverse('userdetails')

# Define Claim Case model
class ClaimCase(models.Model):
    """Model representing a user credential."""
    casenumber = models.AutoField(primary_key=True)
    #UserDetails = models.ForeignKey(UserDetails, on_delete=models.SET_NULL, null=True)
    claimuseruuid = models.CharField(max_length=200, null=True, blank=True)
    insurer = models.CharField(max_length=200, null=True, blank=True)

    CASE_STATUS = (
        ('OPEN', 'Open'),
        ('REVIEW', 'Review'),
        ('CLOSED', 'Closed'),
        ('REJECTED', 'Rejected'),
    )

    casestatus = models.CharField(
        max_length=10,
        choices=CASE_STATUS,
        blank=True,
    )

    policynumber = models.CharField(max_length=200, null=True, blank=True)
    value = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    riskscore = models.IntegerField(blank=True, null=True, validators=[MinValueValidator(1), MaxValueValidator(100)], help_text='Risk Score between 0 - 100')

    CASE_CATEGORY = (
        ('MOTOR', 'Motorvehicle'),
        ('HOUSE', 'House'),
        ('CONTENT', 'Content'),
    )

    casecategory = models.CharField(
        max_length=10,
        choices=CASE_CATEGORY,
        blank=True,
    )

    reporteddate = models.CharField(max_length=20, null=True, blank=True)
    claimnature = models.CharField(max_length=200, null=True, blank=True)

    #@property
    #def retrieve_useruuid(self):
    #    return self.userdetails.useruuid
    #    useruuid = retrieve_useruuid()

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.casenumber}, {self.claimuseruuid}, {self.insurer}, {self.casestatus}, {self.policynumber}, {value}, {riskscore}, {casecategory}, {reporteddate}, {claimnature}'