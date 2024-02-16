from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import FirewallRuleForm
from .models import FirewallRule
import subprocess
from .scripts.firewall import (
    check_ufw_status,
    enable_ufw,
    disable_ufw
)

# Create your views here.
def network_management(request):
    return redirect('/network_management/firewall_management')

def firewall_management(request):
    if request.method == 'POST':
        action = request.POST.get('method')
        # print("METHOD WAS "+request.POST.get('method'))
        
        if action == 'add':
            # Handle adding a new rule
            form_data = {
                'port': request.POST.get('port'),
                'protocol': request.POST.get('protocol'),
                'source_ip': request.POST.get('source_ip'),
                'action': request.POST.get('action'),
            }

            form = FirewallRuleForm(form_data)
            if form.is_valid():
                rule = form.save()

                # Configure the firewall using subprocess (adjust the command as needed)
                command = f"sudo ufw {rule.action} from {rule.source_ip} to any port {rule.port} proto {rule.protocol}"
                subprocess.run(command, shell=True)

                return JsonResponse({'success': True, 'message': 'Rule added successfully'})
            else:
                return JsonResponse({'success': False, 'errors': form.errors})

        elif action == 'remove':
            # Handle removing selected rules
            rule_ids = request.POST.getlist('removeRule')
            rules = FirewallRule.objects.filter(id__in=rule_ids)

            for rule in rules:
                delete_command = f"sudo ufw delete {rule.action} from {rule.source_ip} to any port {rule.port} proto {rule.protocol}"

                # Execute the ufw delete command
                try:
                    subprocess.run(delete_command, shell=True, check=True)
                except subprocess.CalledProcessError as e:
                    return JsonResponse({'success': False, 'message': f'Error deleting ufw rule: {e.stderr}'})
            
            FirewallRule.objects.filter(id__in=rule_ids).delete()

            return JsonResponse({'success': True, 'message': 'Rules removed successfully'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method'})
    if request.method == 'GET':
        query = request.GET.get('set_status',None)
        if query and query == 'enable':
            enable_ufw()
            return redirect('/network_management/firewall_management')
        if query and query == 'disable':
            disable_ufw()
            return redirect('/network_management/firewall_management')
            
        else:
            form = FirewallRuleForm()
            rules = FirewallRule.objects.all()
            status = check_ufw_status()
            data = {
                "status":status,
                "num_rules":len(rules)
            }
            return render(request, 'firewall_management.html', {'rules': rules,'form': form,'data':data})

    # return render(request, 'firewall_management.html', {'form': form})

def vpn_setting(request):
    return render(request, 'vpn.html')

def tor_setting(request):
    return render(request, 'tor.html')