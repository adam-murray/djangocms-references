from django.db import models

from cms.models.pluginmodel import CMSPlugin

from ..polls.models import Poll


class NestedPoll(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)


class NestedPollPlugin(CMSPlugin):
    nested_poll = models.ForeignKey(NestedPoll, on_delete=models.CASCADE)


class DeeplyNestedPollPlugin(CMSPlugin):
    name = models.CharField(max_length=255)
    nested_poll = models.ForeignKey(NestedPoll, on_delete=models.CASCADE)
