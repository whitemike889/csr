from django.forms import ModelForm
from data.models import Task
from django import forms

class MenuItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MenuItemForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            field = self.fields.get(fieldname)
            if field:
                if type(field.widget) in (forms.TextInput, forms.DateInput):
                    field.widget = forms.TextInput(attrs={'placeholder': field.label},)

    class Meta:
        model = Task
        fields = ('timestarted',)
        widgets = {'timestarted': forms.HiddenInput()}
