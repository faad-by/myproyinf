# -*- encoding: utf-8 -*-
from django.db import models
from django.utils import timezone

# Create your models here.
class ModeloRegistro(models.Model):
    "Modelo para guardar informacion del registro"
    nombre_apoderado = models.CharField(max_length=300)
    edad_apoderado = models.IntegerField()
    tipo_documento = models.CharField(max_length=100)
    num_documento = models.CharField(max_length=100)
    telefono = models.CharField(max_length=40)
    correo = models.CharField(max_length=50)
    apoderados = models.CharField(max_length=550)
    terms_cond= models.CharField(max_length=40)
    firma_imagen = models.CharField(max_length=12000)
    hashcode = models.CharField(max_length=400)
    fecha_registro = models.DateTimeField(default=timezone.now)