from django.dispatch import receiver
from django.db.models.signals import pre_save
from election.models import ElectionConfig
import datetime
from django.core.exceptions import ValidationError

@receiver(pre_save, sender=ElectionConfig)
def canModify(sender, instance, **kwargs):
    if ElectionConfig.objects.count() > 0 and instance.id is None:
        # We can not have more than one election config
        raise ValidationError('Add more than one election config is forbidden')
    
    if instance.id:
        now = datetime.datetime.now()
        if instance.locked and now <= instance.end_time:
            raise ValidationError('Election is locked until {}'.format(instance.end_time))

