from election.models import Candidate
import django_tables2 as tables
from django.utils.html import format_html


class CandidateTable(tables.Table):
    #actions = ProductActions(orderable=False) # custom tables.Column()
    id = tables.TemplateColumn('<a href="/candidate/{{record.id}}/change">{{record.id}}</a>')
    delete = tables.TemplateColumn('<a href="/candidate/{{record.id}}/delete"><i class="fas fa-trash-alt"></i></a>')
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'delete'] # fields to display
        attrs = {'id': 'candidate_table'}
        orderable = False