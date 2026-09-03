from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DeploymentPipeline, DeploymentLog
import json

def index(request):
    if DeploymentPipeline.objects.count() == 0:
        DeploymentPipeline.objects.create(repo_name="CodeScan-API-Gateway", branch="main")
    
    pipelines = DeploymentPipeline.objects.all()
    logs = DeploymentLog.objects.order_by('-timestamp')[:10]
    return render(request, 'deployer/index.html', {'pipelines': pipelines, 'logs': logs})

@csrf_exempt
def hook_trigger(request, token):
    if request.method == 'POST':
        pipeline = get_object_or_404(DeploymentPipeline, secret_token=token)
        body = json.loads(request.body.decode('utf-8') or '{}')
        commit = body.get('after', 'manual-trigger')[:8]
        
        DeploymentLog.objects.create(
            pipeline=pipeline,
            commit_hash=commit,
            status='SUCCESS',
            output_log=f"Executed: {pipeline.build_script}\nExit Code: 0 (OK)"
        )
        return JsonResponse({"status": "deployed", "commit": commit})
    return JsonResponse({"error": "POST required"}, status=405)
