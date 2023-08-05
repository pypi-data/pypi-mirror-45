from django.db import models


class CacheKeyManager(models.Manager):
    def get_keys(self, site_id=None, language=None):
        if not site_id and not language:
            ret = self.all()
        elif not site_id:
            ret = self.filter(language=language)
        elif not language:
            ret = self.filter(site=site_id)
        else:
            ret = self.filter(self=site_id).filter(language=language)
        return ret


class CacheKey(models.Model):
    language = models.CharField(max_length=255)
    site = models.PositiveIntegerField()
    key = models.CharField(max_length=255)
    objects = CacheKeyManager()
