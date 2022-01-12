from django.shortcuts import render, redirect
from .forms import NewUserForm, UserDetailsForm, UserDetailsUpdateForm, ClaimCaseForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import TemplateView
from django.views.generic.base import View
# from django.urls import reverse_lazy
import requests

# Create your views here.
from .models import UserDetails, Account, ClaimCase

from .helpers import (
    add_standalone_account,
    #    add_transaction,
)

from rest_framework import viewsets

from .serializers import ClaimCaseSerializer, UserDetailsSerializer
from .models import ClaimCase, UserDetails


def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'insureApp/index.html')


class RegisterView(TemplateView):
    template_name = 'registration/register.html'

    def get_context_data(self, **kwargs):
        ctx = super(RegisterView, self).get_context_data(**kwargs)
        ctx['user_form'] = NewUserForm(prefix='user')
        ctx['userdetails_form'] = UserDetailsForm(prefix='userdetails')
        return ctx

    def post(self, request, *args, **kwargs):
        user_form = NewUserForm(request.POST, prefix='user')
        userdetails_form = UserDetailsForm(request.POST, request.FILES, prefix='userdetails')
        if userdetails_form.is_valid() and user_form.is_valid():
            user = user_form.save(commit=False)
            userdetails = userdetails_form.save(commit=False)
            user.save()
            userdetails.user = user
            # create Algorand account
            private_key, address = add_standalone_account()
            account = Account.objects.create(address=address, private_key=private_key)
            userdetails.AlgoAddress = account
            userdetails.save()
            return redirect('login')
        else:
            return render(request=request, template_name='registration/register.html', context={'user_form': user_form})


# def UserDetailsUpdate(request):
#    t = request.user.userdetails.objects.get(id=1)
#    if request.method == 'POST':
#        userdetailsupdate_form = UserDetailsUpdateForm(request.POST)
#        if userdetailsupdate_form.is_valid():
#            userdetails = userdetailsupdate_form.save(commit=False)
#            t.firstname = userdetails.firstname
#            userdetails.save()
#        return redirect('index')
#    else:
#        messages.error(request, 'Unsuccessful userdetails update')
#    userdetailsupdate_form = UserDetailsUpdateForm()
#    return render(request=request, template_name='insureApp/userdetails_form.html', context={'userdetailsupdate_form': userdetailsupdate_form})

def LoginView(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, "registration/login.html", context)


def Logout(request):
    logout(request)
    return redirect('login')


def userdetails(request):
    loggedin_user = request.user.userdetails
    useruuid = loggedin_user.useruuid
    firstname = loggedin_user.firstname
    lastname = loggedin_user.lastname
    AlgoAddress = loggedin_user.AlgoAddress.address
    AlgoPrivateKey = loggedin_user.AlgoAddress.private_key
    gender = loggedin_user.gender
    dateofbirth = loggedin_user.dateofbirth
    driver_licence_state = loggedin_user.driver_licence_state
    driver_licence_number = loggedin_user.driver_licence_number

    context = {'useruuid': useruuid,
               'firstname': firstname,
               'lastname': lastname,
               'AlgoAddress': AlgoAddress,
               'AlgoPrivateKey': AlgoPrivateKey,
               'gender': gender,
               'dateofbirth': dateofbirth,
               'driver_licence_state': driver_licence_state,
               'driver_licence_number': driver_licence_number}
    return render(request, "insureApp/userdetails.html", context)


def create_standalone(request):
    """Create standalone account."""
    private_key, address = add_standalone_account()
    account = Account.objects.create(address=address, private_key=private_key)
    context = {"account": (address, account.passphrase)}
    return render(request, "insureApp/index.html", context)


# class UsernameView(generic.DetailView):
#    model = User

# class UserDetailView(generic.DetailView):
#	model = UserDetails

def call_api(request):
    response = requests.get('http://api.open-notify.org/astros.json')
    #	response = requests.get('https://api.cloudcheck.co.nz/')
    astros = response.json()
    return render(request, 'insureApp/api.html', {'astros': astros})


def response_api(request):
    if request == '200':
        response = 'Response code: 200. This is a valid driver license.'
    else:
        response = 'Response code: 200. This is a valid driver license.'
    context = {'response': response}
    return render(request, 'insureApp/response_api.html', context)


# class UserDetailsCreate(CreateView):
#    model = UserDetails
#    fields = ['firstname', 'lastname', 'dateofbirth', 'gender', 'driver_licence_state', 'driver_licence_number']

class UserDetailsUpdate(UpdateView):
    model = UserDetails
    fields = ['firstname', 'lastname', 'dateofbirth', 'gender', 'driver_licence_state', 'driver_licence_number']
    template_name = 'insureApp/userdetails_form.html'

def ClaimCaseCreate(request):
    form = ClaimCaseForm()

    if request.method == 'POST':
        form = ClaimCaseForm(request.POST)
        if form.is_valid():
            claim = form.save()
            claim_date = form.cleaned_data.get('reporteddate')
            #print(claim_date)

            claimCase = ClaimCase.objects.latest('casenumber')

            claimCase.claimuseruuid = request.user.userdetails.useruuid
            claimCase.save()

            context = {'claimCase': claimCase}
            return render(request, 'insureApp/claimcase_detail.html', context)
    context = {'form': form}
    return render(request, 'insureApp/claimcase_form.html', context)


"""
class ClaimCaseCreate(CreateView):
    model = ClaimCase
    fields = ['insurer', 'policynumber', 'casestatus', 'value', 'casecategory', 'reporteddate', 'claimnature']
    template_name = 'insureApp/claimcase_form.html'

    def post(self, request, *args, **kwargs):
        #claimcase_form = ClaimCaseForm(request.POST, prefix='claimcase')
        form = ClaimCaseForm(request.POST, prefix='claimcase')
        if form.is_valid():
            claimcase = form.save(commit=False)
            useruuid = request.user.userdetails.useruuid
            #print ('useruuid: ')
            #print (useruuid)
            insurer = request.POST.get('insurer')
            #print (insurer)
            claimcase.save()
            return redirect('index')
        else:
            return render(request=request, context={'form': form})
"""


class ClaimCaseDetailView(generic.DetailView):
    model = ClaimCase

class ClaimCaseViewSet(viewsets.ModelViewSet):
    queryset = ClaimCase.objects.all().order_by('casenumber')
    serializer_class = ClaimCaseSerializer


class UserDetailsViewSet(viewsets.ModelViewSet):
    queryset = UserDetails.objects.all().order_by('useruuid')
    serializer_class = UserDetailsSerializer

def about(request):
    return render(request, "insureApp/about.html")


def apidocs(request):
    return render(request, "insureApp/apidocs.html")


def contact(request):
    return render(request, "insureApp/contact.html")

# def register_request(request):
#	if request.method == 'POST':
#		form = NewUserForm(request.POST)
#		if form.is_valid():
#			 Save user credential
#			user = form.save()
#			login(request, user)

#			messages.success(request, 'Registration successful.')

#			 create Algorand account
#			private_key, address = add_standalone_account()
#			account = Account.objects.create(address=address, private_key=private_key)
#			context = {"account": (address, account.passphrase)}
#			context = {"account": address}
#			return render(request, "registration/login.html", context)
#			return redirect('login')
#		messages.error(request, 'Unsuccessful registration. Invalid information.')
#	form = NewUserForm()
#	return render (request=request, template_name='registration/register.html', context={'register_form':form})
