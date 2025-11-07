from django.contrib.auth.models import AbstractUser
from django.db import models
from localflavor.br.models import BRCPFField, BRPostalCodeField
from django.core.validators import RegexValidator

class Usuario(AbstractUser):
    # ... (Conteúdo do modelo Usuario omitido por brevidade, mas deve ser o completo)
    TIPO_USUARIO = [
        ('DIRETORIA', 'Diretoria'),
        ('ASSOCIADO', 'Associado'),
        ('AFILIADO', 'Afiliado'),
        ('COLETIVO', 'Coletivo/Institucional'),
    ]
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO, default='AFILIADO', verbose_name='Tipo de Usuário')
    nome_social = models.CharField(max_length=150, blank=True, verbose_name='Nome Social')
    cpf = BRCPFField('CPF', unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    nick_discord = models.CharField(max_length=100, blank=True, verbose_name='Nick no Discord')
    cep = BRPostalCodeField('CEP', blank=True)
    endereco = models.CharField('Endereço', max_length=255, blank=True)
    numero = models.CharField('Número', max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True, default='Rio de Janeiro')
    ESTADOS_BRASIL = [('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'), ('MG', 'Minas Gerais'), ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SE', 'Sergipe'), ('TO', 'Tocantins')]
    estado = models.CharField(max_length=2, choices=ESTADOS_BRASIL, default='RJ')
    data_associacao = models.DateField('Data de Associação', null=True, blank=True)
    ativo = models.BooleanField(default=True, verbose_name='Usuário Ativo')
    foto_perfil = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name='Foto de Perfil')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name', 'last_name']
    
    def __str__(self):
        nome_completo = self.get_full_name()
        if nome_completo:
            return f"{nome_completo} ({self.get_tipo_usuario_display()})"
        return f"{self.username} ({self.get_tipo_usuario_display()})"
