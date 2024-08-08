from django_api_admin.sites import APIAdminSite
from . import models,admin


class Site(APIAdminSite):
    pass

site = Site(name="api",include_auth=True)

site.register(models.MyApp)


