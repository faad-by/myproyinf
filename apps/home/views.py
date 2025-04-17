# -*- encoding: utf-8 -*-
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from apps.home.models import ModeloRegistro
from django.shortcuts import redirect, render

import hashlib
import ast
import time
import os
from core import settings
CORE_DIR = getattr(settings, 'CORE_DIR', '')

import qrcode
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
            return redirect("/home/forms-consentimiento.html")
            #return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        # En caso sea la pagina de revision
        if (load_template =="forms-checkForm.html"):
            if request.method == 'GET':                
                if ('regiCode' in request.GET):
                    hash_code = request.GET.get('regiCode')
                    inst = ModeloRegistro.objects.get(hashcode=hash_code)
                    # Se muestra la informacion completa
                    dict_info = {}
                    dict_info["nombre_apoderado"] = inst.nombre_apoderado
                    dict_info["edad_apoderado"] = inst.edad_apoderado
                    dict_info["tipo_documento"] = inst.tipo_documento
                    dict_info["num_documento"] = inst.num_documento
                    dict_info["telefono"] = inst.telefono
                    dict_info["correo"] = inst.correo
                    dict_info["apoderados"] = ast.literal_eval(inst.apoderados)
                    dict_info["terms_cond"] = inst.terms_cond
                    dict_info["firma_imagen"] = inst.firma_imagen
                    dict_info["fecha_registro"] = inst.fecha_registro

                    html_template = loader.get_template("home/forms-checkForm.html")
                    return HttpResponse(html_template.render(dict_info, request))
                
                elif ('dniCode' in request.GET):
                    dni_code = request.GET.get('dniCode')
                    inst = ModeloRegistro.objects.all().filter(num_documento=str(dni_code)).last()
                    # Se muestra la informacion completa
                    dict_info = {}
                    dict_info["nombre_apoderado"] = inst.nombre_apoderado
                    dict_info["edad_apoderado"] = inst.edad_apoderado
                    dict_info["tipo_documento"] = inst.tipo_documento
                    dict_info["num_documento"] = inst.num_documento
                    dict_info["telefono"] = inst.telefono
                    dict_info["correo"] = inst.correo
                    dict_info["apoderados"] = ast.literal_eval(inst.apoderados)
                    dict_info["terms_cond"] = inst.terms_cond
                    dict_info["firma_imagen"] = inst.firma_imagen
                    dict_info["fecha_registro"] = inst.fecha_registro

                    html_template = loader.get_template("home/forms-checkForm.html")
                    return HttpResponse(html_template.render(dict_info, request))
                else:
                    return redirect("/home/forms-consentimiento.html")

        # Se guarda la informacion en caso exista
        if request.method == 'POST':
            # Leer todos los datos de request.POST
            post_data = request.POST.dict()
            h = hashlib.sha3_512()
            h.update(str(time.time()).encode("utf-8"))
            inst = ModeloRegistro(nombre_apoderado = post_data["idVar1"],
                                edad_apoderado = post_data["idVar2"],
                                tipo_documento = post_data["idVar3"],
                                num_documento = post_data["idVar4"],
                                telefono = post_data["idVar5"],
                                correo = post_data["idVar6"],
                                apoderados = post_data["childTable"],
                                terms_cond =  post_data["terminos"],
                                firma_imagen = post_data["firma-base64"],
                                hashcode = str(h.hexdigest()))
            inst.save()

            qr = qrcode.QRCode(
                            version=12,
                            error_correction=qrcode.constants.ERROR_CORRECT_L,
                            box_size=4,
                            border=4)

            # se devuelve la imagen
            newpage = "https://jumpville.pe/forms-checkForm.html?regiCode="+h.hexdigest()
            qr.add_data(newpage)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # Guardar la imagen en un archivo temporal
            file_path = "qr_image_" + h.hexdigest() + ".png"
            img.save(file_path)

            # Leer la imagen del archivo y convertirla en base64
            with open(file_path, "rb") as img_file:
                qr_image_base64 = base64.b64encode(img_file.read()).decode()

            # Eliminar el archivo temporal después de convertir a base64
            os.remove(file_path)
            html_template = loader.get_template("home/qrpage.html")
            return HttpResponse(html_template.render({"qr_image_base64":qr_image_base64}, request))
            #return redirect("/home/qrpage.html?iden="+qr_image_base64)

            #return HttpResponse(html_template.render({"qr_image_base64":qr_image_base64}, request))

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
