from django.db import models

class Fabricante(models.Model):
    nome = models.CharField(max_length=120, unique=True)
    pais_origem = models.CharField(max_length=80, blank=True)
    site = models.URLField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome


class Componente(models.Model):

    class TipoComponente(models.TextChoices):
        PROCESSADOR = "CPU", "Processador (CPU)"
        PLACA_DE_VIDEO = "GPU", "Placa de Vídeo (GPU)"
        MEMORIA_RAM = "RAM", "Memória RAM"
        ARMAZENAMENTO_SSD = "SSD", "Armazenamento SSD"
        ARMAZENAMENTO_HD = "HD", "Armazenamento HD"
        PLACA_MAE = "MOBO", "Placa-mãe"
        FONTE = "PSU", "Fonte de Alimentação"
        GABINETE = "CASE", "Gabinete"

    nome = models.CharField(max_length=150)
    tipo = models.CharField(max_length=4, choices=TipoComponente.choices)
    fabricante = models.ForeignKey(
        Fabricante,
        on_delete=models.CASCADE,
        related_name="componentes",
    )
    preco = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    especificacoes = models.TextField(blank=True)
    em_estoque = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["tipo", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"
