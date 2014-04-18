#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from optparse import make_option
import re
import datetime
from django.core.management import BaseCommand
from main.helper import PlaylistGenerator
from main.models import Days

RE_DATE = re.compile("\d\d\d\d-\d\d-\d\d")

class Command(BaseCommand):
    """Генерирует playlist для одного дня"""

    option_list = BaseCommand.option_list + (
        make_option('-d', '--date', dest='date', help='Date in the format YYYY-MM-DD'),
        make_option('-l', '--list', dest='list_days', action="store_true", default=False, help='Displays a list of dates'),
        make_option('-a', '--all', dest='all_days', action="store_true", default=False, help='Generates plailist for all days'),
    )

    def handle(self, date, list_days, all_days, *args, **options):
        print "List of available days: "
        if list_days:
            for day in Days.objects.all():
                print str(day.date)
            print "Total days: %s" % Days.objects.count()
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

