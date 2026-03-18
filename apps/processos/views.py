from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Processo, HistoricoProcesso
from .dashboard_views import dashboard_view

class ProcessoKanbanView(LoginRequiredMixin, ListView):
    model = Processo
    template_name = 'processos/kanban.html'
    context_object_name = 'processos'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(numero__icontains=query) | Q(titulo__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filter processes by status for the kanban columns
        processos = self.get_queryset()
        context['colunas'] = {
            'aberto': processos.filter(status='aberto'),
            'em_andamento': processos.filter(status='em_andamento'),
            'suspenso': processos.filter(status='suspenso'),
            'encerrado': processos.filter(status='encerrado'),
        }
        return context

class ProcessoDetailView(LoginRequiredMixin, DetailView):
    model = Processo
    template_name = 'processos/detalhes_processo.html'

class ProcessoCreateView(LoginRequiredMixin, CreateView):
    model = Processo
    template_name = 'processos/form_processo.html'
    fields = ['numero', 'titulo', 'cliente', 'advogado', 'status', 'descricao']
    success_url = reverse_lazy('processos:kanban')


class ProcessoUpdateView(LoginRequiredMixin, UpdateView):
    model = Processo
    template_name = 'processos/form_atualizar.html'
    fields = ['numero', 'titulo', 'cliente', 'advogado', 'status', 'descricao']
    success_url = reverse_lazy('processos:kanban')

class ProcessoDeleteView(LoginRequiredMixin, DeleteView):
    model = Processo
    template_name = 'confirmar_delecao.html'
    success_url = reverse_lazy('processos:kanban')

class HistoricoCreateView(LoginRequiredMixin, CreateView):
    model = HistoricoProcesso
    template_name = 'processos/form_historico.html'
    fields = ['comentario', 'arquivo']
    
    def form_valid(self, form):
        form.instance.processo_id = self.kwargs['pk']
        form.instance.advogado = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('processos:detalhes', kwargs={'pk': self.kwargs['pk']})

class ProcessoPorStatusListView(LoginRequiredMixin, ListView):
    model = Processo
    template_name = 'processos/listagem_status.html'
    context_object_name = 'processos'
    paginate_by = 10

    def get_queryset(self):
        self.status_slug = self.kwargs.get('status')
        return Processo.objects.filter(status=self.status_slug).order_by('-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        status_display = dict(Processo.STATUS_CHOICES).get(self.status_slug, self.status_slug.title())
        context['status_nome'] = status_display
        context['status_slug'] = self.status_slug
        return context
