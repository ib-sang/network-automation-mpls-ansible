from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse




def index(request):
    #return HttpResponse('hello home page')
    #publish(topic="LimitBreach/J", payload="Jitter Limit breach", qos=1, retain=False)
    ctx = {}
    return render(request, 'index.html', context=ctx)