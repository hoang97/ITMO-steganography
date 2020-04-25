LSB-Steganography

Requirement:

- python3
- modul OpenCV: py -m pip install -U opencv-python
- modul numpy: py -m pip install -U numpy
- modul pyplot: py -m pip install -U matplotlib

Usage:

usage: LSB.py [-h] [-i ifile] -ii inimg [-o ofile] opts

positional arguments:
  opts        name of option (hide/unhide/analysis)

optional arguments:
  -h, --help  show this help message and exit
  -i ifile    name of input text file
  -ii inimg   name of input image file
  -o ofile    name of output file
 
 Example:
 
 - to hide message in file (in_text.txt) to image (testin.bmp) then ouput to image (testout.bmp)
 
   py LSB.py hide -i in_text.txt -ii testin.bmp -o testout.bmp
   
 - to unhide message in image (testout.bmp) then output to file (out_text.txt)
 
   py LSB.py unhide -ii testout.bmp -o out_text.txt
   
 - to get graphic analysis image (testin.bmp) with message (in_text.txt)
 
   py LSB.py analysis -i in_text.txt -ii testin.bmp
   
 NOTE:
 
 - message in text file must have ASCII order <= 255 (can't contain RUS characters)
 - message in analysis text file must have at least 50 words
 
