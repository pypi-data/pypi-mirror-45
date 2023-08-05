
import subprocess, sys
import time

def is_ffmpeg_available():
    """Check whether `name` is on PATH and marked as executable."""

    # from whichcraft import which
    from shutil import which

    return which("ffmpeg") is not None


def encode_dpx_scans(path, output, num_scan, offset, fps, num_decimal, prefix=''):
    print("Encoding is starting")
    print("path=%s"%path)
    print("output=%s"%output)
    print("num_scan=%s"%num_scan)
    print("offset=%s"%offset)
    print("fps=%s"%fps)
    print("num_decimal=%s"%num_decimal)
    print("prefix=%s"%prefix)
    pathinput = path + prefix + "%0" + str(num_decimal) +"d.dpx"

    cmds = ['ffmpeg', '-y', '-framerate', str(fps), '-start_number', str(offset), 
            '-i', pathinput, '-vframes', str(num_scan), '-vcodec',  'ffv1',  '-level', '3',  '-threads', '16', '-coder', '1',  '-context', '1', '-g', '1', '-slices', '24',  '-slicecrc', '1',
            '-r', str(fps), output
            ]

    print(' '.join(cmds))
    try:
        ret = subprocess.run(cmds)
        if (ret.returncode<0):
            return -1
        else:
            return 0
    except Exception:
        return -1
