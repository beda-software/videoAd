# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import datetime
import shlex
import subprocess
from multiprocessing import ProcessError
from os import path, mkdir, symlink, unlink
from shutil import rmtree
from videoad import settings
from utils import Generator

__author__ = 'lkot'


class PlaylistGenerator(object):
    def __init__(self, day=None):
        self.root_dir = path.join(settings.MEDIA_ROOT, 'terminals')
        self.day = day

        if day:
            self.terminal_pk = self.day.terminal.pk
            self.date = str(self.day.date)
            self.date_path = self.get_date_path(self.terminal_pk, self.date)
            self.terminal_path = self.get_terminal_path(self.terminal_pk)

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
        if ad.__class__.__name__ == 'VideoAd':
            return {'video': ad.file_video.filename}
        elif ad.__class__.__name__ == 'TextAd':
            return {'text': ad.text}
        elif ad.__class__.__name__ == 'ImageAd':
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
        videoal = list(self.day.video_ad.all()) + list(self.day.image_ad.all())
        textal = list(self.day.text_ad.all())

        video_ad_list = Generator(videoal)
        text_ad_list = Generator(textal)

        chunk_len = self.day.video_count
        chunk_len_txt = self.day.text_count

        block, playlist = {}, []

        ctime = self.time_to_seconds(self.day.start_time)
        while ctime < self.time_to_seconds(self.day.stop_time):
            next_chunk = videoal if chunk_len == 0 else video_ad_list[:chunk_len]
            next_chunk_text = textal if chunk_len_txt == 0 else text_ad_list[:chunk_len_txt]

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

            # Infinity loop
            if not nxd:
                return playlist

        return playlist

    def generate_fs(self, filelist, playlist):
        if not self.day:
            raise Exception("Day undefined")

        self.mkdir_base()
        self.mkdir_terminal(self.terminal_pk)
        self.mkdir_date(self.terminal_pk, self.date)
        self.create_playlist(self.date_path, playlist)
        self.create_symlinks(filelist, self.date_path)

    def create_symlinks(self, filelist, dst):
        for fo in filelist:
            self.link_to_file(fo.path_full, path.join(dst, fo.filename))

    def create_playlist(self, dst, playlist):
        pl = open(path.join(dst, 'playlist.json'), 'w+')
        pl.write(json.dumps(playlist))
        pl.close()

    def mkdir_base(self):
        if not path.exists(self.root_dir):
            mkdir(self.root_dir)

    def get_terminal_path(self, tpk):
        return path.join(self.root_dir, str(tpk))

    def get_date_path(self, tpk, date):
        return path.join(self.get_terminal_path(tpk), date)

    def mkdir_terminal(self, tpk):
        if not path.exists(self.get_terminal_path(tpk)):
            mkdir(self.get_terminal_path(tpk))

    def rmdir_terminal(self, tpk):
        if path.exists(self.get_terminal_path(tpk)):
            rmtree(self.get_terminal_path(tpk))

    def mkdir_date(self, tpk, date):
        if not path.exists(self.get_date_path(tpk, date)):
            mkdir(self.get_date_path(tpk, date))

    def rmdir_date(self, tpk, date):
        if path.exists(self.get_date_path(tpk, date)):
            rmtree(self.get_date_path(tpk, date))

    def link_to_file(self, src, dst):
        if path.exists(src) and not path.exists(dst):
            symlink(src, dst)

    def get_file_object(self, obj):
        fields = {'ImageAd': 'image',
                  'VideoAd': 'file_video'}

        return getattr(obj, fields[obj.__class__.__name__])

    def get_filelist(self):
        ad_list = list(self.day.image_ad.all())+list(self.day.video_ad.all())
        return map(self.get_file_object, ad_list)

    def run(self):
        playlist = self.get_play_list()
        filelist = self.get_filelist()
        self.generate_fs(filelist, playlist)
