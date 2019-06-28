from election.models import ElectionConfig
from django.contrib import messages
import datetime

class ElectionBusiness():

    def getCurrentElectionConfig(self):
        ecs = ElectionConfig.objects.all()
        if ecs.count() > 0:
            return ecs[0]
        return None

    def canModify(self, request=None):
        ec = self.getCurrentElectionConfig()
        if ec:
            now = datetime.datetime.now()
            if ec.locked and now >= ec.start_time and now <= ec.end_time:
                if request:
                    msg = 'Election is locked and end time is {}'.format(ec.end_time.isoformat())
                    messages.error(request, msg)
                return False
        return True

    def canAdd(self, request=None):
        if ElectionConfig.objects.all().count() > 0:
            if request:
                msg = 'Add more than one election config is forbidden'
                messages.error(request, msg)
            return False
        return True
        