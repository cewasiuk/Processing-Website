from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.http import HttpResponse, response
from django.contrib.auth import get_user_model
import csv
from django.forms import TextInput, Textarea
from django.db import models
from .forms import ReportForm
from .models import Report

def report_csv(modeladmin, ProcessingRequest, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['company_name', 'material_1',  'quantity', 'engineer_PIC'])
    for record in queryset:
        # Need to add .get() to access the queries on many to many fields
        rec_list = []
        rec_list.append(record.company_name.get())
        rec_list.append(record.material_1.get())
        rec_list.append(record.quantity)
        rec_list.append(record.engineer_PIC.get())
        rec_list.append(record.process_data)
        writer.writerow(rec_list)
    return response
report_csv.short_description = "Export Selected Requests to CSV"




