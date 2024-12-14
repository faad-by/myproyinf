# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

# Create your models here.
class RegistryModel(models.Model):
    "Modelo para guardar informacion del registro"
    nombre_apoderado = models.CharField(max_length=300)
    edad_apoderado = models.IntegerField()
    tipo_documento = models.CharField(max_length=100)
    num_documento = models.CharField(max_length=100)
    telefono = models.CharField(max_length=40)
    correo = models.CharField(max_length=50)
    apoderados = models.CharField(max_length=550)
    terms_cond= models.CharField(max_length=40)
    firma_imagen = models.CharField(max_length=40)
    hashcode = models.CharField(max_length=200)
    fecha_registro = models.DateTimeField(auto_now=True)