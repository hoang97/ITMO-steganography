dic = {}
# in ACSII table russian alphabet 'a' = 1072 .... 'я' = 1104
# create a dictionary for 'transform string text to binary'
for i in range(1072,1104):
    dic[chr(i)] = '{0:05b}'.format(i-1072) 
    # example 
    # dic['a'] = '00000'
    # dic['б'] = '00001'
    # .........

# transform string text to binary
def transform(text):
    binary = ''
    for i in range(len(text)):
        binary = binary + dic[text[i]]
    return binary
# transform binary to string text
def reverse(text):
    res = ''
    for i in range(len(text)//5):
        a = text[i*5:(i+1)*5] # every symbol using a 5bit-encode
        b = int(a,2)
        res += chr(b+1072)
    return res
# encoding text to container (data) using (law)
# by that changing symbol law[0][0] -> law[0][1] to encode bit 0
#                         law[1][0] -> law[1][1] to encode bit 1
def encode(text,data,law):
    binary = list(transform(text))
    data = list(data)
    index = -1
    for i in range(len(binary)):
        if binary[i] == '0':
            index = data.index(law[0][0],index+1) # find index of symbol law[0][0] in container
            data[index] = law[0][1]                 # from the last 'index' to the end of container
        elif binary[i] == '1':
            index = data.index(law[1][0],index+1) # find index of symbol law[1][0] in container
            data[index] = law[1][1]                 # from the last 'index' to the end of container
    return ''.join(data) # result the cipher text (container after changing)
# decoding data (cipher text) using (law)
# by that finding symbol law[0][1] to add bit 0
#                        law[1][1] to add bit 1
def decode(data,law):
    res = ''
    index = -1
    while True:
        index1 = data.find(law[0][1],index+1)
        index2 = data.find(law[1][1],index+1)
        if (index1 == -1) and (index2 == -1): break
        if ((index1 < index2) and (index1 != -1))or(index2 == -1):
            index = index1
            res += '0'  # add bit 0 to result
        elif index2 != -1:
            index = index2
            res += '1'  # add bit 1 to result
    return reverse(res)
# ---------------------------------main programme--------------------------#
file_in = open('container.txt',mode = 'r',encoding='UTF-8')
file_out = open('cipher.txt',mode = 'w',encoding='UTF-8')
data = file_in.read() # read data from container

x = int(input('введите метод\n1.прямой замены символов\n2.исползование доп. пробелов\n3.добавление слуб. символов\n'))
text = input('введите текст\n') # input the text, that we must encode to container

law = {}
if x == 1:
    law[0] = ('o',chr(1086))  # char(1086) = symbol 'o' in russian
    law[1] = ('p',chr(1088))  # char(1088) = symbol 'p' in russian
elif x == 2: 
    law[0] = ('\n',' \n')     # we add 1 spacebar right before endline
    law[1] = ('\n','\t\n')    # we add 1 tab right before endline
elif x == 3:
    law[0] = ('\n',chr(160)+'\n')  # we add a special character (that don't show when we open document)
    law[1] = ('\n',chr(127)+'\n')
cipher_text = encode(text,data,law)

file_out.write(cipher_text)
file_in.close()
file_out.close()

file_in = open('cipher.txt',mode = 'r',encoding='UTF-8')
data = file_in.read()
print('decode:')
print(decode(data,law))



