from django.shortcuts import render
from django.views import View
from django.http import HttpResponse

# Create your views here.
class Views(View):
    
    def get(self, request):
        return render(request,"index.html")
