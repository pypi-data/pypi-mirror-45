[![Build Status](https://travis-ci.com/DerouineauNicolas/dpx_to_ffv1.svg?branch=master)](https://travis-ci.com/DerouineauNicolas/dpx_to_ffv1)
[![PyPI version](https://badge.fury.io/py/dpx2ffv1.svg)](https://badge.fury.io/py/dpx2ffv1)

dpx2ffv1
===================

This program takes a folder filled with dpx indexed images as an input and encode them as a unique ffv1/mkv binary.
The program detects if the indexed image have an offset and a prefix (see test folder for an example)

Requirements
-------------------

ffmpeg binary should be available on your system.

Install (System wide)
-------------------

python3 setup.py install



Run 
-------------------

python3 -m dpx2ffv1 --input=./testdpx/ --output=ffv1out.mkv

or

dpx2ffv1 --input=./testdpx/ --output=ffv1out.mkv

Generate Dist and upload 
-------------------

python3 setup.py sdist bdist_wheel

python3.7 -m twine upload dist/*
