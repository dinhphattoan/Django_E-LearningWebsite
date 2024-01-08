from django.db import models
from . import models
# Query all objects
@staticmethod
def deleteModelData(models):
    models.DocumentarySector.objects.delete()