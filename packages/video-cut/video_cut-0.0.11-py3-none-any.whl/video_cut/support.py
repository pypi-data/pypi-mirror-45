import random
import subprocess
import os.path


def get_video_duration(input_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return float(data)
    except:
        return 0

def get_audio_duration(input_path):
    cmd = f"ffprobe -v error -select_streams a:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return float(data)
    except:
        return 0


def get_video_codec(input_path):
    cmd = f"ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return data
    except:
        return 'libx264'

def get_audio_codec(input_path):
    cmd = f"ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 {input_path}"
    data = subprocess_call([x.strip() for x in cmd.split(' ') if x.strip()])
    data = [x for x in data.split('\n') if x.strip()][0].strip()
    try:
        return data
    except:
        return 'aac'

        
class FfmpegError(Exception):
    def __init__(self, message, stdout=''):

        # Call the base class constructor with the parameters it needs
        super().__init__(f'{message}\n{stdout}\n')

        # Now for your custom code...
        self.stdout = stdout

def subprocess_call(cmd, verbose=True, errorprint=True):
    """ Executes the given subprocess command."""

    popen_params = {"stdout": subprocess.PIPE,
                    "stderr": subprocess.PIPE,
                    "stdin": subprocess.DEVNULL}
    # pretty_cmd = ' '.join(cmd)
    # print(f'executing {pretty_cmd}')
    proc = subprocess.Popen(cmd, **popen_params)

    out, err = proc.communicate()
    # print(out)
    # proc.stderr.close()

    if proc.returncode:
        raise FfmpegError(err.decode('utf8'), out.decode('utf8'), )

    del proc
    return out.decode('utf8')


class temporary_write:
        def __init__(self,  data, path=str(random.random())[3:]):
                self.path = os.path.abspath(path)
                self.data = data
                f = open(self.path, 'w')
                f.write(self.data)
                f.close()

        __enter__ = lambda self: self.path
        __exit__ = lambda self, a, b, c: os.remove(self.path)

def name_and_ext(path):
    path, ext = os.path.splitext(path)
    name = os.path.basename(path)
    return name, ext
