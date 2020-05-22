from LSB_DCT import *
from analysis import *
import argparse

# config command line arguments
parse = argparse.ArgumentParser(description= "DBH lab3 staganography")
parse.add_argument('-i',metavar='ifile',type=str,dest= "in_text",help= "name of input text file")
parse.add_argument('-ii',metavar='inimg',type=str,dest= "in_img",help= "name of input image file",required= True)
parse.add_argument('-o',metavar='ofile',type=str,dest= "out_file",help= "name of output image/text file")
parse.add_argument('option',metavar='opts',type=str,help= "name of option (embed/extract/PSNR/detection)")
args = parse.parse_args()

# embed text data to image with LSB-DCT method
if args.option == "embed":
    # read text to embed
    text = open(args.in_text,"r",encoding="UTF-8").read()
    # get data and run LSB-DCT stegano
    data_in = cv2.imread(args.in_img)
    steg = LSB_DCT_steg(data_in)
    data_out = steg.embed(text)
    # write image's data to file
    cv2.imwrite(args.out_file,data_out)
# extract text data from image by LSB-DCT method
elif args.option == "extract":
    # get data and run inverse LSB-DCT stegano
    data_in = cv2.imread(args.in_img)
    steg = LSB_DCT_steg(data_in)
    text = steg.extract()
    # write extracted text to file
    open(args.out_file,"w",encoding="UTF-8").write(text)
# calculate PSNR of 2 image
elif args.option == "PSNR":
    # get 2 input images's data and run PSNR
    data1 = cv2.imread(args.in_img)
    data2 = cv2.imread(args.out_file)
    analize = Analysis(data1,data2)
    PSNR = analize.PSNR()
    # show PSNR
    print("PSNR of your 2 images is:",end = " ")
    print(PSNR)
# draw PSNR graphic with image embed by 1,2,.... symbols
elif args.option == "graph":
    # read input text
    text = open(args.in_text,"r",encoding="UTF-8").read()
    # get input images's data
    data_in = cv2.imread(args.in_img)
    # data_out = cv2.imread(args.out_file)
    in_text = ""
    PSNRs = []
    numWords = []
    for i in range(len(text)):
        in_text += text[i]
        print(in_text)
        steg = LSB_DCT_steg(data_in) # init LSB-DCT method
        data_out = steg.embed(in_text)
        data_in = cv2.imread(args.in_img)
        analize = Analysis(data_in,data_out)
        # save output data to array
        numWords.append(i)
        PSNR = analize.PSNR()
        PSNRs.append(PSNR)
    # draw PSNR graphic
    import matplotlib.pyplot as plt
    plt.plot(numWords,PSNRs)
    plt.xlabel("Number of words hided in image")
    plt.ylabel("PSNR value in Db")
    plt.title("Graphic PSNR with Number of words ratio")
    plt.show()
# run a simple attack to LSB-DCT method
elif args.option == "detection":
    # get input images's data
    data_in = cv2.imread(args.in_img)
    steg = LSB_DCT_steg(data_in)
    steg.statistic()