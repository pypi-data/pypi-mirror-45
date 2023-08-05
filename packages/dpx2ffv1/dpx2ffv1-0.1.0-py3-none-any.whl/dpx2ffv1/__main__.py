#!/usr/bin/env python3
import sys, os, fnmatch,  getopt
from dpx2ffv1.dpx2ffv1 import dpx2ffv1, usage, print_error

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hop:v", ["help", "output=", "input="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print_error(err)  # will print something like "option -a not recognized"
    output = None
    input = None
    verbose = False
    fps = 24

    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
            print("output is %s " % output)
        elif o in ("-i", "--input"):
            input = a
            print("path is %s " % input)
            if(os.path.isdir(input) == False):
                print_error("The input path is not a directory")
        else:
            assert False, "unhandled option"
    
    if input is None:
        print_error("No input was given")
    if output is None:
        print_error("No Output was given")
    return dpx2ffv1(input, output, fps)


if __name__ == "__main__":
    main()
