from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Sum
from django.http import HttpResponse
from openpyxl import Workbook
from .models import Transacao

class FinanceiroDashboardView(LoginRequiredMixin, ListView):
    model = Transacao
    template_name = 'financeiro/dashboard.html'
    context_object_name = 'transacoes'
    paginate_by = 20

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Transacao.objects.filter(cliente__nome__icontains=query) | Transacao.objects.filter(descricao__icontains=query)
        return Transacao.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Financial summaries
        total_pago = Transacao.objects.filter(status='pago').aggregate(Sum('valor'))['valor__sum'] or 0
        total_pendente = Transacao.objects.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0
        context['resumo'] = {
            'total_pago': total_pago,
            'total_pendente': total_pendente,
            'total_geral': total_pago + total_pendente
        }
        return context

class TransacaoCreateView(LoginRequiredMixin, CreateView):
    model = Transacao
    template_name = 'financeiro/form_transacao.html'
    fields = ['cliente', 'tipo', 'valor', 'data', 'descricao', 'status']
    success_url = reverse_lazy('financeiro:dashboard')

class TransacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Transacao
    template_name = 'financeiro/form_transacao.html'
    fields = ['cliente', 'tipo', 'valor', 'data', 'descricao', 'status']
    success_url = reverse_lazy('financeiro:dashboard')

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = 'confirmar_delecao.html'
    success_url = reverse_lazy('financeiro:dashboard')

def exportar_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Financeiro AB Advocacia"

    # Header
    columns = ['Data', 'Cliente', 'Tipo', 'Valor', 'Descrição', 'Status']
    ws.append(columns)

    # Data
    for transacao in Transacao.objects.all():
        ws.append([
            transacao.data.strftime('%d/%m/%Y'),
            str(transacao.cliente),
            transacao.get_tipo_display(),
            float(transacao.valor),
            transacao.descricao,
            transacao.get_status_display()
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=financeiro_ab_advocacia.xlsx'
    wb.save(response)
    return response
