import datetime
import json
from django.contrib.contenttypes.models import ContentType

from main.helper import PlaylistGenerator
from django.test import TestCase
from main.models import TextAd, ImmediatelyAd, ImageAd, Partner, Days, Terminal
from django.core.files import File
from filebrowser.base import FileObject
from filebrowser.sites import site
import os


class MainTest(TestCase):
    def test_generate_timetable(self):

        # Create models

        terminal = Terminal(text='description', config='config test')
        terminal.save()

        # Create partner
        partner = Partner(name='test name')
        partner.save()

        # Create image
        image = ImageAd(prolongation=datetime.time(minute=5),
                        partner=partner,
                        image=FileObject(os.path.join(site.directory, "test", "testimage.jpg")))
        image.save()

        # Create image for immediately
        image_im = ImageAd(prolongation=datetime.time(minute=1),
                           partner=partner,
                           image=FileObject(os.path.join(site.directory, "test", "testimage_im.jpg")))
        image_im.save()

        # Create text
        text = TextAd(text='test text...', partner=partner)
        text.save()

        # Create day
        day = Days(date=datetime.datetime.now(),
                   video_count=2,
                   show_text=True,
                   text_count=4,
                   show_video=False,
                   start_time=datetime.time(hour=8),
                   stop_time=datetime.time(hour=8, minute=30),
                   terminal=terminal)
        day.save()

        day.image_ad.add(image)
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
            {'time': '08:00:00', 'params': [
                {'image': image.image.filename},
                {'image': image.image.filename},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text}
            ]},
            {'time': '08:10:00', 'params': [
                {'image': image.image.filename},
                {'image': image.image.filename},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text}
            ]},
            {'time': '08:20:00', 'params': [
                {'image': image.image.filename},
                {'image': image.image.filename},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text}
            ]},
            {'time': '08:25:00', 'params': [
                {'image': immediately.content_object.image.filename},
            ]},
            {'time': '08:26:00', 'params': [
                {'image': image.image.filename},
                {'image': image.image.filename},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text},
                {'text': text.text}
            ]}
        ]

        # Generate play list
        g = PlaylistGenerator(day=day)
        playlist = g.get_play_list()

        self.assertEqual(json.dumps(playlist), json.dumps(result_playlist))
