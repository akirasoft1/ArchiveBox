from typing import Any, ClassVar, Iterable
from django.db import models
from django.contrib.auth import get_user_model

class AutoDateTimeField(models.DateTimeField):
    # def pre_save(self, model_instance, add):
    #     return timezone.now()
    pass

def get_or_create_system_user_pk(username='system'):
    """Get or create a system user with is_superuser=True to be the default owner for new DB rows"""

    User = get_user_model()

    # if only one user exists total, return that user
    if User.objects.filter(is_superuser=True).count() == 1:
        return User.objects.filter(is_superuser=True).values_list('pk', flat=True)[0]

    # otherwise, create a dedicated "system" user
    user, _was_created = User.objects.get_or_create(username=username, is_staff=True, is_superuser=True, defaults={'email': '', 'password': ''})
    return user.pk

class ModelWithReadOnlyFields(models.Model):
    """
    Base class for models that have some read-only fields enforced by .save().
    """
    read_only_fields: ClassVar[tuple[str, ...]] = ()
    
    class Meta:
        abstract = True
        
    def _fresh_from_db(self):
        try:
            return self.objects.get(pk=self.pk)
        except self.__class__.DoesNotExist:
            return None
    
    def diff_from_db(self, keys: Iterable[str]=()) -> dict[str, tuple[Any, Any]]:
        """Get a dictionary of the fields that have changed from the values in the database"""
        keys = keys or [field.name for field in self._meta.get_fields()]
        if not keys:
            return {}
        
        in_db = self._fresh_from_db()
        if not in_db:
            return {}
    
        diff = {}
        for field in keys:
            new_value = getattr(self, field, None)
            existing_value = getattr(in_db, field, None)
            if new_value != existing_value:
                diff[field] = (existing_value, new_value)
        return diff
        
    def save(self, *args, **kwargs) -> None:
        diff = self.diff_from_db(keys=self.read_only_fields)
        if diff:
            changed_key = next(iter(diff.keys()))
            existing_value, new_value = diff[changed_key]
            raise AttributeError(f'{self}.{changed_key} is read-only and cannot be changed from {existing_value} -> {new_value}')
        super().save(*args, **kwargs)
