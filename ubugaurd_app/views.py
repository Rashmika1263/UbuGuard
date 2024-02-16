from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import SearchEntry

# Create your views here.
# def about(request):
#     return redirect('/logs_monitoring/system')

def about(request):
    return render(request, 'about.html')


def search_view(request):
    query = request.GET.get('query', '')
    results = SearchEntry.objects.filter(name__icontains=query)
    data = [{'name': result.name, 'url': result.url} for result in results]
    return JsonResponse(data, safe=False)