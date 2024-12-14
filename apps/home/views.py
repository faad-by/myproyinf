# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import RegistryModel
import hashlib

import qrcode
from django.shortcuts import render
from .forms import QRCodeForm
from io import BytesIO
import base64

@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


#@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        # Se guarda la informacion en caso exista
        if request.method == 'POST':
            # Leer todos los datos de request.POST
            post_data = request.POST.dict()
            h = hashlib.sha3_512()
            inst = RegistryModel(nombre_apoderado = post_data["idVar1"],
                                edad_apoderado = post_data["idVar2"],
                                tipo_documento = post_data["idVar3"],
                                num_documento = post_data["idVar4"],
                                telefono = post_data["idVar5"],
                                correo = post_data["idVar6"],
                                apoderados = post_data["childTable"],
                                terms_cond =  post_data["terminos"],
                                firma_imagen = post_data["firma-base64"],
                                hashcode = h.hexdigest())
            inst.save()


            qr = qrcode.QRCode(
                            version=1,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=10,
                            border=4)

            # se devuelve la imagen
            qr.add_data(h.hexdigest())
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            qr_image_base64 = base64.b64encode(buffer.getvalue()).decode()

            html_template = loader.get_template('home/qrpage.html')
            return HttpResponse(html_template.render({"qr_image_base64":qr_image_base64}, request))

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
