from election.models import Candidate, Position
import django_tables2 as tables
from django.utils.html import format_html


class CandidateTable(tables.Table):
    #actions = ProductActions(orderable=False) # custom tables.Column()
    id = tables.TemplateColumn('<a href="{% url \'candidate_change\' record.id %}">{{record.id}}</a>')
    delete = tables.TemplateColumn('<a href="{% url \'candidate_delete\' record.id %}"><i class="fas fa-trash-alt"></i></a>')


    class Meta:
        model = Candidate
        fields = ['id', 'name', 'position', 'delete'] # fields to display
        attrs = {'id': 'candidate_table'}
        orderable = False

class PositionTable(tables.Table):
    #actions = ProductActions(orderable=False) # custom tables.Column()
    #id = tables.TemplateColumn('<a href="{% url \'candidate_change\' record.id %}">{{record.id}}</a>')
    delete = tables.TemplateColumn('<a href="{% url \'position_delete\' record.id %}"><i class="fas fa-trash-alt"></i></a>')


    class Meta:
        model = Position
        fields = ['id', 'description', 'quantity', 'delete'] # fields to display
        attrs = {'id': 'position_table'}
        orderable = False
