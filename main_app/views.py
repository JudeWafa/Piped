from django.shortcuts import render, redirect, get_object_or_404
from .forms import PipelineForm, StageForm, ItemForm
from django.contrib.auth.decorators import login_required
from .models import Pipeline, Stage, Item, ItemHistory
import json
from django.http import JsonResponse

# Create your views here.

def mainpage(request):
    return render(request, "Mainpage.html")

# @login_required
# def homepage(request):
#     return render(request, "Homepage.html")

@login_required
def viewAllPipelines(request):
    pipelines = Pipeline.objects.filter(user=request.user)
    return render(request, "pipelines/view_pipelines.html", {'pipelines': pipelines})

@login_required
def create_pipeline(request):
    if request.method == 'POST':
        form = PipelineForm(request.POST)
        if form.is_valid():
            pipeline = form.save(commit=False)
            pipeline.user = request.user
            pipeline.save()
            return redirect('pipeline_detail', pipeline_id=pipeline.id)
    else:
        form = PipelineForm()
    
    return render(request, 'pipelines/create_pipeline.html', {'form': form})


@login_required
def pipeline_detail(request, pipeline_id):
    pipeline = get_object_or_404(Pipeline, id=pipeline_id, user=request.user)
    stages = pipeline.stages.all()
    items = pipeline.items.all()


    if request.method == 'POST' and 'add_stage' in request.POST:
        stage_form = StageForm(request.POST)
        if stage_form.is_valid():
            stage = stage_form.save(commit=False)
            stage.pipeline = pipeline
            stage.save()
            return redirect('pipeline_detail', pipeline_id=pipeline.id)
        
    else:
        stage_form = StageForm()

    

    if request.method == 'POST' and 'add_item' in request.POST:
        item_form = ItemForm(request.POST)
        if item_form.is_valid():
            stage_id = request.POST.get('stage_id')
            stage = Stage.objects.get(id=stage_id)
            item = item_form.save(commit=False)
            item.pipeline = stage.pipeline
            item.stage = stage
            item.save()

            return redirect('pipeline_detail', pipeline_id=stage.pipeline.id)
    else:
        item_form = ItemForm()

    return render(request, 'pipelines/pipeline_page.html', {
        'pipeline': pipeline,
        'stages': stages,
        'stage_form': stage_form,
        'item_form': item_form,
    })


@login_required
def move_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        stage_id = data.get('stage_id')

        try:
            item = Item.objects.get(id=item_id)
            new_stage = Stage.objects.get(id=stage_id)

            item.stage = new_stage
            item.save()

            return JsonResponse({'status': 'success'})
        except (Item.DoesNotExist, Stage.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Item or stage not found'}, status=404)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)


