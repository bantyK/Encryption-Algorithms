words_array = [] # arrays to hold 44 words for a 128-bit key
s_box = [['63','7C','77','7B','F2','6B','6F','C5','30','01','67','2B','FE','D7','AB','76'], 
		 ['CA','82','C9','7D','FA','59','47','F0','AD','D4','A2','AF','9C','A4','72','C0'], 
		 ['B7','FD','93','26','36','3F','F7','CC','34','A5','E5','F1','71','D8','31','15'], 
		 ['04','C7','23','C3','18','96','05','9A','07','12','80','E2','EB','27','B2','75'], 
		 ['09','83','2C','1A','1B','6E','5A','A0','52','3B','D6','B3','29','E3','2F','84'], 
		 ['53','D1','00','ED','20','FC','B1','5B','6A','CB','BE','39','4A','4C','58','CF'], 
		 ['D0','EF','AA','FB','43','4D','33','85','45','F9','02','7F','50','3C','9F','A8'], 
		 ['51','A3','40','8F','92','9D','38','F5','BC','B6','DA','21','10','FF','F3','D2'], 
		 ['CD','0C','13','EC','5F','97','44','17','C4','A7','7E','3D','64','5D','19','73'], 
		 ['60','81','4F','CD','22','2A','90','88','46','EE','B8','14','DE','5E','0B','DB'], 
		 ['E0','32','3A','0A','49','06','24','5C','C2','D3','AC','62','91','95','E4','79'], 
		 ['E7','C8','37','6D','8D','D5','4E','A9','6C','56','F4','EA','65','7A','AE','08'], 
		 ['BA','78','25','2E','1C','A6','B4','C6','E8','DD','74','1F','4B','BD','8B','8A'], 
		 ['70','3E','B5','66','48','03','F6','0E','61','35','57','B9','86','C1','1D','9E'], 
		 ['E1','F8','98','11','69','D9','8E','94','9B','1E','87','E9','CE','55','28','DF'], 
		 ['8C','A1','89','0D','BF','E6','42','68','41','99','2D','0F','B0','54','BB','16']]
constant_array = ['','01000000','02000000','04000000','08000000','10000000','20000000',
				 	 '40000000','80000000','1B000000','36000000']

state_array = [[0]*4 for i in range(4)] #intially it contains 16 zeros

def rotate(input_text):
	output_text = []
	output_text.append(input_text[2:])
	output_text.append(input_text[0:2])
	return (''.join(output_text))
#----------------------------------------------------------------------------
def substitute(input_text):
	#print (input_text)
	i = 0
	output_text = []
	while(i < len(input_text)):
		x,y = input_text[i],input_text[i+1]
		output_text.append(s_box[int(x,16)][int(y,16)])
		i+=2
	return (''.join(output_text))
#----------------------------------------------------------------------------
def XOR(text1,text2): return ("{0:0>X}".format(int(text1,16) ^ int(text2,16)))
#----------------------------------------------------------------------------
def key_generation(original_key):
	words_array.append(original_key.replace(' ','')[0:8])
	words_array.append(original_key.replace(' ','')[8:16])
	words_array.append(original_key.replace(' ','')[16:24])
	words_array.append(original_key.replace(' ','')[24:32])

	for i in range(4,44): # generate the other 40 words
		temp = words_array[i-1]

		if i%4 == 0:
			#if i is a multiple of 4 then perform roration,Subsitution and XOR with constant value
			rotated = rotate(temp)
			#print ("After Rotation : ",rotated)
			substituted = substitute(rotated)
			#print ("After Substitution : ",substituted)
			temp = XOR(substituted,constant_array[int(i/4)])
			#print ("After Constant function : ",temp)
		
		#else if i is not a multiple of 4, then simply xor the temp with words_array[i-4]
		temp = XOR(temp,words_array[i-4])
		temp = temp.rjust(8,'0') #To make all the words 16 byte long
		words_array.append(temp) #add the newly generated key into the word array
#----------------------------------------------------------------------------
def one_time_intialization(plain_text):
	k=0
	for i in range(0,4):
		for j in range(0,4):
			state_array[j][i] = plain_text[k]+plain_text[k+1]
			k+=2
			j+=1
		i+=1
	return state_array
#----------------------------------------------------------------------------
def init_permutation(state_array):
	permuted = [[0]*4 for i in range(4)]
	for i in range(len(state_array)):
		k=0
		for j in range(len(state_array[i])):
			permuted[j][i] = XOR(state_array[j][i],words_array[i][k]+words_array[i][k+1]).rjust(2,'0')
			k+=2
	return permuted
#----------------------------------------------------------------------------
def multiply_by_two(hex_number):
	'''Input -> A hex number
	   Output -> hex number multiplied by two in hexadecimal format
	'''
	binary_num = '{0:08b}'.format(int(hex_number,16))
	shifted_num = [] #variable to hold the output
	#step1 : Left Shift the number by 1
	shifted_num.append('{0:08b}'.format(int(hex_number,16))[1:])
	shifted_num.append("0")
	shifted_num = "".join(shifted_num)
	if binary_num[0]=="1":
		return XOR("{0:0>X}".format(int(shifted_num,2)),'1B')
	return "{0:0>X}".format(int(shifted_num,2))
#----------------------------------------------------------------------------
def multiply_by_three(hex_number): return (XOR(multiply_by_two(hex_number),hex_number))
#----------------------------------------------------------------------------
def substitute2(input_text):
	output_text = [[0]*4 for i in range(4)]
	for i in range(len(input_text)):
		for j in range(len(input_text[i])):
			x,y = input_text[i][j][0],input_text[i][j][1]
			output_text[i][j] = s_box[int(x,16)][int(y,16)]
	return output_text
#----------------------------------------------------------------------------
def rotate_rows(substituted,num_rotation):
	out_row = []
	for i in range(0,num_rotation):
		out_row = substituted[1:]
		out_row.append(substituted[0])
		substituted = out_row
	return substituted
#----------------------------------------------------------------------------
def mix_columns(rotated):
	mixed_array = [[0]*4 for i in range(4)]
	for j in range(0,4):
		mixed_array[0][j] = XOR(XOR(XOR(multiply_by_two(rotated[0][j]),
							multiply_by_three(rotated[1][j])),rotated[2][j]),rotated[3][j])
		mixed_array[1][j] = XOR(XOR(XOR(rotated[0][j],multiply_by_two(rotated[1][j])),
								multiply_by_three(rotated[2][j])),rotated[3][j])
		mixed_array[2][j] = XOR(XOR(XOR(rotated[0][j],rotated[1][j]),multiply_by_two(rotated[2][j])),
								multiply_by_three(rotated[3][j]))
		mixed_array[3][j] = XOR(XOR(XOR(multiply_by_three(rotated[0][j]),rotated[1][j]),rotated[2][j]),
								multiply_by_two(rotated[3][j]))
	return mixed_array
#----------------------------------------------------------------------------
def add_round_key(mixed_array,round_keys):
	print (round_keys)
	permuted = [[0]*4 for i in range (4)]
	for i in range(4):
		k=0
		for j in range(4):
			permuted[j][i] = XOR(mixed_array[j][i],round_keys[i][k:k+2]).rjust(2,'0')
			k+=2
	return permuted	
#----------------------------------------------------------------------------
def AES(permuted_array):
	for r in range(1,11): #rounds start from 1 to 10 	
		#step 1 : Substitution
		substituted = substitute2(permuted_array)
		print("substituted Array")
		for row in substituted:
			print (row)
		#step 2: Rotate rows
		rotated = []
		i=0
		for row in substituted:
			rotated.append(rotate_rows(row,i))
			i+=1
		print ("Rotated Array")
		for row in rotated:
			print (row)
		#step 3: mix column transformation
		mixed_array = mix_columns(rotated)
		print ("Mixed Array")
		for row in mixed_array:
			print (row)
		permuted_array = add_round_key(mixed_array,words_array[4*r:4*r+4])
		print("Rounded Array:")
		for row in permuted_array:
			print (row)
	return (permuted_array)	
#----------------------------------------------------------------------------
def main():
	original_key = '0F1571C947D9E8590CB7ADD6AF7F6798'
	plain_text = '0123456789ABCDEFFEDCBA9876543210'
	#Step 1 : Expand the 16-byte Key to get the Actual Key block to be used
	key_generation(original_key)
	#for key in words_array:
		#print (key)
	#Step 2 : One time Initialization of the 16-byte PLain Text BLock(Called as State)
	state_array = one_time_intialization(plain_text)
	print ("State Array")
	for i in range(len(state_array)):
		print state_array[i]
	#Step 3: Initial Permutation before starting the rounds
	permuted_array = init_permutation(state_array)
	print ("Initial Permuted Array")
	for row in permuted_array:
		print (row)
	#step 4: Start the rounds
		#1.Substitute Bytes
		#2.Shift Rows
		#3.Mix Columns
		#4.Add Round Key
		#AES function will perform all these 10 rounds and finally return the cipher text.
	permuted_array = AES(permuted_array)
	cipher_text=[]
	for i in range(4):
		for j in range(4):
			cipher_text.append(permuted_array[j][i])
	print ("Cipher Text :-","".join(cipher_text))
	
if __name__ == '__main__':
	main()