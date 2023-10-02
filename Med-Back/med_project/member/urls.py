from django.urls import path ,include
from .views import UserMedViewSet
from rest_framework import routers



router=routers.DefaultRouter()

router.register(r'usermed',UserMedViewSet)

urlpatterns = [
    path('',include(router.urls))
]
