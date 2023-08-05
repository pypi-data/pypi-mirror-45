from django.conf import settings
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=255, default='')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="skills")

    class Meta:
        permissions = (
            ('view_skill', 'Read'),
            ('control_skill', 'Control'),
        )

    def __str__(self):
        return self.name
