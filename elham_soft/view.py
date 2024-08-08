from typing import Any
from django.contrib.admin import AdminSite
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.urls.resolvers import URLResolver
from django.urls import path
from django.http.response import JsonResponse
import json,zipfile,os,io,time
from django.conf import settings
BASE_DIR = settings.BASE_DIR
APPS_DIR = os.path.join(BASE_DIR,"apps")
apps_list = os.listdir(APPS_DIR)

class Site(AdminSite):
    index_template = "index.html"
    app_index_template = "app_index.html"
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        return super().index(request, extra_context)
    def app_index(self, request, app_label, extra_context=None):

        return super().app_index(request, app_label, extra_context)
    
    def get_urls(self):
        my_urls = [
            path("store_apps/",self.store_apps,name="store_apps"),
            path("new_apps/",self.new_apps,name="new_apps"),
            path("version_apps/",self.version_apps,name="version_apps"),
            path("add_app/",self.add_app,name="add_app"),
            path("app_<app_label>/",self.app_index,name="app_index"),
            
        ]
        return my_urls + super().get_urls()


    def store_apps(self,request):
        context = {}
        return TemplateResponse(request,"store_apps.html",context)
    def new_apps(self,request):
        context = {}
        return TemplateResponse(request,"new_apps.html",context)
    def version_apps(self,request):
        context = {}
        return TemplateResponse(request,"version_apps.html",context)
    
    def add_app(self,request):
        message = "هناك خطئ غير معروف"
        is_error = True
        
        if request.method == "POST":
            file = request.FILES.get('file')
            print(file)
            if file:
                if file.content_type == 'application/x-zip-compressed':
                    with zipfile.ZipFile(file) as zf:
                        dir_name = zf.namelist()[0]
                        if f"{dir_name}detail.json" in zf.namelist():
                            with open(f"{dir_name}detail.json","r") as detail:
                                data = json.loads(detail.read().encode("utf-8"))
                                print(data)
                                if not data["app_name"] in apps_list:
                                    zf.extractall(APPS_DIR)
                                    with open(os.path.join(os.path.join(BASE_DIR,"pr"),"urls.py"),"a") as ur:
                                        ur.write("\n#")
                                        
                                    message = "تم"
                                    is_error = False
                                    
                                else:
                                    message = "موجود مسبقا"
                        else:
                            message = "ليس ملف تطبيق"
                else:
                    message = "ليس ملف تطبيق"
            else:
                message = "حمل الملف أولا..."
        
                    

        return JsonResponse(data={"message":message,"is_error":is_error})

site = Site(name="view")

