from django.urls import include, path
from . import views
from rest_framework import routers
#from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()
router.register(r'claimcaseapi', views.ClaimCaseViewSet)

router2 = routers.DefaultRouter()
router2.register(r'userdetailsapi', views.UserDetailsViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    #path('^login/', auth_views.login, {'template_name': 'registration/login2.html'}),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('algorand', views.create_standalone, name='algorand'),
    path('api', views.call_api, name='api'),
    path('response_api/', views.response_api, name='response_api'),
    path('userdetails/', views.userdetails, name='userdetails'),
    path('userdetailsupdate/<pk>', views.UserDetailsUpdate.as_view(), name='userdetailsupdate'),
    path('claimcase/', views.ClaimCaseCreate, name='claimcase'),
    path('displayclaimcase/<int:pk>', views.ClaimCaseDetailView.as_view(), name='displayclaimcase'),
    path('claimcaseapi/', include(router.urls)),
    path('userdetailsapi/', include(router2.urls)),
    path('about', views.about, name='about'),
    path('apidocs', views.apidocs, name='apidocs'),
    path('contact', views.contact, name='contact'),
]