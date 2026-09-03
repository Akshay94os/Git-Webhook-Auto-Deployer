from django.contrib import admin
from .models import DeploymentPipeline, DeploymentLog
admin.site.register(DeploymentPipeline)
admin.site.register(DeploymentLog)
