from collections.abc import MutableMapping
from typing import Any
from django.db import models
from django.contrib.auth import models as auth_models
from django.urls import reverse
from django.contrib.contenttypes import models as contenttype_models
from django.contrib.contenttypes import fields as contenttype_fields
from django.db.models import Model
from django.utils.translation import gettext as _
from django.forms import ValidationError
import zipfile
import json,os
from django.apps import apps
from django.conf import settings
BASE_DIR = settings.BASE_DIR
APPS_DIR = os.path.join(BASE_DIR,"apps")
apps_list = os.listdir(APPS_DIR)





class AccountManagement(models.Model):
    class Meta:
        abstract = True
        verbose_name = "حساب رئيسي"
class AccountBranch(models.Model):
    class Meta:
        abstract = True
        verbose_name = "حساب فرعي"

class Account(models.Model):
    name = models.CharField(_("name"), max_length=50)
    account_type = models.CharField(_("account_type"), max_length=50,choices=[
        (AccountManagement.__name__,AccountManagement._meta.verbose_name),
        (AccountBranch.__name__,AccountBranch._meta.verbose_name),
        
    ])
    account = models.ForeignKey("Account", verbose_name=_("account"), on_delete=models.CASCADE,null=True,blank=True,related_name="account_account")


    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.name


class App(models.Model):
    """is_version = models.BooleanField(_("is_version"),default=False)
    app = models.ForeignKey("App", verbose_name=_("app"), on_delete=models.CASCADE,related_name="app_app",null=True,blank=True)
    name = models.CharField(_("name"), max_length=50,null=True,blank=True)
    verbose_name = models.CharField(_(""), max_length=50)"""
    zip_file = models.FileField(_("zip_file"), upload_to="apps/zipfiles", max_length=100,null=True,blank=True)
    #app_dir = models.FilePathField(_("app_dir"), path=None, match=None, max_length=100)

    class Meta:
        verbose_name = _("App")
        verbose_name_plural = _("Apps")

    def __str__(self):
        return self.name

class AccountApp(models.Model):
    account = models.ForeignKey("Account", verbose_name=_("account"), on_delete=models.CASCADE)
    app = models.ForeignKey(App, verbose_name=_("app"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("AccountApp")
        verbose_name_plural = _("AccountApps")

    def __str__(self):
        return self.name



class MyApp(models.Model):

    zip_file = models.FileField(_("zip_file"), upload_to="myapps/zipfiles", max_length=100,null=True,blank=True)

    
    class Meta:
        verbose_name = _("MyApp")
        verbose_name_plural = _("MyApps")
 
    
    def clean(self):
        if not self.zip_file:
            raise ValidationError({"zip_file":"مطلوب"})
        with zipfile.ZipFile(self.zip_file) as zf:
            dir_name = zf.namelist()[0]
            print(dir_name)
            with open(f"{dir_name}detail.json","r") as detail:
                data = json.loads(detail.read().encode("utf-8"))
                print(data)
                if not data["app_name"] in apps_list:
                    zf.extractall(APPS_DIR)
                else:
                    raise ValidationError("موجود")
        return super().clean()
    
