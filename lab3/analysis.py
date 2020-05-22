from cv2 import cv2
import numpy as np
class PSNRException(Exception):
    pass
class Analysis():
    def __init__(self,originImg,Img):
        self.origin = originImg
        self.changed = Img

        orirow,oricol = originImg.shape[:2]
        # Padding some pixel to make row and col divisible by 8
        if orirow % 8 != 0 or oricol %8 != 0:
            newRow = orirow+8-orirow%8
            newCol = oricol+8-oricol%8
            self.origin = cv2.resize(originImg,(newCol,newRow))

        self.oheight, self.owidth, self.ochannel = self.origin.shape
        self.osize = self.oheight * self.owidth * self.ochannel

        self.cheight, self.cwidth, self.cchannel = Img.shape
        self.csize = self.cheight * self.cwidth * self.ochannel

        self.MAXi = 255 # maximum posible channel value of the image = 2^8-1
        self.maskONE = 0b00000001 # use bitwise OR to make LSB 1

    def MSE(self): # calculate MSE = 1/size * sum((I(i,j)-K(i,j))^2) with i = 1..n;j = 1..m
        mse = np.mean((self.origin - self.changed)**2)
        return mse
    def PSNR(self): # calculate PSNR = 10*log10(MAXi^2/MSE)
        mse = np.mean((self.origin - self.changed)**2)
        res = self.MAXi**2/mse
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