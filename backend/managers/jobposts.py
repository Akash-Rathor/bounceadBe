from django.db import models
from backend.utils.datetime import datetime


class JobsPostsManager(models.Manager):
    
    def get_active_and_not_deleted(self):
        return self.filter(is_active=True, deleted=False)
    
    def delete(self, queryset=None):
        """Soft delete the objects by setting deleted=True."""
        # If a queryset is provided, soft delete the objects in the queryset
        if queryset is None:
            queryset = self.get_queryset()
        queryset.update(deleted=True, is_active=False , deleted_at=datetime.get_date_time())
        


