from django import forms
from .models import Pipeline, Stage, Item

class PipelineForm(forms.ModelForm):
    class Meta:
        model = Pipeline
        fields = ['name']

    
class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = ['name']


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description']
       