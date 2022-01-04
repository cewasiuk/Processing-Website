from django.urls import path, re_path, include
from . import views



urlpatterns = [
    path('reports/', views.AllCustomersView.as_view(), name='report-customers'),
    re_path(r'^reports/(?P<company>[\w\d\s]+)/reports/$', views.ReportsByCompleted.as_view(), name='show-company-reports'),
    re_path(r'^reports/(?P<company>[\w\d\s]+)/reports/(?P<pk>\d+)/$', views.ReportDetailView.as_view(), name='report-details'),
    re_path(r'^reports/(?P<company>[\w\d\s]+)/reports/update/(?P<pk>\d+)/$', views.UpdateReport.as_view(), name='update-report'),
    re_path(r'^reports/(?P<company>[\w\d\s]+)/reports/(?P<pk>\d+)/complete/$', views.CompleteReportDetailView.as_view(), name='report-details-complete'),


        ]
