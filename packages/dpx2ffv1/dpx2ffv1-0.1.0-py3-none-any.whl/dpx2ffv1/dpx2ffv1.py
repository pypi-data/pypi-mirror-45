from dpx2ffv1.fileutils import parse_directory 
from dpx2ffv1.encode import is_ffmpeg_available, encode_dpx_scans 
import sys

def usage():
    print("dpx2ffv1 is a simple module to convert a set of dpx to ffv1 codec")
    print("Expected usage:")
    print("python3 -m dpx2ffv1 --input=./test/ --output=ffv1out.mkv ")

def print_error(error_message):
    print(error_message)
    usage()
    sys.exit()

def dpx2ffv1(input, output, fps):
    num_scan, offset, num_decimal, prefix = parse_directory(input)

    if(is_ffmpeg_available()==True):
        try:
            ret = encode_dpx_scans(input, output, num_scan, offset, fps, num_decimal, prefix)
            if ret < 0:
                print("Something went wrong")
                sys.exit(-1)
            else:
                print("Encoding is finished")
                #sys.exit(0)
                return 0
        except Exception:
            print("Something went wrong")
            sys.exit(-1)
    else:
        print_error("ffmpeg is not installed")