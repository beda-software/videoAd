import json
import datetime
from main.models import VideoAd, TextAd, ImageAd
from os import path, mkdir, rmdir
from server.videoad import settings
from utils import Generator

__author__ = 'lkot'


class PlaylistGenerator(object):
    def __init__(self, day):
        self.root_dir = path.join(settings.MEDIA_ROOT, 'terminals')
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
        Return duration in second for chunk (video or image or text)
        chunk elements must have a prolongation `property`
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

        def get_len(im):
            """
            Return duration
            """
            return self.time_to_seconds(im.content_object.prolongation)

        def get_end(im):
            return self.time_to_seconds(im.time) + get_len(im)

        immediatelies = list(self.day.immediatelies.all())

        times_im = {}

        # Generate times_im
        for im in immediatelies:
            times_im[str(self.time_to_seconds(im.time))] = im

        for time in times_im:
            if ctime < int(time) < nxd:
                return {'time': self.seconds_to_time(int(time)),
                        'params': [self.get_params(getattr(times_im[time], 'content_object'))],
                        'end': get_end(times_im[time])}

        return False

    def get_play_list(self):
        """
        Base method, run generate playlist
        """
        video_ad_list = Generator(list(self.day.video_ad.all()) + list(self.day.image_ad.all()))
        text_ad_list = Generator(list(self.day.text_ad.all()))
        chunk_len = self.day.video_count
        chunk_len_txt = self.day.text_count
        block, playlist = {}, []

        ctime = self.time_to_seconds(self.day.start_time)
        while ctime < self.time_to_seconds(self.day.stop_time):
            next_chunk = video_ad_list[:chunk_len]
            next_chunk_text = text_ad_list[:chunk_len_txt]

            # next chunk duration
            nxd = self.get_chunk_duration(next_chunk)
            im = self.is_immediately(ctime, ctime+nxd)

            # ad
            playlist.append({
                'time': str(self.seconds_to_time(ctime)),
                'params': self.get_params_list(next_chunk+next_chunk_text)})

            if im:
                # immediately
                playlist.append({
                    'time': str(im['time']),
                    'params': im['params']})
                ctime = im['end']
            else:
                ctime += nxd

        return playlist

    def create_base_dir(self):
        if not path.exists(self.root_dir):
            mkdir(self.root_dir)

    def mkdir_terminal(self, tpk):
        if not path.exists(path.join(self.root_dir, str(tpk))):
            mkdir(path.join(self.root_dir, str(tpk)))

    def rmdir_terminal(self, tpk):
        if not path.exists(path.join(self.root_dir, str(tpk))):
            rmdir(path.join(self.root_dir, str(tpk)))

    def mkdir_date(self, tpath, date):
        if not path.exists(path.join(tpath, date)):
            mkdir(path.join(path.join(tpath, date)))

    def rmdir_date(self, tpath, date):
        if not path.exists(path.join(tpath, date)):
            rmdir(path.join(path.join(tpath, date)))
