from django.contrib import admin
from election.models import ElectionConfig, Elector, Position, Candidate

class ElectionConfigAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time', 'block_time_generation', 'guess_rate', 'min_votes_in_block', 'min_votes_in_last_block', 'attendance_rate']
    list_editable = ['start_time', 'end_time', 'block_time_generation', 'guess_rate', 'min_votes_in_block', 'min_votes_in_last_block', 'attendance_rate']

class ElectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_editable = ['user']

class PositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'quantity']
    list_editable = ['description', 'quantity']

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'position']
    list_editable = ['name', 'position']

admin.site.register(ElectionConfig, ElectionConfigAdmin)
admin.site.register(Elector, ElectorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)

