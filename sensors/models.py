from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Region(models.Model):
    """Modelo para representar grandes regiões ou áreas (ex: Campus, Bloco A)"""
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    manager = models.CharField(max_length=100, blank=True, null=True, verbose_name="Gerente/Responsável")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Região"
        verbose_name_plural = "Regiões"

class Location(models.Model):
    """Modelo para representar locais específicos dentro de uma região"""
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations', verbose_name="Região")
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    # Deprecated: old region string field, kept for migration if needed, but we will use the FK
    # region_old = models.CharField(max_length=100, blank=True, null=True, verbose_name="Região (Antigo)") 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    
    def __str__(self):
        if self.region:
            return f"{self.name} ({self.region.name})"
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = "Local"
        verbose_name_plural = "Locais"

class SensorType(models.Model):
    """Modelo para padronizar tipos de sensores"""
    name = models.CharField(max_length=50, unique=True, verbose_name="Nome do Tipo")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código (ex: temp, hum)")
    unit = models.CharField(max_length=20, verbose_name="Unidade Padrão")
    icon = models.CharField(max_length=50, default='bi-activity', verbose_name="Ícone Bootstrap")
    min_value_default = models.FloatField(default=0, verbose_name="Mínimo Padrão")
    max_value_default = models.FloatField(default=100, verbose_name="Máximo Padrão")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        ordering = ['name']
        verbose_name = "Tipo de Sensor"
        verbose_name_plural = "Tipos de Sensor"

class Sensor(models.Model):
    STATUS_CHOICES = [
        ('normal', 'Normal'),
        ('warning', 'Atenção'),
        ('alert', 'Alerta'),
        ('disconnected', 'Desconectado'),
        ('error', 'Erro'),
    ]

    CONNECTION_CHOICES = [
        ('bluetooth', 'Bluetooth'),
        ('wifi', 'Wi-Fi'),
        ('usb', 'USB'),
        ('lora', 'LoRaWAN'),
        ('ethernet', 'Ethernet'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name='sensors', verbose_name="Localização")
    sensor_type = models.ForeignKey(SensorType, on_delete=models.SET_NULL, null=True, blank=True, related_name='sensors', verbose_name="Tipo de Sensor")
    
    name = models.CharField(max_length=100, verbose_name="Nome")
    description = models.TextField(blank=True, null=True, verbose_name="Descrição")
    connection_type = models.CharField(max_length=20, choices=CONNECTION_CHOICES, default='wifi', verbose_name="Conexão")
    
    # Dados de rede/hardware
    mac_address = models.CharField(max_length=17, blank=True, null=True, verbose_name="Endereço MAC")
    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Endereço IP")
    battery_level = models.IntegerField(default=100, verbose_name="Nível da Bateria")
    
    value = models.FloatField(default=0, verbose_name="Valor")
    # Unit can be overridden from SensorType, but usually inherited. 
    # We keep it here for flexibility or historical data if type changes.
    unit = models.CharField(max_length=20, blank=True, null=True, verbose_name="Unidade") 
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal', verbose_name="Status")
    last_update = models.DateTimeField(default=timezone.now, verbose_name="Última Atualização")
    
    # Limites para alertas
    min_value = models.FloatField(default=0, verbose_name="Valor Mínimo")
    max_value = models.FloatField(default=100, verbose_name="Valor Máximo")
    warning_min = models.FloatField(default=20, verbose_name="Mínimo para Atenção")
    warning_max = models.FloatField(default=80, verbose_name="Máximo para Atenção")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")
    
    def __str__(self):
        unit_display = self.unit if self.unit else (self.sensor_type.unit if self.sensor_type else "")
        return f"{self.name} ({self.value} {unit_display})"
    
    @property
    def status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
    
    def save(self, *args, **kwargs):
        # Auto-fill unit from SensorType if not set
        if not self.unit and self.sensor_type:
            self.unit = self.sensor_type.unit
        super().save(*args, **kwargs)

    def update_value(self, new_value):
        """Atualiza o valor do sensor e recalcula o status"""
        self.value = new_value
        self.last_update = timezone.now()
        
        # Atualiza o status com base nos limites
        if new_value < self.min_value or new_value > self.max_value:
            self.status = 'alert'
        elif new_value < self.warning_min or new_value > self.warning_max:
            self.status = 'warning'
        else:
            self.status = 'normal'
        
        self.save()
        return self.status

class SensorReading(models.Model):
    """Modelo para armazenar leituras históricas dos sensores"""
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings', db_index=True)
    value = models.FloatField(verbose_name="Valor")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Timestamp", db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.sensor.name}: {self.value} {self.sensor.unit} ({self.timestamp})"

class SensorAlert(models.Model):
    """Modelo para armazenar alertas dos sensores"""
    SEVERITY_CHOICES = [
        ('critical', 'Crítico'),
        ('warning', 'Aviso'),
        ('info', 'Informação'),
    ]
    
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='alerts')
    message = models.CharField(max_length=255, verbose_name="Mensagem")
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info', verbose_name="Severidade")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Data/Hora")
    is_resolved = models.BooleanField(default=False, verbose_name="Resolvido")
    resolved_at = models.DateTimeField(blank=True, null=True, verbose_name="Resolvido em")
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"[{self.get_severity_display()}] {self.sensor.name}: {self.message}"

class SensorLog(models.Model):
    """Modelo para auditoria e logs do sistema"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Usuário")
    action = models.CharField(max_length=100, verbose_name="Ação")
    details = models.TextField(blank=True, null=True, verbose_name="Detalhes")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Data/Hora")
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        user_str = self.user.username if self.user else "Sistema"
        return f"[{self.timestamp}] {user_str}: {self.action}"
