from django import forms
from django.forms import ModelForm, Textarea, widgets
from django.contrib.auth.forms import UserCreationForm
from .models import Report
from users.models import CustomUser
from ckeditor.widgets import CKEditorWidget
from django.apps import apps
from processing_requests.models import ProcessingRequest

class RFormWidget(forms.TextInput):
    class Media:
        css = {
            'all': ('widget.css',)
        }

class ReportForm(ModelForm):
    # Un-comment after setting up CSS
    required_css_class = 'required'
    # company_name = forms.CharField(max_length=100, )
    
    class Meta:
        model = ProcessingRequest
        fields = ['report']
        '''
        widgets = {
            'company_name': RFormWidget(attrs={'class': 'mywidget'}),
        }
        '''

    class Media:
        css = {
            'all': ('form.css',)
        }
        js = ('mycustom.js',)
