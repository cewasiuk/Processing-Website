from django.contrib.admin.apps import AdminConfig


class DhaAdminConfig(AdminConfig):
    default_site = 'process_site.admin.DhaAdmin'
    # name = 'process_site'