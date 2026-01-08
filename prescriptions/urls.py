from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrdonnanceListCreate.as_view(), name='ordonnance-list-create'),
    path('<int:pk>/', views.OrdonnanceDetail.as_view(), name='ordonnance-detail'),
    path('patient/<int:patient_id>/', views.OrdonnancesByPatient.as_view(), name='ordonnances-by-patient'),
]
