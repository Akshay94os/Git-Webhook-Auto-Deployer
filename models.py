from django.db import models
import uuid

class DeploymentPipeline(models.Model):
    repo_name = models.CharField(max_length=120)
    branch = models.CharField(max_length=50, default='main')
    secret_token = models.CharField(max_length=64, blank=True)
    build_script = models.TextField(default='git pull origin main && python manage.py migrate')
    last_deployed = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.secret_token:
            self.secret_token = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.repo_name} ({self.branch})"

class DeploymentLog(models.Model):
    pipeline = models.ForeignKey(DeploymentPipeline, on_delete=models.CASCADE, related_name='logs')
    commit_hash = models.CharField(max_length=40)
    status = models.CharField(max_length=20, default='SUCCESS')
    output_log = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
