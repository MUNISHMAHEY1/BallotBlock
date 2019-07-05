from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset,Row, \
    Column, ButtonHolder, Submit,Button
from django.forms.models import inlineformset_factory
from election.models import Candidate, ElectionConfig
import datetime

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
        
    '''
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        if start_time < datetime.datetime.now():
            raise forms.ValidationError("Check if the start time is set properly.")
    '''
    
    def clean_start_time(self):
        start_time = self.cleaned_data['start_time']
        if start_time < datetime.datetime.now():
            raise forms.ValidationError("Check if the start time is set properly.")
        
        return start_time

        #     if start_time < datetime.now():
        #         if end_time < datetime.now():
        #             if start_time > end_time:
        #                 msg='End time cannot end before the start time'
        #                 self.add_error('start_time', msg)
        #         msg ='End time cannot be in the past'
        #         self.add_error('end_time', msg)
        #     msg="Start time cannot be in the past."
        #     self.add_error('start_time',msg)


class electionconfigviewForm(forms.ModelForm):
    class Meta:
        model = ElectionConfig
        fields = '__all__'
        widgets = {
        'description': forms.TextInput(attrs={'readonly': 'readonly'}),
        'start_time': forms.TextInput(attrs={'readonly': 'readonly'}),
        'end_time': forms.TextInput(attrs={'readonly': 'readonly'}),
        'block_time_generation': forms.TextInput(attrs={'readonly': 'readonly'}),
        'guess_rate': forms.TextInput(attrs={'readonly': 'readonly'}),
        'min_votes_in_block': forms.TextInput(attrs={'readonly': 'readonly'}),
        'min_votes_in_last_block': forms.TextInput(attrs={'readonly': 'readonly'}),
        'attendance_rate': forms.TextInput(attrs={'readonly': 'readonly'}),
    }


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

                ),
            ),

        )




#ArticleFormSet = formset_factory(MyArticleForm)
#formset = ArticleFormSet(form_kwargs={'user': request.user})
