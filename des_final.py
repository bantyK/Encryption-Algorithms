import binascii
#Permutation table : used to convert the 64-bit key into 56-bit
PCtable = (57, 49, 41, 33, 25, 17, 9,
           1, 58, 50, 42, 34, 26, 18,
           10, 2, 59, 51, 43, 35, 27,
           19, 11, 3, 60, 52, 44, 36,
           63, 55, 47, 39, 31, 23, 15,
           7, 62, 54, 46, 38, 30, 22,
           14, 6, 1, 53, 45, 37, 29,
           21, 13, 5, 28, 20, 12, 4)

#Second permutation table : used to convert the 56-bit key into 48-bit
PC2table = (14, 17, 11, 24,  1, 5,
             3, 28, 15,  6, 21,10,
            23, 19, 12,  4, 26, 8,
            16,  7, 27, 20, 13, 2,
            41, 52, 31, 37, 47,55,
            30, 40, 51, 45, 33,48,
            44, 49, 39, 56, 34,53,
            46, 42, 50, 36, 29,32)

#Initial Permutation table : used for intial permutation of the plain text
IPtable = (58, 50, 42, 34, 26, 18, 10, 2,
           60, 52, 44, 36, 28, 20, 12, 4,
           62, 54, 46, 38, 30, 22, 14, 6,
           64, 56, 48, 40, 32, 24, 16, 8,
           57, 49, 41, 33, 25, 17, 9, 1,
           59, 51, 43, 35, 27, 19, 11, 3,
           61, 53, 45, 37, 29, 21, 13, 5,
           63, 55, 47, 39, 31, 23, 15, 7)

#Expansion table : used to expand the plain text from 32-bit to 48-bit
EPtable = (32, 1, 2, 3, 4, 5,
           4, 5, 6, 7, 8, 9,
           8, 9, 10, 11, 12, 13,
           12, 13, 14, 15, 16, 17,
           16, 17, 18, 19, 20, 21,
           20, 21, 22, 23, 24, 25,
           24, 25, 26, 27, 28, 29,
           28, 29, 30, 31, 32, 1)

#Permutation table
PFtable = (16, 7, 20, 21, 29, 12, 28, 17,
           1, 15, 23, 26, 5, 18, 31, 10,
           2, 8, 24, 14, 32, 27, 3, 9,
           19, 13, 30, 6, 22, 11, 4, 25)

#Inverse Permutation table : used in the final stage of encryption
FPtable = (40, 8, 48, 16, 56, 24, 64, 32,
           39, 7, 47, 15, 55, 23, 63, 31,
           38, 6, 46, 14, 54, 22, 62, 30,
           37, 5, 45, 13, 53, 21, 61, 29,
           36, 4, 44, 12, 52, 20, 60, 28,
           35, 3, 43, 11, 51, 19, 59, 27,
           34, 2, 42, 10, 50, 18, 58, 26,
           33, 1, 41,  9, 49, 17, 57, 25)

#defining the s-boxex:
sBox = 8 * [64 * [0]]  # a 2-d array where each row has 64 places and there are 8 rows
sBox[0] = ( (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7),
           (0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8),
           (4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0),
           (15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13))

sBox[1] = ( (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10),
           (3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5),
           (0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15),
           (13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9))

sBox[2] = ( (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8),
           (13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1),
           (13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7),
           (1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12))

sBox[3] = ( (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15),
            (13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9),
            (10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4),
            (3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14))

sBox[4] = ( (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9),
            (14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6),
            (4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14),
            (11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3))

sBox[5] = ( (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11),
           (10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8),
           (9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6),
           (4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13))

sBox[6] = ( (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1),
            (13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6),
            (1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2),
            (6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12))

sBox[7] = ((13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7),
           (1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2),
           (7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8),
           (2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11))
#----------------------------------------------------------------
def hex_to_binary(plain_text):
  binary_text = "{0:064b}".format(int(plain_text,16))
  return binary_text
#----------------------------------------------------------------
def permutation(text,table):
  permuted_key = []
  for index in table:
      permuted_key.append(text[index-1])

  return ''.join(str(i) for i in permuted_key)
#----------------------------------------------------------------
def leftShift(inKeyBitList,round):
  #number of left shifts in 16 iteration
  left_shift_table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]  
  outKeyBitList = 56*[0]
  if(left_shift_table[round] == 2):
    outKeyBitList[:26] = inKeyBitList[2:28]
    outKeyBitList[26] = inKeyBitList[0]
    outKeyBitList[27] = inKeyBitList[1]
    outKeyBitList[28:54] = inKeyBitList[30:]
    outKeyBitList[54] = inKeyBitList[28]
    outKeyBitList[55] = inKeyBitList[29]
  else:
    outKeyBitList[:27] = inKeyBitList[1:28]
    outKeyBitList[27] = inKeyBitList[0]
    outKeyBitList[28:55] = inKeyBitList[29:]
    outKeyBitList[55] = inKeyBitList[28]

  return("".join(outKeyBitList))
#----------------------------------------------------------------
def XOR(text,key): return '{0:048b}'.format(int(text,2) ^ int(key,2))
#----------------------------------------------------------------
def XOR_32(text,key): return '{0:032b}'.format(int(text,2) ^ int(key,2))
#----------------------------------------------------------------
def substitution(xored_text):
  ''' This function choose give the excrypted text from one of the s-boxes'''
  encrypted_text = []
  i,j=0,0
  while(i < 48):
    block = ''
    block = xored_text[i:i+6]
    row = int(block[0]+block[5],2)
    column = int(block[1:5],2)
    encrypted_text.append('{0:04b}'.format(sBox[j][row][column]))
    i+=6
    j+=1
  return (''.join([i for i in encrypted_text]))
#----------------------------------------------------------------
def DES(plain_text,key):
  plain_text = plain_text.replace(' ','')
  key = key.replace(' ','')
  key_56 = permutation(key,PCtable) # OK
  key_set,key_set1 = [],[] # the array to hold the 16 keys
  for round in range(0,16):
    shifted_key = leftShift(key_56,round)
    key_set.append(shifted_key) #OK
    key_56 = shifted_key

  for round in range(16):
    key_set1.append(permutation(key_set[round],PC2table))

  initial_permuted_data = permutation(plain_text,IPtable)
  left = initial_permuted_data[:32]
  right = initial_permuted_data[32:]
  for i in range(16):
    new_left = right
    expanded_right_part = permutation(right,EPtable)
    xored_right_with_key = XOR(expanded_right_part,key_set1[i])
    substituted_text = substitution(xored_right_with_key)
    permuted_xored_text = permutation(substituted_text,PFtable)
    new_right = XOR_32(left,permuted_xored_text)
    left = new_left
    right = new_right

  cipher_text = new_right + new_left #right and left part are reversed
  final_cipher_text = permutation(cipher_text,FPtable)
  return (final_cipher_text)
#----------------------------------------------------------------
def main():
  plain_text = str(input("Enter the text to encode : "))
  key = str(input("Enter the key : "))
  cipher_text = DES(hex_to_binary(plain_text),hex_to_binary(key))
  print ("Plain  Text : ",plain_text)
  print ("Cipher Text : ","{0:0>X}".format(int(cipher_text,2)))


if __name__ == "__main__":
  main()