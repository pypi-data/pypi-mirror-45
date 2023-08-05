import os.path
from .support import subprocess_call
from .align_audio_video import align_audio_video
from .support import name_and_ext, temporary_write, get_video_codec, get_audio_codec




def cut_video(in_path, out_path, start, end, encode=False, acodec=None, vcodec=None,):
    name, ext = name_and_ext(out_path)
    if end - start > 4 and not encode:
        with temporary_write('', path=f'disaligned_temporary_{name}{ext}') as temp_path:
            cmd = [
              "ffmpeg","-y",
              "-i", in_path,
              "-ss", "%0.3f" % start,
              "-to", "%0.3f" % end,
              "-map","0",
              "-c", "copy",
              "-shortest",
              # "-avoid_negative_ts", "1",
              temp_path
            ]
            subprocess_call(cmd)
            out_path = align_audio_video(temp_path, out_path)
            return out_path
    else:
        vcodec = vcodec or get_video_codec(in_path)
        acodec = acodec or get_audio_codec(in_path)
        cmd = [
          "ffmpeg","-y",
          "-i", in_path,
          "-ss", "%0.3f" % start,
          "-to", "%0.3f" % end,
          "-map","0",
          "-c:v", vcodec,
          "-c:a", acodec,
          "-shortest",
          "-crf", "18",
          # "-avoid_negative_ts", "1",
          out_path
        ]
        subprocess_call(cmd)
        return out_path
