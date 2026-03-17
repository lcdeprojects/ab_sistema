from django.urls import path
from . import views

app_name = 'financeiro'

urlpatterns = [
    path('', views.FinanceiroDashboardView.as_view(), name='dashboard'),
    path('transacao/nova/', views.TransacaoCreateView.as_view(), name='nova_transacao'),
    path('transacao/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='editar_transacao'),
    path('transacao/<int:pk>/deletar/', views.TransacaoDeleteView.as_view(), name='deletar_transacao'),
    path('exportar/', views.exportar_excel, name='exportar_excel'),
]
