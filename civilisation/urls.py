from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from civilisation import views

app_name = 'civilisation'

urlpatterns = [
    path('company/employees/<str:company_id>/', views.CompanyEmployees.as_view(), name='company-employees'),
    path('citizen/<str:person_1_id>/common-friends/<str:person_2_id>/', views.CitizenMutualFriends.as_view(),
         name='citizen-mutual-friends'),
    path('citizen/favourite-food/<str:person_1_id>/', views.CitizenFavouriteFoodOverview.as_view(),
         name='citizen-favourite-food'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
