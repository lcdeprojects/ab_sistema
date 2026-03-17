from django.db import models
from django.conf import settings
from apps.clientes.models import Cliente

class Processo(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('suspenso', 'Suspenso'),
        ('encerrado', 'Encerrado'),
    ]

    numero = models.CharField(max_length=50, unique=True, verbose_name="Número do Processo")
    titulo = models.CharField(max_length=200)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='processos')
    advogado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='processos_atribuidos')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    descricao = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.numero} - {self.titulo}"

class HistoricoProcesso(models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='historico')
    advogado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    comentario = models.TextField()
    arquivo = models.FileField(upload_to='processos/documentos/', null=True, blank=True)
    data_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_hora']
