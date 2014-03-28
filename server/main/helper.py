import json
import datetime
from main.models import VideoAd, TextAd, ImageAd
from utils import Generator

__author__ = 'lkot'


class PlaylistGenerator(object):
    def __init__(self, day):
        self.day = day

    def time_to_seconds(self, time):
        """
        Convert datetime.time -> int::second
        """
        return time.hour*3600 + time.minute*60 + time.second

    def seconds_to_time(self, seconds):
        """
        Convert int::second -> datetime.time
        """
        h = seconds/3600

        return datetime.time(hour=h, minute=(seconds-(h*3600))/60, second=(seconds-(h*3600))%60)

    def get_chunk_duration(self, videos):
        """
        Returne duration in second for chunk (video or image or text)
        chunk elemens must have a prolongation 'property'
        """
        return sum(map(lambda x: self.time_to_seconds(x.prolongation), videos))

    def get_params_list(self, ads):
        return map(self.get_params, ads)

    def get_params(self, ad):
        if ad._meta.model == VideoAd:
            return {'video': ad.file_video.filename}
        elif ad._meta.model == TextAd:
            return {'text': ad.text}
        elif ad._meta.model == ImageAd:
            return {'image': ad.image.filename}

    def is_immediately(self, ctime, nxd):

        def get_offset(im):
            return self.time_to_seconds(im.content_object.prolongation)

        immediatelies = list(self.day.immediatelies.all())

        times_im = {}

        # Generate times_im
        for im in immediatelies:
            times_im[str(self.time_to_seconds(im.time))] = im

        print times_im

        for time in times_im:
            if ctime < int(time) < nxd:
                return {'time': self.seconds_to_time(int(time)),
                        'params': self.get_params(getattr(times_im[time], 'content_object')),
                        'offset': get_offset(times_im[time])}

        return False

    def get_play_list(self):
        """
        Base method, run generate playlist
        """
        ad_list = Generator(list(self.day.video_ad.all()) + list(self.day.image_ad.all()))
        chunk_len = self.day.video_count
        block, playlist = {}, []

        ctime = self.time_to_seconds(self.day.start_time)
        while ctime < self.time_to_seconds(self.day.stop_time):
            next_chunk = ad_list[:chunk_len]
            next_chunk_duration = self.get_chunk_duration(next_chunk)

            im = self.is_immediately(ctime, next_chunk_duration)

            # ad
            playlist.append({
                'time': str(self.seconds_to_time(ctime)),
                'params': self.get_params_list(next_chunk)})

            # if im:
            #     # immediately
            #     playlist.append({
            #         'time': str(im['time']),
            #         'params': im['params']})
            #     ctime += im['offset']
            # else:
            ctime += next_chunk_duration

        return playlist