# in this analysis we just see what symbols and how many of them in cipher text
file_in = open('cipher.txt',mode = 'r',encoding='UTF-8')
data = file_in.read() 

# examples
# dic['b'] = 10 that mean in cipher text we have 10 symbol 'b'
dic = {}
for i in range(len(data)):
    if i == data.find(data[i]): # if ith character appears the 1st time on cipher text
        dic[data[i]] = 0
    dic[data[i]] += 1
keys = dic.keys()

print('number of characters in data: %d' %(len(keys)))
for item in dic.items():
    print(item)