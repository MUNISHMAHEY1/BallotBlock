from django.contrib import admin
from election.business import ElectionBusiness
from chain.models import BlockStructure
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

class BlockHandler(ElectionAdminControl):
    list_display = ['id', 'BlockNo','ParentHash']
    #list_editable = ['user']

admin.site.register(BlockStructure, BlockHandler)
