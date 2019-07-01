from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,Row, \
    Column, ButtonHolder, Submit,Button
from django.forms.models import inlineformset_factory
from election.models import Candidate, ElectionConfig

class VoteForm(forms.Form):

    position = forms.HiddenInput()
    candidate = forms.ModelChoiceField(widget=forms.RadioSelect, queryset=Candidate.objects.none(), label='')

    def __init__(self, *args, position, **kwargs):
        self.fields["candidate"].queryset = Candidate.objects.filter(position=position)
        super().__init__(*args, **kwargs)

class ElectionConfigForm(forms.ModelForm):
    class Meta:
        model = ElectionConfig
        fields = '__all__'
        #fields = ['pub_date', 'headline', 'content', 'reporter']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset(
                'Configuration Data',
                Row(
                    Column('description', css_class='form-group col-md-4 mb-0'),
                    Column('start_time', css_class='form-group col-md-4 mb-0'),
                    Column('end_time', css_class='form-group col-md-4 mb-0'),
                    Column('block_time_generation', css_class='form-group col-md-4 mb-0'),
                    Column('guess_rate', css_class='form-group col-md-4 mb-0'),
                    Column('min_votes_in_block', css_class='form-group col-md-4 mb-0'),
                    Column('min_votes_in_last_block', css_class='form-group col-md-4 mb-0'),
                    Column('attendance_rate', css_class='form-group col-md-4 mb-0'),
                    Column('locked', css_class='form-group col-md-4 mb-0'),
                    #css_class='form-row'
                ),
            ),

        )



#ArticleFormSet = formset_factory(MyArticleForm)
#formset = ArticleFormSet(form_kwargs={'user': request.user})
