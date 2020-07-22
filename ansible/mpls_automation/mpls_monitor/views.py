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
	try:
		output, err = result.communicate(timeout=15)
  		#pprint.pprint(outs.decode().split('\n'))
	except subprocess.SubprocessError as errs:
		proc.kill()
		sys.exit("Error: {}".format(errs))
	return JsonResponse(json.loads(output))
