from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from arcanaapi.views import register_user, login_user
from arcanaapi.views import Cards, Readings, Comments



router = routers.DefaultRouter(trailing_slash=False)
router.register(r'cards', Cards, 'card')
router.register(r'readings', Readings, 'reading')
router.register(r'comments', Comments, 'comments')


urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

