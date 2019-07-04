from django_cron import CronJobBase, Schedule
from election.models import ElectionConfig
import logging

class BlockChainCronJob(CronJobBase):

    RUN_EVERY_MINS = 15    
    if ElectionConfig.objects.all().count() > 0:
        ec = ElectionConfig.objects.all()[0]
        RUN_EVERY_MINS = ec.block_time_generation

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'chain.block_chain_cron_job'    # a unique code

    def do(self):

        #TODO: Call the block generator function

        logger = logging.getLogger(__name__)
        logger.info('Info log test')
        logger.debug('Debug log test')
        logger.error('Error log test')

        print("Block chain cron job is running...")
