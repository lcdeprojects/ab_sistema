from django.urls import path
from . import views

app_name = 'processos'

urlpatterns = [
    path('', views.ProcessoKanbanView.as_view(), name='kanban'),
    path('novo/', views.ProcessoCreateView.as_view(), name='novo'),
    path('<int:pk>/', views.ProcessoDetailView.as_view(), name='detalhes'),
    path('<int:pk>/criar_historico/', views.HistoricoCreateView.as_view(), name='criar_historico'),
    path('<int:pk>/atualizar_processo/', views.ProcessoUpdateView.as_view(), name='atualizar_processo'),
    path('<int:pk>/excluir_processo/', views.ProcessoDeleteView.as_view(), name='excluir_processo'),
    path('status/<str:status>/', views.ProcessoPorStatusListView.as_view(), name='listagem_status'),
    path('status/<str:status>/', views.ProcessoPorStatusListView.as_view(), name='listagem_status'),
    path('historico/<int:pk>/editar/', views.HistoricoUpdateView.as_view(), name='atualizar_historico'),
    path('historico/<int:pk>/excluir/', views.HistoricoDeleteView.as_view(), name='excluir_historico'),
    path('historico/documento/<int:pk>/excluir/', views.DocumentoHistoricoDeleteView.as_view(), name='excluir_documento'),
]
