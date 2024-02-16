from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scripts import logs_parser

# Create your views here.
def logs_monitoring(request):
    return redirect('/logs_monitoring/system')

@csrf_exempt
def system_log(request):
    if request.method == "GET":
        query = request.GET.get('length', None)
        if query:
            data = logs_parser.get_last_activities(log_dir="/var/log/syslog", num_entries=int(query))
            return JsonResponse(data=data, safe=False)
        else:
            return render(request, 'system_logs.html')

@csrf_exempt
def kernel_log(request):
    if request.method == "GET":
        query = request.GET.get('length', None)
        if query:
            data = logs_parser.get_last_activities(log_dir="/var/log/kern.log", num_entries=int(query))
            return JsonResponse(data=data, safe=False)
        else:
            return render(request, 'kernel_logs.html')
    
@csrf_exempt
def auth_log(request):
    if request.method == "GET":
        query = request.GET.get('length',None)
        if query:
            data = logs_parser.get_last_activities(log_dir="/var/log/auth.log",num_entries=int(query))
            return JsonResponse(data=data, safe=False)
        else:
            return render(request, 'auth_logs.html')