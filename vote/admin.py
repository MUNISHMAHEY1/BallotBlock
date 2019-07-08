from django.contrib import admin
from vote.models import Voted, CandidateVote
from election.business import ElectionBusiness
# Register your models here.

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

class voters_voted(ElectionAdminControl):
    list_display = ['id', 'elector','hash_val']
    #list_editable = ['user']

class CandidateaVoteCount(ElectionAdminControl):
    list_display = ['id', 'candidate','quantity']
    #list_editable = ['user']

admin.site.register(Voted, voters_voted)
admin.site.register(CandidateVote, CandidateaVoteCount)
