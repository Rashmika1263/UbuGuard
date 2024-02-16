from django.shortcuts import render, redirect
from django.http import JsonResponse
from .scripts import usbSettings
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def physical_security(request):
    return redirect('/physical_device_security/usb')

@csrf_exempt
def usb(request):
    if request.method == 'GET':
        query = request.GET.get('display', None)
        if query:
            if query == 'status':
                data = usbSettings.list_usb_devices()
                return JsonResponse(data=data)
        else:
            return render(request, 'usb.html')
    
    elif request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if json_data.get('action', None) == 'allow':
            usbSettings.allow_usb_device(json_data.get('id', None))
            return redirect('/physical_device_security/usb')

        elif json_data.get('action', None) == 'block':
            usbSettings.block_usb_device(json_data.get('id', None))
        return redirect('/physical_device_security/usb') 
