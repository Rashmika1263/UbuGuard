from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .scripts import user_management,sudo_management, last_user_activity, last_user_login
from .forms import SSHSettingsForm
from .scripts.ssh_conf import (
    read_sshd_config, 
    write_sshd_config, 
    set_boolean_setting, 
    set_list_setting,
    get_boolean_setting,
    get_list_setting,
    get_ssh_status,
    enable_ssh,
    disable_ssh,
    restart_ssh
)
import json

# Create your views here.
def access_control(request):
    return redirect('/access_control/user_access_management')

def user_access_management(request):
    return render(request, 'user_management.html')

@csrf_exempt
def uam(request):
    if request.method == "GET":
        data = user_management.list_users()
        return JsonResponse(data=data, safe=False)
    elif request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if json_data.get('action', None) == 'add_user':
            user_management.create_user(
                username=json_data.get('uname',None),
                password=json_data.get('pass',None)
            )
            return JsonResponse({'message': 'Data processed successfully'})

        elif json_data.get('action', None) == 'remove_user':
            user_management.delete_user(
                username=json_data.get('uname',None)
            )
            return JsonResponse({'message': 'Data processed successfully'})


@csrf_exempt
def pam(request):
    if request.method == "GET":
        data = sudo_management.list_sudo_users()
        return JsonResponse(data=data, safe=False)
    elif request.method == "POST":
        try:
            json_data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if json_data.get('action', None) == 'add_user':
            sudo_management.add_user_to_sudo(
                username=json_data.get('uname',None)
            )
            return JsonResponse({'message': 'Data processed successfully'})
        
        elif json_data.get('action', None) == 'remove_user':
            sudo_management.remove_user_from_sudo(
                username=json_data.get('uname',None)
            )
            return JsonResponse({'message': 'Data processed successfully'})

@csrf_exempt
def ua(request):
    if request.method == "GET":
        data = last_user_activity.get_last_activities()
        return JsonResponse(data=data, safe=False)

@csrf_exempt
def ul(request):
    if request.method == "GET":
        data = last_user_login.get_last_login_users()
        return JsonResponse(data=data, safe=False)


def ssh_management(request):
    return render(request, 'ssh_management.html')

@csrf_exempt
def ssh_conf(request):
    sshd_config_lines = read_sshd_config()

    if request.method == 'GET':
        try:
            sshd_config_lines = read_sshd_config()
            
            ssh_status = get_boolean_setting(sshd_config_lines, "PasswordAuthentication")
            allow_users = get_list_setting(sshd_config_lines, "AllowUsers")
            permit_root_login = get_boolean_setting(sshd_config_lines, "PermitRootLogin")
            use_dns = get_boolean_setting(sshd_config_lines, "UseDNS")
            permit_empty_passwords = get_boolean_setting(sshd_config_lines, "PermitEmptyPasswords")
            client_alive_interval = get_list_setting(sshd_config_lines, "ClientAliveInterval")
            client_alive_count_max = get_list_setting(sshd_config_lines, "ClientAliveCountMax")
            login_grace_time = get_list_setting(sshd_config_lines, "LoginGraceTime")
            default_port = get_list_setting(sshd_config_lines,"Port")

            return JsonResponse({
                "PasswordAuthentication": ssh_status,
                "AllowUsers": allow_users,
                "PermitRootLogin": permit_root_login,
                "UseDNS": use_dns,
                "PermitEmptyPasswords": permit_empty_passwords,
                "ClientAliveInterval": client_alive_interval,
                "ClientAliveCountMax": client_alive_count_max,
                "LoginGraceTime": login_grace_time,
                "DefaultPort": default_port
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    form = SSHSettingsForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        if form.cleaned_data['ssh_status'] == 'enable':
            enable_ssh()
        elif form.cleaned_data['ssh_status'] == 'disable':
            disable_ssh()

        password_auth = form.cleaned_data['password_authentication']
        allow_users = form.cleaned_data['allow_users'].split(',') if form.cleaned_data['allow_users'] else []
        client_alive_interval = str(form.cleaned_data['client_alive_interval'])
        client_alive_count_max = str(form.cleaned_data['client_alive_count_max'])
        login_grace_time = str(form.cleaned_data['login_grace_time'])
        default_port = str(form.cleaned_data['change_default_port'])

        set_boolean_setting(sshd_config_lines,"PasswordAuthentication", password_auth)
        set_list_setting(sshd_config_lines,"AllowUsers", allow_users)
        set_boolean_setting(sshd_config_lines, "PermitRootLogin", form.cleaned_data['permit_root_login'])
        set_boolean_setting(sshd_config_lines, "UseDNS", form.cleaned_data['use_dns'])
        set_boolean_setting(sshd_config_lines, "PermitEmptyPasswords", form.cleaned_data['permit_empty_passwords'])
        set_list_setting(sshd_config_lines, "ClientAliveInterval", [client_alive_interval])
        set_list_setting(sshd_config_lines, "ClientAliveCountMax", [client_alive_count_max])
        set_list_setting(sshd_config_lines, "LoginGraceTime", [login_grace_time])
        set_list_setting(sshd_config_lines, "Port", [default_port])
        # Write the updated configuration back to the file
        write_sshd_config(sshd_config_lines)
        restart_ssh()

    return render(request, 'ssh_management.html', {'form': form})

def ubugaurd_authentication(request):
    return render(request, 'ubugaurd_authentication.html')

def ubugaurd_passwd(request):
    pass

def ubugaurd_email(request):
    pass