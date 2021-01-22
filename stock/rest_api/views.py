import json
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Create your views here.


@method_decorator(csrf_exempt, name="dispatch")
class IndexView(View):
    def get(self, request):
        return

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        return HttpResponse(status=200)