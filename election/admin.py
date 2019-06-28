from django.contrib import admin
from election.models import ElectionConfig, Elector, Position, Candidate
from election.business import ElectionBusiness

class ElectionAdminControl(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        if ElectionBusiness().canModify(None):
            return super().has_change_permission(request, obj)
        return False
    
    def has_add_permission(self, request):
        if ElectionBusiness().canModify(None):
            return super().has_add_permission(request)
        return False

    def has_delete_permission(self, request, obj=None):
        if ElectionBusiness().canModify(None):
            return super().has_delete_permission(request, obj)
        return False


class ElectionConfigAdmin(ElectionAdminControl):
    list_display = ['id', 'start_time', 'end_time', 'block_time_generation', 'guess_rate', 'min_votes_in_block', 'min_votes_in_last_block', 'attendance_rate', 'locked']
    list_editable = ['start_time', 'end_time', 'block_time_generation', 'guess_rate', 'min_votes_in_block', 'min_votes_in_last_block', 'attendance_rate', 'locked']

    def has_add_permission(self, request):
        if ElectionConfig.objects.all().count() > 0:
            return False
        return super().has_add_permission(request)

class ElectorAdmin(ElectionAdminControl):
    list_display = ['id', 'user']
    #list_editable = ['user']

class PositionAdmin(ElectionAdminControl):
    list_display = ['id', 'description', 'quantity']
    list_editable = ['description', 'quantity']

class CandidateAdmin(ElectionAdminControl):
    list_display = ['id', 'name', 'position']
    list_editable = ['name', 'position']

admin.site.register(ElectionConfig, ElectionConfigAdmin)
admin.site.register(Elector, ElectorAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Candidate, CandidateAdmin)

