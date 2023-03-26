import imp
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from . import views
from rest_framework.authtoken.views import obtain_auth_token, ObtainAuthToken

app_name = "leadconversion"

router = routers.DefaultRouter()
router.register("lead_conversion", views.LeadViewSet)
router.register("register", views.UserRoleViewSet)
router.register('products', views.ProductViewSet)
router.register('customer_creation', views.CustomerViewSet)
router.register('user', views.UserRoleAuth)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', ObtainAuthToken.as_view())

]
