#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import make_option
import re
import datetime
from django.core.management import BaseCommand
from main.helper import PlaylistGenerator
from main.models import Days

RE_DATE = re.compile("\d{4}-\d{2}-\d{2}")

class Command(BaseCommand):
    """Генерирует playlist для одного дня"""

    option_list = BaseCommand.option_list + (
        make_option('-d', '--date', dest='date', help='Date in the format YYYY-MM-DD'),
        make_option('-l', '--list', dest='list_days', action="store_true", default=False, help='Displays a list of dates'),
        make_option('-a', '--all', dest='all_days', action="store_true", default=False, help='Generates plailist for all days'),
        make_option('-t', '--today', dest='today', action="store_true", default=False, help='Generates plailist for today'),
    )

    def handle(self, date, today, list_days, all_days, *args, **options):
        if list_days:
            print "List of available days: "
            for day in Days.objects.all():
                print str(day.date)
            print "Total days: %s" % Days.objects.count()
            return

        if today:
            print "Generates plailist for today %s ..." % datetime.datetime.now().strftime("%Y-%m-%d")

            try:
                day = Days.objects.get(date=datetime.datetime.now())
            except Days.DoesNotExist:
                print "Day %s does not exist" % date
                return
            else:
                generator = PlaylistGenerator(day=day)
                generator.run()

            print "\nGeneration successfully completed"

            return

        if all_days:
            print "Generates plailist for all days..."
            for day in Days.objects.all():
                PlaylistGenerator(day=day).run()
                print "Generate for %s" % str(day.date)

            print "The generation is completed. Total days: %s" % Days.objects.count()
            return

        if not date or not RE_DATE.match(date):
            print "Error! Enter the date in the format YYYY-MM-DD"
            return

        dateo = datetime.datetime.strptime(date, "%Y-%m-%d")

        try:
            day = Days.objects.get(date=dateo)
        except Days.DoesNotExist:
            print "Day %s does not exist" % date
            print "List of available days: "
            for day in Days.objects.all():
                print str(day.date)
            return
        else:
            generator = PlaylistGenerator(day=day)
            generator.run()

        print "\nGeneration successfully completed"

