from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.clientes.models import Cliente
from apps.processos.models import Processo
from apps.financeiro.models import Transacao
from django.db.models import Count, Sum, Q

@login_required
def dashboard_view(request):
    # Stats for the main dashboard (Home)
    query = request.GET.get('q', '')
    
    if query:
        processos = Processo.objects.filter(
            Q(numero__icontains=query) | Q(titulo__icontains=query)
        ).order_by('numero')
    else:
        processos = Processo.objects.all().order_by('numero')

    context = {
        'processos': processos,
        'query': query,
    }
    
    stats = {
        'total_clientes': Cliente.objects.count(),
        'total_processos': Processo.objects.count(),
        'processos_por_advogado': Processo.objects.values('advogado__username').annotate(total=Count('id')).order_by('-total'),
        'total_financeiro': Transacao.objects.filter(status='pago').aggregate(Sum('valor'))['valor__sum'] or 0,
    }
    return render(request, 'dashboard/index.html', {'stats': stats, 'processos': processos, 'query': query})
