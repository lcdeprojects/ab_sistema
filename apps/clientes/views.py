from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cliente

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'clientes/lista_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Cliente.objects.filter(nome__icontains=query) | Cliente.objects.filter(cpf__icontains=query)
        return Cliente.objects.all()

class ClienteDetailView(LoginRequiredMixin, DetailView):
    model = Cliente
    template_name = 'clientes/detalhes_cliente.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adding linked processes and financial history
        context['processos'] = self.object.processos.all().order_by('-updated_at')
        context['transacoes'] = self.object.transacoes.all().order_by('-data')
        return context

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'clientes/form_cliente.html'
    fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'whatsapp', 'email']
    success_url = reverse_lazy('clientes:lista')

class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    template_name = 'clientes/form_cliente.html'
    fields = ['nome', 'sobrenome', 'cpf', 'telefone', 'whatsapp', 'email']
    success_url = reverse_lazy('clientes:lista')

class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente
    template_name = 'confirmar_delecao.html'
    success_url = reverse_lazy('clientes:lista')
