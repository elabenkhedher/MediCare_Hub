from django.urls import path
from . import views

urlpatterns = [
    # Explicit patterns for trailing slash compatibility
    path('ordonnances/', views.OrdonnanceListCreate.as_view(), name='ordonnance-list-create'),
    path('ordonnances', views.OrdonnanceListCreate.as_view(), name='ordonnance-list-create-no-slash'),
    path('ordonnances/<int:pk>/', views.OrdonnanceDetail.as_view(), name='ordonnance-detail'),
    path('ordonnances/<int:pk>', views.OrdonnanceDetail.as_view(), name='ordonnance-detail-no-slash'),
    path('ordonnances/patient/<int:patient_id>/', views.OrdonnancesByPatient.as_view(), name='ordonnances-by-patient'),
    path('ordonnances/patient/<int:patient_id>', views.OrdonnancesByPatient.as_view(), name='ordonnances-by-patient-no-slash'),
    path('medications/', views.MedicationList.as_view(), name='medication-list'),
    path('medications', views.MedicationList.as_view(), name='medication-list-no-slash'),
]
