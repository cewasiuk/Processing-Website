from django import forms
from django.forms import ModelForm, Textarea, widgets
from django.contrib.auth.forms import UserCreationForm
from .models import DicingRequest, ProcessingRequest, GrindRequest
from users.models import CustomUser
from company.customers import Customer

from ckeditor.widgets import CKEditorWidget


class RFormWidget(forms.TextInput):

    class Meta:
        js = ('script.js',)

    class Media:
        css = {
            'all': ('widget.css',)
        }
        # js = ('script.js',)


class RequestForm(ModelForm):
    # Un-comment after setting up CSS
    required_css_class = 'required'
    # company_name = forms.CharField(max_length=100, )
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = ProcessingRequest
        fields = [ 'company_name', 'process_date', 'quantity', 'material_1', 'track_num_in',  'description',]
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



class GrindRequestForm(ModelForm):
    # Un-comment after setting up CSS
    required_css_class = 'required'
    class Meta:
        model = GrindRequest
        fields = '__all__'


class DicingRequestForm(ModelForm):
    # Un-comment after setting up CSS
    required_css_class = 'required'
    class Meta:
        model = DicingRequest
        fields = '__all__'

class CustomerForm(ModelForm):
    # Un-comment after setting up CSS
    required_css_class = 'required'
    
    
    class Meta:
        model = Customer
        fields = ['company', 'address']
        



class CustomUserForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """ 
    class Meta:
        model = CustomUser
        fields = ('username',)
        
class SurveyForm1(forms.Form):
    department = forms.CharField(max_length=100)
    email = forms.EmailField()
    feedback = forms.BooleanField(label="Any Feedback?", required=False)
    more = forms.BooleanField(label="More cowbells?", required=False)


class SurveyForm2(forms.Form):
    positive_response = forms.CharField(label="What alibi work does this request system eliminate for you?", widget=Textarea)
    negative_response = forms.CharField(label="Does this website create more alibi work for you? If so, any suggestions on how to eliminate it?", widget=Textarea)


class SurveyForm3(forms.Form):
    cowbells = forms.CharField(label="What do we need?")
