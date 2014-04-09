from celery.decorators import task
from helper import PlaylistGenerator
import shlex
import subprocess
from os import path
from filebrowser.base import FileObject


@task
def create_playlist_task(day):
    g = PlaylistGenerator(day=day)
    g.run()


@task
def compress_video_task(video):
    from models import OsCommandLog
    from models import create_update_day

    ext, file_path = video.file_video.extension, video.file_video.path_full

    if '_compress' in file_path:
        return

    out = ''.join(file_path.split('.')[:-1] + ['_compress%s' % ext])
    command = 'ffmpeg -i %s -s 320x240 %s -loglevel error -y' % (file_path, out)

    process = subprocess.Popen(shlex.split(str(command)), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    output, errors = process.communicate()
    returncode = process.poll()

    if path.exists(out):
        video.file_video = FileObject(out)
        video.save()

    # log
    OsCommandLog.objects.create(command=command, ouput=output, errors=errors, return_code=returncode)

    # create or update days for video
    for day in video.days:
        create_update_day(None, day, action='post_add')
