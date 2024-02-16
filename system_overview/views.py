from django.shortcuts import render, redirect
from .scripts import get_system_info, get_security_status, lynis_report
from django.http import JsonResponse

# Create your views here.
def system_overview(request):
    return redirect('/system_overview/general_system_overview')

def general_system_overview(request):
    system_info = get_system_info.get_system_info()
    return render(request, 'general_system_overview.html',{'system_info': system_info})

def security_status(request):
    query = request.GET.get('display', None)

    if query:
        if query == "user_access_status":
            data = get_security_status.get_user_access_status()
            return JsonResponse(data=data)
        elif query == "application_security_status":
            data = get_security_status.get_application_security_status()
            return JsonResponse(data=data)
        elif query == "installed_security_modules":
            data = get_security_status.get_installed_security_modules()
            return JsonResponse(data=data)
        elif query == "network_security":
            data = get_security_status.get_network_security_status()
            return JsonResponse(data=data)
    else:
        return render(request, 'security_status.html')

def security_assessment(request):
    query = request.GET.get('scan', None)
    
    if query:
        output_file = 'lynis_report.txt'
        if query == 'true':
            lynis_report.run_lynis_and_save_output(output_file)

            with open(output_file, 'r') as file:
                lynis_output = file.readlines()

            parsed_data = lynis_report.parse_lynis_output(lynis_output)
            return JsonResponse(parsed_data)
        elif query == 'false':
            with open(output_file, 'r') as file:
                lynis_output = file.readlines()

            parsed_data = lynis_report.parse_lynis_output(lynis_output)
            return JsonResponse(parsed_data)

    else:
        return render(request, 'security_assessment.html')

def critical_alerts(request):
    return render(request, 'critical_alerts.html')