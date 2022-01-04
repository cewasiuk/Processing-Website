from django.urls import path, re_path, include
from . import views
from .forms import RequestForm, GrindRequestForm, DicingRequestForm,  SurveyForm1, SurveyForm2, SurveyForm3

# survey_forms = [SurveyForm1, SurveyForm2, SurveyForm3]

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    # path('processing_requests/', views.all_requests, name='show-processing_requests'),
    # Request paths:
    # TODO: Set up so that the url path is company/processing_requests/
    # Relevant_files: customer_list.html, request_by_company_list.html, forms.py, views.py
    re_path(r'^customers/(?P<company>[\w\d\s]+)/processing_requests/$', views.RequestsByCompanyView.as_view(), name='show-company-requests'),
    re_path(r'^customers/(?P<company>[\w\d\s]+)/processing_requests/(?P<pk>\d+)/$', views.RequestDetailView.as_view(), name='request-detail'),
    re_path(r'processing_requests/add/$', views.CreateRequest.as_view(), name='add-request'),
    re_path(r'^customers/(?P<company>[\w\d\s]+)/processing_requests/update/(?P<pk>\d+)/$', views.UpdateRequest.as_view(), name='update-request'),
    re_path(r'^customers/(?P<company>[\w\d\s]+)/processing_requests/delete/(?P<pk>\d+)/$', views.DeleteRequest.as_view(), name='delete-request'), 
    path('new/', views.ModelFormWizard.as_view([RequestForm, GrindRequestForm, DicingRequestForm]), name='request-demo'),
    # Customer paths:
    path('customers/', views.AllCustomersView.as_view(), name='show-customers'), 
    path('customers/<int:pk>', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('customer/add/', views.CreateCustomer.as_view(), name='add-customer'),
    path('customer/update/<int:pk>', views.UpdateCustomer.as_view(), name='update-customer'),
    path('customer/delete/<int:pk>', views.DeleteCustomer.as_view(), name='delete-customer'),
    path('request/<int:year>/<int:month>', views.RequestMonthView.as_view(), name='request-montharchive'),
    # path('add_request/', views.add_request, name='add-request'),
    path('allrequests/', views.all_requests, name='all-request'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('survey/', 
        views.SurveyWizard.as_view(views.SURVEY_FORMS,
        condition_dict=views.SurveyWizard.condition_dict),
        name='survey'
    ),
    
]