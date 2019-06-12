from django.conf.urls import url
from rest_framework import routers
# from project.appname.views import UniversityViewSet
from quickstart.views import UniversityViewSet
 
router = routers.DefaultRouter()
router.register(r'universities', UniversityViewSet)
 
urlpatterns = router.urls