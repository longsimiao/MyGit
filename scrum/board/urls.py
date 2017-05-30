from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'sprint', views.SprintViewSet)
router.register(r'tasks', views.TaskViewSet)
router.register(r'users', views.UserViewSet)
