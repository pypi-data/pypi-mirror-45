# ------------------------------------------------------------------------------
# Test Extra Info Page
# ------------------------------------------------------------------------------
import sys
import datetime as dt
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from wagtail.core.models import Page
from ls.joyous.models.calendar import CalendarPage
from ls.joyous.models.events import RecurringEventPage
from ls.joyous.models.events import ExtraInfoPage
from ls.joyous.utils.recurrence import Recurrence, WEEKLY, MO, WE, FR
from .testutils import datetimetz

# ------------------------------------------------------------------------------
class Test(TestCase):
    def setUp(self):
        self.home = Page.objects.get(slug='home')
        self.user = User.objects.create_user('i', 'i@bar.test', 's3(r3t')
        self.calendar = CalendarPage(owner = self.user,
                                     slug  = "events",
                                     title = "Events")
        self.home.add_child(instance=self.calendar)
        self.calendar.save_revision().publish()
        self.event = RecurringEventPage(slug      = "test-meeting",
                                        title     = "Test Meeting",
                                        repeat    = Recurrence(dtstart=dt.date(1988,1,1),
                                                               freq=WEEKLY,
                                                               byweekday=[MO,WE,FR]),
                                        time_from = dt.time(13),
                                        time_to   = dt.time(15,30))
        self.calendar.add_child(instance=self.event)
        self.info = ExtraInfoPage(owner = self.user,
                                  slug  = "1988-11-11-extra-info",
                                  title = "Extra Information for Friday 11th of November",
                                  overrides = self.event,
                                  except_date = dt.date(1988,11,11),
                                  extra_title = "System Demo",
                                  extra_information = "<h3>System Demo</h3>")
        self.event.add_child(instance=self.info)
        self.info.save_revision().publish()

    def testGetEventsByDay(self):
        events = RecurringEventPage.events.byDay(dt.date(1988,11,1),
                                                 dt.date(1988,11,30))
        self.assertEqual(len(events), 30)
        evod = events[10]
        self.assertEqual(evod.date, dt.date(1988,11,11))
        self.assertEqual(len(evod.all_events), 1)
        self.assertEqual(len(evod.days_events), 1)
        self.assertEqual(len(evod.continuing_events), 0)
        title, page, url = evod.days_events[0]
        self.assertEqual(title, "System Demo")
        self.assertIs(type(page), ExtraInfoPage)

    def testStatus(self):
        self.assertEqual(self.info.status, "finished")
        self.assertEqual(self.info.status_text, "This event has finished.")
        now = timezone.localtime()
        myday = now.date() + dt.timedelta(days=1)
        friday = myday + dt.timedelta(days=(4-myday.weekday())%7)
        futureInfo = ExtraInfoPage(owner = self.user,
                                   slug  = "fri-extra-info",
                                   title = "Extra Information for Friday",
                                   overrides = self.event,
                                   except_date = friday,
                                   extra_title = "It's Friday",
                                   extra_information = "Special")
        self.event.add_child(instance=futureInfo)
        self.assertIsNone(futureInfo.status)
        self.assertEqual(futureInfo.status_text, "")

    def testWhen(self):
        self.assertEqual(self.info.when, "Friday 11th of November 1988 at 1pm to 3:30pm")

    def testAt(self):
        self.assertEqual(self.info.at.strip(), "1pm")

    def testUpcomingDt(self):
        self.assertIsNone(self.info._upcoming_datetime_from)


    def testPastDt(self):
        self.assertEqual(self.info._past_datetime_from,
                         datetimetz(1988,11,11,13,0))

    def testGroup(self):
        self.assertIsNone(self.info.group)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
