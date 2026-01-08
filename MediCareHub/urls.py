from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('patients.urls')),
    path('api/', include('appointments.urls')),
    path("api/auth/", include("accounts.urls")),
    path('api/', include('consultations.urls')),
    path('api/', include('prescriptions.urls')),

]
