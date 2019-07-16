from chain.models import BBlock
import django_tables2 as tables
from django.utils.html import format_html


class BBlockTable(tables.Table):
    #id = tables.TemplateColumn('<a href="#">{{record.id}}</a>')
    
    class Meta:
        model = BBlock
        fields = ['id', 'timestamp_iso', 'parent_hash', 'hash_of_database_hash', 'hash_of_source_code_hash', 'candidate_votes', 'total_votes', 'block_hash']
        attrs = {'id': 'bblock_table', 'class': 'table table-sm'}
        orderable = False


