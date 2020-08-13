import math

def decimalToBinary(n, bits):  
    shortened = bin(n).replace("0b", "") 
    return "0"*(bits-len(shortened)) + shortened

# print(decimalToBinary(8, 8))

def generateBinaryStrings(k):
    upto = int(math.pow(2, k))
    for i in range(0, upto):
        print(decimalToBinary(i, k))

generateBinaryStrings(9)