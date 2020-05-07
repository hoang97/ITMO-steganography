import cv2
import numpy as np
class SteganoException(Exception):
    pass
class LSBSteg():
    def __init__(self,img):
        self.image = img
        self.mheight, self.mwidth, self.mchannel = img.shape
        self.size = self.mheight * self.mwidth

        self.maskONE = 0b00000001 # use bitwise OR to make LSB 1
        self.maskZERO = 0b11111110 # use bitwise AND to make LSB 0

        self.curwidth = 0
        self.curheight = 0
        self.curchan = 0
    
    def binary_value(self,val,bitsize):
        binval = bin(val)[2:]
        if len(binval) > bitsize:
            raise SteganoException("your text contain unexpected character")
        while len(binval) < bitsize:
            binval = '0' + binval
        return binval

    def hide_binary_value(self,binVal):
        for c in binVal:
            val = list(self.image[self.curheight,self.curwidth]) # get pixel information in list format
            if int(c) == 1:
                val[self.curchan] = int(val[self.curchan]) | self.maskONE # OR with maskONE to make LSB = 1
            else:
                val[self.curchan] = int(val[self.curchan]) & self.maskZERO # AND with maskZERO to make LSB = 0

            self.image[self.curheight,self.curwidth] = tuple(val) # save change to image
            self.next_slot() # move to next space of image to hide

    def next_slot(self):
        if self.curchan == self.mchannel - 1:
            self.curchan = 0
            if self.curwidth == self.mwidth - 1:
                self.curwidth = 0
                if self.curheight == self.mheight - 1:
                    raise SteganoException("Can't hide/unhide image !!!!")
                else: self.curheight += 1
            else: self.curwidth += 1
        else: self.curchan += 1
    
    def read_bit(self): # read a single bit in the image
        val = self.image[self.curheight,self.curwidth][self.curchan] # get value from 1 channel of 1 pixel in image
        val = int(val) & self.maskONE # AND with maskONE
        self.next_slot()
        if val > 0: 
            return '1'
        else: 
            return '0'

    def read_bits(self,bitsize): # read a fixed (bitsize) bits in the image
        res = ""
        for _ in range(bitsize):
            res += self.read_bit()
        return res

    def hide_text(self, txt):
        l = len(txt)
        binl = self.binary_value(l,16) # set the length of text up to 16 bits (text size up to 65536 bits long)
        self.hide_binary_value(binl) # hide the length of text in image
        for ch in txt: # hide all the chars of text in image
            c = ord(ch)
            self.hide_binary_value(self.binary_value(c,8))
        return self.image
    def unhide_text(self):
        binl = self.read_bits(16) # get the length of text in binary format
        l = int(binl,2) # length of text in integer format
        text = ""
        for _ in range(l):
            tmp = self.read_bits(8) # read 8 bits = 1 char
            text += chr(int(tmp,2))
        return text

class PSNRException(Exception):
    pass
class Analysis():
    def __init__(self,originImg,Img):
        self.origin = originImg
        self.changed = Img

        self.oheight, self.owidth, self.ochannel = originImg.shape
        self.osize = self.oheight * self.owidth * self.ochannel

        self.cheight, self.cwidth, self.cchannel = Img.shape
        self.csize = self.cheight * self.cwidth * self.ochannel

        self.MAXi = 255 # maximum posible channel value of the image = 2^8-1
        self.maskONE = 0b00000001 # use bitwise OR to make LSB 1

    def MSE(self): # calculate MSE = 1/size * sum((I(i,j)-K(i,j))^2) with i = 1..n;j = 1..m
        res = 0
        if self.oheight != self.cheight: raise PSNRException("2 images not at same size")
        if self.owidth != self.cwidth: raise PSNRException("2 images not at same size")
        if self.ochannel != self.cchannel: raise PSNRException("2 images not at same size")

        for curheight in range(self.oheight):
            for curwidth in range(self.owidth):
                for curchan in range(self.ochannel):
                    I = int(self.origin[curheight,curwidth][curchan])
                    K = int(self.changed[curheight,curwidth][curchan])
                    res += (I-K)*(I-K)

        res *= 1/self.osize
        return res
    def PSNR(self): # calculate PSNR = 10*log10(MAXi^2/MSE)
        res = self.MAXi*self.MAXi/self.MSE() 
        res = 10 * np.log(res) / np.log(10)
        return res
    def Detec(self):
        for curheight in range(self.oheight):
            for curwidth in range(self.owidth):
                for curchan in range(self.ochannel):
                    I = int(self.origin[curheight,curwidth][curchan])
                    K = int(self.changed[curheight,curwidth][curchan]) 
                    self.origin[curheight,curwidth][curchan] = (I & self.maskONE) * 255
                    self.changed[curheight,curwidth][curchan] = (K & self.maskONE) * 255
        cv2.imwrite('tmp1.bmp',self.origin)
        cv2.imwrite('tmp2.bmp',self.changed)

class AnalysisException(Exception):
    pass

import argparse

parse = argparse.ArgumentParser(description= "DBH lab2 staganography")
parse.add_argument('-i',metavar='ifile',type=str,dest= "in_file",help= "name of input text file")
parse.add_argument('-ii',metavar='inimg',type=str,dest= "in_img",help= "name of input image file",required= True)
parse.add_argument('-o',metavar='ofile',type=str,dest= "out_file",help= "name of output file")
parse.add_argument('option',metavar='opts',type=str,help= "name of option (hide/unhide/analysis)")
args = parse.parse_args()

in_img = cv2.imread(args.in_img)
steg = LSBSteg(in_img)

if args.option == "hide":
    data = open(args.in_file,"r",encoding= 'UTF-8').read()
    res = steg.hide_text(data)
    out_img = args.out_file
    cv2.imwrite(out_img,res)
    print("Hiding process complete !!!")
elif args.option == "unhide":
    res = steg.unhide_text()
    out_file = args.out_file
    with open(out_file,'w',encoding= "UTF-8") as f:
        f.write(res)
    print("Unhiding process complete !!!\nYou can see result in out_text.txt")
elif args.option == "analysis":
    data = open(args.in_file,"r",encoding= "UTF-8").read()
    if len(data) < 50: raise AnalysisException("Your input has less than 50 symbols !!!")
    input = ""
    PSNRs = []
    numWords = []
    for i in range(0,len(data),5):
        input += data[i:i+5] # append 1 symbols to input

        stega = LSBSteg(in_img) # init LSB changing method

        changed_img = stega.hide_text(input) # get value of changed image
        in_img = cv2.imread(args.in_img) # refresh value in variable "in_img" (value of orginal img)

        res = Analysis(in_img,changed_img)

        PSNRs.append(res.PSNR())
        numWords.append(i)
    # print("Analysis complete !!!")
    # print(PSNRs)
    import matplotlib.pyplot as plt
    plt.plot(numWords,PSNRs)
    plt.xlabel("Number of words hided in image")
    plt.ylabel("PSNR value in Db")
    plt.title("Graphic PSNR with Number of words ratio")
    plt.show()
elif args.option == "detection":
    in_img = cv2.imread(args.in_img)
    changed_img = cv2.imread(args.out_file)
    res = Analysis(in_img,changed_img)
    res.Detec()