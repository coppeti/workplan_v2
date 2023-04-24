import calendar
import locale
from datetime import date, datetime, timedelta

from django.db.models import Q

from holidays.holidays import Holidays

from accounts.models import CustomUser
from events.models import Events


locale.setlocale(locale.LC_ALL, 'de_DE')


def holy_day(date, year):
    """Returns a specific class if the given date is a holiday"""
    if date in Holidays(year).hdays():
        return 'feiertage'
    elif date in Holidays(year).other_hdays():
        return 'andere_feiertage'
    else:
        return ''


def date_between(start, end):
    """Returns a tuple of all dates contained between a start date and an end date, both included."""
    start_date = date.fromisoformat(str(start))
    end_date = date.fromisoformat(str(end))
    delta = end_date - start_date
    dates = {(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)}
    return sorted(dates)


def user_month_events(user, year, month):
    """Returns a dict of all events of a user for a given month and year.
    The dict is composed of the dates in key and the short name of the activity in value."""
    user_events = {}
    events = Events.objects.filter(Q(user_id=user), Q(confirmed=True), Q(is_active=True),
                                   Q(date_start__year=year, date_start__month=month) |
                                   Q(date_stop__year=year, date_stop__month=month))
    for event in events:
        dates = date_between(event.date_start, event.date_stop)
        for date in dates:
            user_events[date] = event.activity_id.short_name, event.activity_id.activity_class
    return user_events


def user_line(cal, user, year, month):
    v = []
    a = v.append
    be_hdays = Holidays(year).hdays()
    other_hdays = Holidays(year).other_hdays()
    user_events = user_month_events(user, year, month)
    for month_date in cal.itermonthdates(year, month):
        if month_date.month == month:
            a('<td class="text-center')
            if month_date in be_hdays:
                a(' feiertage')
            elif month_date in other_hdays:
                a(' andere_feiertage')
            elif not user_events.get(month_date.strftime('%Y-%m-%d')) and (month_date.weekday() == 5 or month_date.weekday() == 6):
                a(' wochenende')
            for date, activity in user_events.items():
                if month_date.strftime('%Y-%m-%d') in date:
                    if not 'P' in activity[0] and not 'S' in activity[0] and (month_date.weekday() == 5 or
                                               month_date.weekday() == 6):
                        a(' wochenende')
                    elif not 'P' in activity[0] and not 'S' in activity[0] and month_date in be_hdays:
                        a(' feiertage')
                    elif not 'P' in activity[0] and not 'S' in activity[0] and month_date in other_hdays and \
                            (month_date.weekday() == 5 or month_date.weekday() == 6):
                        a(' andere_feiertage')
                    else:
                        a(f' {activity[1]}')
            a('">')
            for date, activity in user_events.items():
                if month_date.strftime('%Y-%m-%d') in date:
                    if not 'P' in activity[0] and not 'S' in activity[0] and (month_date.weekday() == 5 or
                                               month_date.weekday() == 6 or
                                               month_date in be_hdays):
                        a('')
                    elif activity[0] == 'P' and month_date.weekday() == 5:
                        a('PSA')
                    elif activity[0] == 'P' and (month_date.weekday() == 6 or
                                                 month_date in be_hdays):
                        a('PSO')
                    else:
                        a(f' {activity[0]}')
        a('</td>\n')
    return ''.join(v)


def holiday_line(cal, year, month):
    v = []
    a = v.append
    a('<tr>\n')
    be_hdays = Holidays(year).hdays()
    other_hdays = Holidays(year).other_hdays()
    for d in cal.itermonthdates(year, month):
        if d.month == month:
            a('<td class="holyday_cell')
            if d in other_hdays:
                a(' andere_feiertage"><div class="holiday_line">')
                a(f'{other_hdays.get(d)}')
            elif d in be_hdays:
                a(' feiertage"><div class="holiday_line">')
                a(f'{be_hdays.get(d)}')
            elif d in Holidays(year + 1).other_hdays():
                a(' andere_feiertage"><div class="holiday_line">')
                a(f'{Holidays(year + 1).other_hdays().get(d)}')
            elif d in Holidays(year + 1).hdays():
                a(' feiertage"><div class="holiday_line">')
                a(f'{Holidays(year + 1).hdays().get(d)}')
            elif d.weekday() == 5 or d.weekday() == 6:
                a(' wochenende"><div class="holiday_line">')
                a(' ')
            else:
                a('">&nbsp;\n')
            a('</div></td>')
    a('</tr>')
    return ''.join(v)


class CustomCalendar(calendar.HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    def formatmonthname(self, year, month, withyear=True):
        if withyear:
            string = f'{calendar.month_name[month]} {year}'
        else:
            string = f'{calendar.month_name[month]}'
        return f'<th rowspan="2" id="{ month }" class="text-center {self.cssclass_month_head}">{string}</th>'

    def formatmonth(self, year, month, withyear=False):
        v = []
        a = v.append
        a(f'<tr class="{self.cssclass_month_head}">\n')
        a(f'{self.formatmonthname(year, month, withyear=withyear)}\n')
        for d, date_name in self.itermonthdays2(year, month):
            if d != 0:
                a('<td class="weekday_shortname ')
                if (date(year, month, d).isocalendar()[2] == 6 or
                    date(year, month, d).isocalendar()[2] == 7):
                    a('wochenende ')
                a(holy_day(date(year, month, d), year) + ' ')
                a(f'">{calendar.day_abbr[date_name]} ')
                if date(year, month, d).isocalendar()[2] == 1 or d == 1:
                    week_nbr =date(year, month, d).isocalendar()[1]
                    a(f'<span class="bg-danger text-light rounded-circle week_nbr">{week_nbr:02d}</span>')
                a('</td>\n')
        a('</tr>\n')
        a(holiday_line(self, year, month))
        return ''.join(v)

    def formatuser(self, year, month):
        v = []
        a = v.append
        users = CustomUser.objects.order_by('last_name')
        for user in users:
            a('<tr class="user_line">\n')
            a(f'<td class="ps-1">{user.last_name.upper()}</td>\n')
            a(user_line(self, user.pk, year, month))
            a('</tr>\n')
        return ''.join(v)

    def formatyear(self, year):
        v = []
        a = v.append
        for i in range(calendar.January, calendar.January + 12):
            a(self.formatmonth(year, i))
            a(self.formatuser(year, i))
        a(self.formatmonth(year + 1, 1, withyear=True))
        a(self.formatuser(year + 1, 1))
        return ''.join(v)