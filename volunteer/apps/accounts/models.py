from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible

from authtools.models import AbstractEmailUser

from volunteer.apps.accounts.utils import obfuscate_email


@python_2_unicode_compatible
class User(AbstractEmailUser):
    @property
    def is_admin(self):
        return self.is_staff or self.is_superuser

    @property
    def profile(self):
        try:
            return self._profile
        except ObjectDoesNotExist:
            from volunteer.apps.profiles.models import Profile
            return Profile.objects.get_or_create(user=self)[0]

    @property
    def shifts(self):
        return tuple(set((
            shift_slot.shift
            for shift_slot
            in self.shift_slots.filter(cancelled_at__isnull=True).select_related('shift')
        )))

    def __str__(self):
        if self.pk is None:
            return "Unsaved User"
        if self.profile.display_name:
            return self.profile.display_name
        else:
            return obfuscate_email(self.email)
