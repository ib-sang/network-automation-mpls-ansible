from django.shortcuts import render
import subprocess, json
from django.http import JsonResponse, HttpResponse


def index(request):
	DeviceList = [('R1 - Cisco ios', 'R1'), ('R2 - Cisco ios', 'R2'),
	 				('R3 - Junos srx', 'R3'), ('R4 - Cisco ios xr', 'R4'),
	 				]
	return render(request, 'index.html', {'DeviceList': DeviceList})


def ping_test(request):
	device = request.POST.get('device-name') 
	result = subprocess.Popen(['ansible-playbook', 'ping-playbook.yml', '--extra-vars', 'host='+device ], stdout=subprocess.PIPE)
	output, err = result.communicate()
	return HttpResponse(resulr)
	return JsonResponse(json.loads(output))
