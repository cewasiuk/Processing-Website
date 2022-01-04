from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.dates import MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory, modelformset_factory
from formtools.wizard.views import SessionWizardView
from django.core.mail import send_mail, get_connection
from django.contrib import messages


from datetime import date
import calendar
from company.customers import Customer

from processing_requests.forms import (
    RequestForm, GrindRequestForm, 
    SurveyForm1, SurveyForm2, SurveyForm3, 
    CustomUserForm, 
    CustomerForm
)
from .models import ProcessingRequest, GrindRequest
from processing_requests.admin import EngineerInLine


class HomePageView(TemplateView):
    
    template_name = "home.html" 


# Company views (which will filter the following requests):
class AllCustomersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Customer
    context_object_name = 'all_customers'
    template_name = 'processing_requests/customer_list.html'
    paginate_by = 10


class CustomerDetailView(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    model = Customer
    context_object_name = 'customer'
    context_object_name = 'customer_detail.html'
    

class CreateCustomer(LoginRequiredMixin, CreateView):
    
    login_url = reverse_lazy('login')
    model = Customer
    form_class = CustomerForm
    template_name = 'processing_requests/customer_form.html'
    success_url = reverse_lazy('show-customers')


class UpdateCustomer(LoginRequiredMixin, UpdateView):
    
    login_url = reverse_lazy('login')
    model = Customer
    form_class = CustomerForm
    template_name = 'processing_requests/customer_update_form.html'
    success_url = reverse_lazy('show-customers')


class DeleteCustomer(LoginRequiredMixin, DeleteView):
    
    login_url = reverse_lazy('login')
    model = Customer
    form_class = CustomerForm
    context_object_name = 'customer'
    template_name = 'processing_requests/customer_confirm_delete.html'
    success_url = reverse_lazy('show-customer')


# Request views
class AllRequestsView(LoginRequiredMixin, ListView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    context_object_name = 'all_processing_requests'
    template_name = 'processing_requests/processing_requests_list.html'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        object_list = ProcessingRequest.processing_requests.filter(
            Q(company_name__company__icontains=query) |
            Q(material_1__wafer_material__icontains=query) |
            Q(track_num_in__exact=query)
        )
        return object_list

'''
# TypeError: context must be a dict rather than ReturnList
class RequestsTemplateHTMLRenderer(TemplateHTMLRenderer):
    def get_template_context(self, data, renderer_context):
        data = super().get_template_context(data, renderer_context)
        if not data:
            return {}
        else:
            return data
'''


class RequestsByCompanyView(LoginRequiredMixin, ListView):

    # serializer_class = RequestSerializer
    login_url = reverse_lazy('login')
    # context_object_name = 'company_request'
    # renderer_classes = (RequestsTemplateHTMLRenderer,)
    template_name = 'processing_requests/processing_request_by_company_list.html'

    def get_queryset(self):
        """
        This view should return a list of all the processing_requests 
        made by the specific company selected in the AllCustomersView.
        """
        queryset = ProcessingRequest.processing_requests.all()
        company = self.kwargs['company']
        if company is not None:
            object_list = queryset.filter(company_name__company=company)
        return object_list


class RequestDetailView(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    context_object_name = 'processing_request'
    template_name = 'processing_requests/processing_request_detail.html'
    

class CreateRequest(LoginRequiredMixin, CreateView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    form_class = RequestForm
    context_object_name = 'processing_request'
    template_name = 'processing_requests/processing_request_form.html'
    success_url = reverse_lazy('show-customers')
    '''
    def get_success_url(self):
        if 'company' in self.kwargs:
            company = self.kwargs['company']  
        else: 
            company = 'Did not work!'
        return reverse('show-company-requests', kwargs={'company': ProcessingRequest.company_name})
    '''

class UpdateRequest(LoginRequiredMixin, UpdateView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    form_class = RequestForm
    context_object_name = 'processing_request'
    template_name = 'processing_requests/processing_request_update_form.html'

    def get_success_url(self):
        if 'company' in self.kwargs:
            company = self.kwargs['company']
        else: 
            company = ''
        return reverse('show-company-requests', kwargs={'company': company})


class DeleteRequest(LoginRequiredMixin, DeleteView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    form_class = RequestForm
    context_object_name = 'processing_request'
    template_name = 'processing_requests/processing_request_confirm_delete.html'
    
    def get_success_url(self):
        if 'company' in self.kwargs:
            company = self.kwargs['company']
        else: 
            company = ''
        return reverse('show-company-requests', kwargs={'company': company})




class RequestMonthView(LoginRequiredMixin, MonthArchiveView):
    
    login_url = reverse_lazy('login')
    queryset = ProcessingRequest.processing_requests.all()
    date_field = "process_date"
    context_object_name = "processing_request_list"
    allow_future = True
    month_format = '%m'



class Register(CreateView):
    template_name = 'registration/register.html'
    form_class = CustomUserForm
    success_url = reverse_lazy('register-success')

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.success_url)

@login_required
def all_requests(request):
    RequestFormSet = modelformset_factory(
        ProcessingRequest, 
        fields=('company_name', 'process_date', 'quantity', 'material_1', 'track_num_in'),
        extra=0
    )
    qry = ProcessingRequest.processing_requests.all()
    pg = Paginator(qry, 4)
    page = request.GET.get('page')
    try:
        request_records = pg.page(page)
    except PageNotAnInteger:
        request_records = pg.page(1)
    except EmptyPage:
        request_records = pg.page(pg.num_pages)
    if request.method == 'POST':
        formset = RequestFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return_url = 'allrequests/'
            if 'page' in request.GET:
                return_url += '?page=' + request.GET['page']
            return HttpResponseRedirect(return_url)
    else:
        page_qry = qry.filter(id__in=[rqst.id for rqst in request_records])
        formset = RequestFormSet(queryset=page_qry)

    context = {'request_records': request_records, 'formset': formset}
    return render(request, 'processing_requests/all_requests.html', context)



SURVEY_FORMS = [
    ('general', SurveyForm1),
    ('feedback', SurveyForm2),
    ('cowbells', SurveyForm3),
]

def show_feedback_form_condition(wizard):
    # Attempt to get cleaned data from first form
    cleaned_data = wizard.get_cleaned_data_for_step('general') or {}
    # Check if field 'feedback' is checked
    return cleaned_data.get('feedback', True)

def show_cowbell_form_condition(wizard):
    # Attempt to get cleaned data from first form
    cleaned_data = wizard.get_cleaned_data_for_step('general') or {}
    # Check if field 'more' is checked
    return cleaned_data.get('more', True)



class SurveyWizard(SessionWizardView):
    template_name = 'processing_requests/survey.html'
    condition_dict = {
        'feedback': show_feedback_form_condition, 
        'cowbells': show_cowbell_form_condition,    
    }

    def done(self, form_list, **kwargs):
        responses = [form.cleaned_data for form in form_list]
        mail_body = ''
        for response in responses:
            for k,v in response.items():
                mail_body += f"{k}: {v}\n"
        con = get_connection('django.core.mail.backends.console.EmailBackend')
        send_mail(
            'Survey Submission',
            mail_body,
            'noreply@example.com',
            ['siteowner@example.com'],
            connection=con,
        )
        messages.add_message(
            self.request,
            messages.SUCCESS, 
            'Your survey was submitted successfully. Thank you for your feedback.'
        )
        return HttpResponseRedirect('/survey')


class ModelFormWizard(LoginRequiredMixin, SessionWizardView):
    template_name = "processing_requests/modelwiz_request.html"
    def done(self, form_list, **kwargs):
        for form in form_list:
            form.save()
        return HttpResponseRedirect('/')

