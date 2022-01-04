from django.db.models.fields import NullBooleanField
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.dates import MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.forms import formset_factory, modelformset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.apps import apps
from itertools import chain
from django.http import FileResponse
from fpdf import FPDF
from .models import Report
from reports.forms import ReportForm
from processing_requests.models import ProcessingRequest
from company.customers import Customer
# Create your views here.

class AllCustomersView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Customer
    context_object_name = 'all_customers'
    template_name = 'reports/report_customer_list.html'
    paginate_by = 10


class ReportsByCompleted(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'reports/report_by_company_list.html'

    def get_queryset(self):

        qs = ProcessingRequest.processing_requests.all()
        company = self.kwargs['company']
        if company is not None:
            object_list = qs.filter(company_name__company=company)
        return object_list

  #def get_context_data(self):
        #qs = ProcessingRequest.processing_requests.all()
        #company = self.kwargs['company']
        #if company is not None:
            #context = super().get_context_data()
            #context['incomplete'] = qs.filter(company_name__company=company ).filter(report__isnull = True)
            #context['complete'] = qs.filter(company_name__company=company ).exclude(report__isnull = True)
        #return context


class ReportsByCompanyView(LoginRequiredMixin, ListView):

    # serializer_class = RequestSerializer
    login_url = reverse_lazy('login')
    # context_object_name = 'company_report'
    # renderer_classes = (RequestsTemplateHTMLRenderer,)
    template_name = 'reports/report_by_company_list.html'

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




@login_required
def all_reports(request):
    RequestFormSet = modelformset_factory(
        ProcessingRequest, 
        fields=('company_name', 'process_date', 'quantity', 'material_1', 'report_input'),
        extra=0
    )
    qry = Report.reports.all()
    pg = Paginator(qry, 4)
    page = request.GET.get('page')
    try:
        report_records = pg.page(page)
    except PageNotAnInteger:
        report_records = pg.page(1)
    except EmptyPage:
        report_records = pg.page(pg.num_pages)
    if request.method == 'POST':
        formset = RequestFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return_url = 'allreports/'
            if 'page' in request.GET:
                return_url += '?page=' + request.GET['page']
            return HttpResponseRedirect(return_url)
    else:
        page_qry = qry.filter(id__in=[rqst.id for rqst in report_records])
        formset = RequestFormSet(queryset=page_qry)

    context = {'report_records': report_records, 'formset': formset}
    return render(request, 'reports/all_reports.html', context)


class ReportDetailView(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    template_name = 'reports/report_detail.html'
    context_object_name = 'report'

class CompleteReportDetailView(LoginRequiredMixin, DetailView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    template_name = 'reports/report_detail_complete.html'
    context_object_name = 'reports'

class UpdateReport(LoginRequiredMixin, UpdateView):
    
    login_url = reverse_lazy('login')
    model = ProcessingRequest
    form_class = ReportForm
    context_object_name = 'report'
    template_name = 'reports/report_update_form.html'

    def get_success_url(self):
        if 'company' in self.kwargs:
            company = self.kwargs['company']
        else: 
            company = ''
        return reverse('show-company-reports', kwargs={'company': company})




def pdfview(request, pk):
    report_info = ProcessingRequest.processing_requests.get(id = pk)
    a = str(pk)

    engineers = [engineer for engineer in report_info.engineer_PIC.all()]

    engineer_string = ", ".join([f"{x}" for x in engineers])
    
    pdf = FPDF('P', 'mm', 'A4')
    pdf.add_page()
    pdf.header()
    pdf.set_line_width(0.0)
    pdf.set_font('times', 'B', 16)
    pdf.header() 

    #Border
    pdf.rect(5,5,200,285)


    #Disco Logo
    pdf.set_xy(10.0,10.0)
    pdf.image('reports/disco_icon.png',  link='', type='png', w=1400/80, h=1400/80)

    #Text Lines
    pdf.cell(40, 10, '',0, 1)
    pdf.cell(40, 10, '',0, 1)
    pdf.set_font('times', 'B', 16)
    
    #Title 
    pdf.set_xy(5.0,0.0)
    pdf.cell(w=200.0, h=40.0, align='C', txt= f"{ '{} Processing Report'.format(report_info.company_name.get())}", border=0)
    pdf.line(65,25,145,25)

    #Report/Company Info 
    pdf.set_xy(10.0,35.0)
    pdf.set_font('times','', 12)
    pdf.cell(100, 10, f"Process Date: {report_info.process_date}", 0, 0)
    pdf.line(11.5,43,75,43)
    pdf.cell(100, 10, f"Company: {report_info.company_name.get()}", 0, 1)
    pdf.line(111.5,43,155,43)
    pdf.cell(100, 10, f"Material: {report_info.material_1.get()}", 0, 0)
    pdf.line(11.5,53,75,53)
    pdf.cell(100, 10, f"Number of wafers processed: {report_info.quantity}", 0, 1)
    pdf.line(111.5,53,170,53)
    pdf.cell(180, 10, f"Disco Engineers in charge: {engineer_string}", 0, 1)
    pdf.line(11.5,63,170,63)
    
    #Report Summary
    pdf.set_xy(5.0, 55.0)
    pdf.set_font('times','B', 12)
    pdf.cell(w = 200, h = 40, align = 'C', txt = "Report Summary", border = 0, ln = 1)
    pdf.line(11.5,80,198.5,80)
    pdf.set_font('times','', 12)
    pdf.set_xy(10.0,87)
    pdf.multi_cell(190, 8, f"{report_info.report}")


    #Return Report
    pdf.output('{}_Report.pdf'.format(report_info.company_name.get()), 'F')
    return FileResponse(open('{}_Report.pdf'.format(report_info.company_name.get()), 'rb'), as_attachment=False, content_type='application/pdf')
