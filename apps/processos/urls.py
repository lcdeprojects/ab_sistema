from django.urls import path
from . import views

app_name = 'processos'

urlpatterns = [
    path('', views.ProcessoKanbanView.as_view(), name='kanban'),
    path('novo/', views.ProcessoCreateView.as_view(), name='novo'),
    path('<int:pk>/', views.ProcessoDetailView.as_view(), name='detalhes'),
    path('<int:pk>/atualizar/', views.HistoricoCreateView.as_view(), name='adicionar_historico'),
    path('<int:pk>/atualizar_processo/', views.ProcessoUpdateView.as_view(), name='atualizar_processo'),
    path('<int:pk>/excluir_processo/', views.ProcessoDeleteView.as_view(), name='excluir_processo'),
]
