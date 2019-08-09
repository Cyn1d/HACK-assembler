import sys
import string
import os

try:
	os.remove("white_clean")
except:
	pass


def Assembler(file, file_name):


	temp_variables = []

	variables = {
	"SP":0,
	"LCL":1,
	"ARG":2,
	"THIS":3,
	"THAT":4,
	"R0":0,
	"R1":1,
	"R2":2,	
	"R3":3,
	"R4":4,
	"R5":5,
	"R6":6,
	"R7":7,
	"R8":8,
	"R9":9,
	"R10":10,
	"R11":11,
	"R12":12,
	"R13":13,
	"R14":14,
	"R15":15,
	"SCREEN":16384,
	"KBD":24576,
	}


	c_dest = {

	"null":"000",
	"M":"001",
	"D":"010",
	"MD":"011",
	"A":"100",
	"AM":"101",
	"AD":"110",
	"AMD":"111",
	}

	c_comp = {

	"0":["101010", 0],
	"1":["111111", 0],
	"-1":["111010", 0],
	"D":["001100", 0],
	"A":["110000", 0],
	"!D":["001101", 0],
	"!A":["110001", 0],
	"-D":["001111", 0],
	"-A":["110011", 0],
	"D+1":["011111", 0],
	"A+1":["110111", 0],
	"D-1":["001110", 0],
	"A-1":["110010", 0],
	"D+A":["000010", 0],
	"A+D":["000010", 0],
	"D-A":["010011", 0],
	"A-D":["000111", 0],
	"D&A":["000000", 0],
	"D|A":["010101", 0],
	"M":["110000", 1],
	"!M":["110001", 1],
	"-M":["110011", 1],
	"M-1":["110010", 1],
	"M+1":["110111", 1],
	"D+M":["000010", 1],
	"M+D":["000010", 1],
	"D-M":["010011", 1],
	"M-D":["000111", 1],
	"D&M":["000000", 1],
	"D|M":["010101", 1]
		}

	c_jump = {

	"null":"000",
	"JGT":"001",
	"JEQ":"010",
	"JGE":"011",
	"JLT":"100",
	"JNE":"101",
	"JLE":"110",
	"JMP":"111",

	}


	def clean_white_space(pass1file): #takes in an empty 'opened' file and write to it and closes it, dont forget to open the file in read for var and flag processing
		for line in file:
			first_slash = line.find("/")
			if not first_slash == -1:
				clean_line = line[:first_slash]
			else:
				clean_line = line[:]
			if whitecheck(clean_line) or clean_line == "\n":
				continue
			pass1file.write(f"{clean_line.strip()}\n")
		pass1file.close()

	def init_var(white_clean_file, temp_variables, variables):  #takes in a white cleaned file and processes all the variables
		for line in white_clean_file:
			if line.startswith("@"):
				try:
					a = int(line[1])
				except:
					a = line[1:-1]
					if a not in variables and (a not in temp_variables):
						temp_variables.append(a)
		white_clean_file.close()

	def init_flag(white_clean_file, temp_variables, variables): 
		line_position = 0
		for line in white_clean_file:
			if line.startswith("("):
				if line[1:-2] in temp_variables:
					temp_variables.remove(line[1:-2])
					variables[line[1:-2]] = line_position
				continue
			else:
				line_position += 1

	def temp_to_per(temp_variables, variables):
		counter = 16
		for i in temp_variables:
			variables[i] = counter
			counter += 1


	def whitecheck(code):
		if code == "" or code.startswith("/"):
			return True
		else:
			return False

	def main_assembler(variables, processed_file, final_file, c_dest, c_comp, c_jump):
		for line in processed_file:
			if line.startswith("@"):
				try:
					a = int(line[1:-1])
					final_file.write(f"0{str(bin(a)[2:]).zfill(15)}\n")
				except:
					a = int(variables[line[1:-1]])
					final_file.write(f"0{str(bin(a)[2:]).zfill(15)}\n")
			elif line.startswith("("):
				pass
			else:
				parsed_code = cparser(line[:-1], c_dest, c_comp, c_jump)
				final_file.write(f"{parsed_code}\n")
		final_file.close()
		processed_file.close()




	def cparser(ccode, c_dest, c_comp, c_jump):
		ccode = ccode.replace(" ", "")
		equal_sign_location = ccode.find("=")
		if equal_sign_location == -1:
			equal_sign_location = None
		semicolon_sign_location = ccode.find(";")
		if semicolon_sign_location == -1:
			semicolon_sign_location = None
		#git the location of equal and semicolon signs
		#not we will check for the three posible cases

		if not equal_sign_location == None and (not semicolon_sign_location == None): #both signs are present
			dest = c_dest[ccode[:equal_sign_location].strip()]
			comp = c_comp[ccode[equal_sign_location + 1:semicolon_sign_location].strip()][0]
			jump = c_jump[ccode[semicolon_sign_location+1:].strip]
			a = c_comp[ccode[equal_sign_location + 1:semicolon_sign_location]][1]
			
			return f"111{a}{comp}{dest}{jump}" #list in format [dest, comp, jump]
		elif not equal_sign_location == None:
			dest = c_dest[ccode[:equal_sign_location].strip()]
			comp = c_comp[ccode[equal_sign_location+1:].strip()][0]
			jump = c_jump["null"]
			a = c_comp[ccode[equal_sign_location + 1:semicolon_sign_location]][1]
			return f"111{a}{comp}{dest}{jump}"
		elif not semicolon_sign_location == None:
			dest = c_dest["null"]
			comp = c_comp[ccode[:semicolon_sign_location].strip()][0]
			jump = c_jump[ccode[semicolon_sign_location+1:].strip()]
			a = c_comp[ccode[:semicolon_sign_location]][1]
			return f"111{a}{comp}{dest}{jump}"



	white_clean_write = open("white_clean", "w")
	clean_white_space(white_clean_write)
	white_clean_read = open("white_clean", "r")
	init_var(white_clean_read, temp_variables, variables)
	file_flag = open("white_clean", "r")
	init_flag(file_flag, temp_variables, variables)
	file_flag.close()
	temp_to_per(temp_variables, variables)
	#variables ready
	final_input = open("white_clean", "r")
	final_output = open(f"{file_name[:-4]}.hack", "w")
	main_assembler(variables, final_input, final_output, c_dest, c_comp, c_jump)
	os.remove("white_clean")


if __name__ == "__main__":
	file_name = str(sys.argv[1])
	file = open(file_name, "r")
	Assembler(file, file_name)

    