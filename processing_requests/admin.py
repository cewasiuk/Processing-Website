from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from django.http import HttpResponse, response
from django.contrib.auth import get_user_model

from .models import ProcessingRequest, GrindRequest, DicingRequest
from .forms import RequestForm
from company.customers import Customer

import csv

# User = get_user_model()

'''
class RequestsAdmin(AdminSite):
    site_header = 'DHA requests Administration'
    site_title = 'DHA requests Admin'
    index_title = 'DHA requests Admin Home'

admin_site = RequestsAdmin(name='requestsadmin')
'''
'''
def set_manager(modeladmin, request, queryset):
    queryset.update(engineer_PIC=request.user)
set_manager.short_description = "Set Engineering PIC"
'''

def requests_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="request_export.csv"'
    writer = csv.writer(response)
    writer.writerow(['company_name', 'process_date', 'material_1',  'quantity', 'sales_PIC', 'engineer_PIC', 'description'])
    for record in queryset:
        # Need to add .get() to access the queries on many to many fields
        rec_list = []
        rec_list.append(record.company_name.get())
        rec_list.append(record.process_date.strftime("%m/%d/%Y"))
        rec_list.append(record.material_1.get())
        rec_list.append(record.quantity)
        rec_list.append(record.sales_PIC.get())
        rec_list.append(record.engineer_PIC.get())
        rec_list.append(record.description)
        writer.writerow(rec_list)
    return response
requests_csv.short_description = "Export Selected Requests to CSV"

class EngineerInLine(admin.TabularInline):
    model = ProcessingRequest.engineer_PIC.through
    verbose_name = 'Engineer PIC'
    verbose_name_plural = 'Engineer PICs'


@admin.register(ProcessingRequest)
class RequestAdmin(admin.ModelAdmin):
    form = RequestForm
    # fields = ('company_name', 'material_1', 'quantity', 'sales_PIC', 'engineer_PIC', 'process_date','report')
    list_display = ('get_company', 'quantity', 'process_date')
    list_display_links = ('get_company',)
    ordering = ('-process_date',)
    list_filter = ('company_name', 'material_1', 'process_date', 'sales_PIC', 'engineer_PIC')
    search_fields = (
        'company_name__company', 'material_1__wafer_material', 'report', 
        )
    list_editable = ('process_date', 'quantity',)
    actions = [requests_csv]
    inlines = [
        EngineerInLine,
    ]
    autocomplete_fields = [
        'company_name', 'material_1', 'sales_PIC', 'engineer_PIC',
    ]
    fieldsets = (
        ('Required Information', {
            'description': "These fields are required for each request.",
            'fields': ('company_name', 'material_1', 'quantity', 'sales_PIC',)
        }), 
        ('Tracking Information', {
            'description': 'Fill these fields out as soon as you have tracking information.', 
            'classes': ('wide',), 
            'fields': ('track_num_in', 'track_num_out', 'process_date',)
        }),
        
        ('Additional Information', {
            'classes': ('collapse',),
            'fields': ('description', 'report')
        }),
    )


    def get_company(self, obj):
        return "\n".join([c.company for c in obj.company_name.all()])

'''
class RequestInLine(admin.StackedInline):
    model = ProcessingRequest

@admin.register(GrindRequest)
class GrindRequestAdmin(admin.ModelAdmin):
    form = GrindRequest
    inlines = [
        RequestInLine,
    ]
'''


# admin.site.register(RequestAdmin)
admin.site.register(GrindRequest)
admin.site.register(DicingRequest)
