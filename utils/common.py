import whisper
import ffmpeg
import numpy as np
import traceback
from datetime import timedelta



def transcribe_file(filepath: str, model_type="base", out="default"):

    #model_type = 'base'
    model = whisper.load_model(model_type)

    result = model.transcribe(filepath)
    if out == "default":
        # ----
        ret = ""
        for seg in result['segments']:
            td_s = timedelta(milliseconds=seg["start"] * 1000)
            td_e = timedelta(milliseconds=seg["end"] * 1000)

            t_s = f'{td_s.seconds // 3600:02}:{(td_s.seconds // 60) % 60:02}:{td_s.seconds % 60:02}.{td_s.microseconds // 1000:03}'
            t_e = f'{td_e.seconds // 3600:02}:{(td_e.seconds // 60) % 60:02}:{td_e.seconds % 60:02}.{td_e.microseconds // 1000:03}'

            ret += '{}\n{} --> {}\n{}\n\n'.format(seg["id"], t_s, t_e, seg["text"])
        ret += '\n'
        return {"text": ret}
        # -----
    elif out == "text":
        return {"text": result['text']}
    else:
        return {"text": result['text']}