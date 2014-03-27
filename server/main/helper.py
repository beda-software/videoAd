import json
import datetime

__author__ = 'lkot'


class Generator(object):
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

    def get_time_table(self):
        """
        Generate timetable
        """

        day = self.day

        playlist = []

        # video
        state_video = {'time': '', 'action': [
                           {'action': 'start_video'},]}

        # text
        state_text = {'time': '', 'action': [
                           {'action': 'start_text'},]}

        # immediately template
        immediately_tpl = {'time': '',
                           'action': [
                               {'action': 'immediately_start', 'params': ''},]},

        time_for_video = day.time_for_video
        time_for_text  = day.time_for_text

        start_time = day.start_time
        stop_time = day.stop_time

        if day.show_text:
            state_video['action'].append({'action': 'start_text'})

        if day.show_video:
            state_text['action'].append({'action': 'start_video'})

        # current time in second
        ctime_s = self.time_to_seconds(start_time)

        # stop time in second
        stime_s = self.time_to_seconds(stop_time)

        time_video_s = self.time_to_seconds(time_for_video)
        time_text_s = self.time_to_seconds(time_for_text)

        immediatelies = day.immediatelies.all()

        # time loop
        while ctime_s < stime_s:
            sv, st = state_video.copy(), state_text.copy()

            # video block
            sv['time'] = str(self.seconds_to_time(ctime_s))
            ctime_s += time_video_s

            playlist.append(sv)

            # text block
            st['time'] = str(self.seconds_to_time(ctime_s))
            ctime_s += time_text_s

            playlist.append(st)

        return playlist

    def get_filelist(self):
        pass

    def run(self):
        """
        Base method, run generate playlist
        """
        playlist = {
            'time_table': self.get_time_table(),
            'filelist': self.get_filelist()}

        return json.dumps(playlist)