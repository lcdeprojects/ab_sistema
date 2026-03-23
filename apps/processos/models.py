from django.db import models
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
import os
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

    def __str__(self):
        return f"Atualização de {self.data_hora.strftime('%d/%m/%Y')} - {self.advogado.username if self.advogado else 'Sistema'}"

class DocumentoHistorico(models.Model):
    historico = models.ForeignKey(HistoricoProcesso, on_delete=models.CASCADE, related_name='documentos')
    arquivo = models.FileField(upload_to='processos/documentos/')
    nome_original = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_original or f"Documento {self.pk}"

@receiver(post_delete, sender=DocumentoHistorico)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deleta o arquivo físico do disco quando o registro do banco é excluído.
    """
    if instance.arquivo:
        if os.path.isfile(instance.arquivo.path):
            os.remove(instance.arquivo.path)
