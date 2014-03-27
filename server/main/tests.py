import datetime
import json
from django.contrib.contenttypes.models import ContentType

from server.main.helper import Generator
from django.test import TestCase
from server.main.models import TextAd, ImmediatelyAd, ImageAd, Partner, Days, Terminal
from django.core.files import File


class MainTest(TestCase):
    def test_generate_timetable(self):

        # Create models

        terminal = Terminal(text='description', config='config test')
        terminal.save()

        # Create partner
        partner = Partner(name='test name')
        partner.save()

        # Create image
        file_image = open('tmp.jpg', 'w+')
        file_image.write('test picture')

        image = ImageAd(prolongation=datetime.time(second=5),
                        partner=partner)

        image.image.save('tmp.jpg', File(file_image))
        image.save()

        # Create image for immediately
        file_image_im = open('tmp_im.jpg', 'w+')
        file_image_im.write('test picture immediately')

        image_im = ImageAd(prolongation=datetime.time(minute=1),
                           partner=partner)

        image_im.image.save('tmp_im.jpg', File(file_image_im))
        image_im.save()

        # Create text
        text = TextAd(text='test text...', partner=partner)
        text.save()

        # Create day
        day = Days(date=datetime.datetime.now(),
                   time_for_video=datetime.time(minute=5),
                   show_text=True,
                   time_for_text=datetime.time(minute=2, second=30),
                   show_video=False,
                   start_time=datetime.time(hour=8),
                   stop_time=datetime.time(hour=8, minute=30),
                   terminal=terminal)
        day.save()

        day.text_ad.add(text)
        day.save()

        # Create immediately
        immediately = ImmediatelyAd(day=day,
                                  time=datetime.time(hour=8, minute=25),
                                  content_type=ContentType.objects.get(model='imagead'),
                                  object_id=image_im.pk)
        immediately.save()

        # Result playlists in json

        result_playlist = [
                {'time': '08:00:00',
                 'action': [
                     {'action': 'start_video'},
                     {'action': 'start_text'},
                 ]},
                {'time': '08:05:00',
                 'action': [
                     {'action': 'start_text'},
                 ]},
                {'time': '08:07:30',
                 'action': [
                     {'action': 'start_video'},
                     {'action': 'start_text'},
                 ]},
                {'time': '08:12:30',
                 'action': [
                     {'action': 'start_text'},
                 ]},
                {'time': '08:15:00',
                 'action': [
                     {'action': 'start_video'},
                     {'action': 'start_text'},
                 ]},
                {'time': '08:20:00',
                 'action': [
                     {'action': 'start_text'},
                 ]},
                {'time': '08:22:30',
                 'action': [
                     {'action': 'start_video'},
                     {'action': 'start_text'},
                 ]},

                # Immediately start...
                {'time': '08:25:00',
                'action': [
                     {'action': 'immediately_start',
                      'params': '/home/videoad/uploads/videos/tmp_im.jpg'},
                ]},

                {'time': '08:26:00',
                 'action': [
                     {'action': 'start_text'},
                 ]},
                {'time': '08:28:30',
                 'action': [
                     {'action': 'start_video'},
                     {'action': 'start_text'},
                 ]},
            ]

        # Generate play list

        generator = Generator(day=day)
        playlist = generator.get_time_table()

        self.assertEqual(json.dumps(playlist), json.dumps(result_playlist))
