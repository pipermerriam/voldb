import datetime
import factory

from django.utils import timezone
from django.conf import settings

from volunteer.apps.shifts.models import (
    Shift,
    ShiftSlot,
)
from volunteer.apps.shifts.utils import DENVER_TIMEZONE


def today_at_hour(hour):
    return datetime.datetime.combine(
        datetime.date.today(),
        datetime.time(hour=hour, tzinfo=DENVER_TIMEZONE),
    )


def yesterday_at_hour(hour):
    return today_at_hour(hour) - datetime.timedelta(1)


def tomorrow_at_hour(hour):
    return today_at_hour(hour) + datetime.timedelta(1)


def get_default_event(*args, **kwargs):
    from volunteer.apps.events.models import Event
    current_event = Event.objects.get_current()
    if current_event is None or (
        not current_event.is_registration_open and settings.CURRENT_EVENT_ID is None
    ):
        open_at = timezone.now() - timezone.timedelta(10)
        close_at = timezone.now() + timezone.timedelta(10)

        current_event = Event.objects.create(
            name="Apogaea",
            registration_open_at=open_at,
            registration_close_at=close_at,
        )
    return current_event


class ShiftFactory(factory.DjangoModelFactory):
    event = factory.LazyAttribute(get_default_event)
    role = factory.SubFactory('tests.factories.departments.RoleFactory')
    start_time = factory.LazyAttribute(
        lambda x: today_at_hour(9)
    )
    shift_minutes = 3 * 60
    code = ''

    class Meta:
        model = Shift


class ShiftSlotFactory(factory.DjangoModelFactory):
    shift = factory.SubFactory(ShiftFactory)
    volunteer = factory.SubFactory('tests.factories.accounts.UserFactory')

    cancelled_at = None

    class Meta:
        model = ShiftSlot


class CancelledShiftSlotFactory(ShiftSlotFactory):
    cancelled_at = factory.LazyAttribute(lambda x: timezone.now())
