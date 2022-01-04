from django.contrib.admin import AdminSite
from django.contrib import admin


class DhaAdmin(AdminSite):
    site_header = 'DHA Administration'
    site_title = 'DHA Site Admin'
    index_title = 'DHA Site Admin Home'
