from django import forms
from crispy_forms.helper import FormHelper
from django.forms.models import inlineformset_factory
from election.models import Candidate

class VoteForm(forms.Form):

    position = forms.HiddenInput()
    candidate = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Candidate.objects.none(), label='')

    def __init__(self, *args, position, **kwargs):
        self.fields["candidate"].queryset = Candidate.objects.filter(position=position)
        super().__init__(*args, **kwargs)
    
    
    
#ArticleFormSet = formset_factory(MyArticleForm)
#formset = ArticleFormSet(form_kwargs={'user': request.user})
