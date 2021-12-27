from django.db import models


class MyCampaign(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    objective = models.CharField(max_length=255, blank=True, null=True)


class MyAdset(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    campaign_id = models.CharField(max_length=255)
    lifetime_budget = models.CharField(max_length=255)
    daily_budget = models.CharField(max_length=255)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    targeting = models.JSONField()
    bid_amount = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    optimization_goal = models.CharField(max_length=255, blank=True, null=True)


class MyAdImage(models.Model):
    """
        {'images': {'gucci-bag.jpg': {
        'hash': '4f9914935a345227409b2cc7f811928c',
        'url': 'https://scontent.fadb2-2.fna.fbcdn.net/v/t45.1600-4/269780490_120330000091595109_3551065005542236_n.jpg?_nc_cat=100&ccb=1-5&_nc_sid=2aac32&_nc_ohc=nAcwL_amSVcAX8-PH5U&_nc_ht=scontent.fadb2-2.fna&edm=AJNyvH4EAAAA&oh=00_AT-RpEkCDTMp97kxR48dtaqEg7oeYQ2VAyhMDtNr0uaqgA&oe=61CC6990'}}}

    """

    hash = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField(max_length=500, blank=True, null=True)


class MyAdCreative(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    object_story_spec = models.JSONField(blank=True, null=True)
