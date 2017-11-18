import sys

# Global vars

#The equation in which the variables are substituted
equation = str(sys.argv[1])
#List of variables
vars = []
#List of values for the variables
values = []

# Functions

#Function to find the variables used in the equation
def Parse(eq):
	for ch in eq:
		if ch.isalpha() and ch != '.':
			#if a variable is found add it to the list
			vars.append(ch)
			print(vars)
			#initialize variables with a 0 value
			values.append(0)


#Function to show a graphical display of the equation
def Graph(eq, x, ind):
	plane = ['|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|                                               ',
			 '|_______________________________________________'			 
	]
	y = []
	for xcoord in x:
		values[ind] = xcoord;
		y.append(Equate(eq))
	print(vars[ind] + ' = ' + str(x))
	print('Result = ' + str(y))
	
	yscale = max(y) / 14
	if yscale < 1:
		yscale = 1

	plane.reverse()
	for i in range(len(x)):
		temp =''
		xcoord = x[i] * 2
		ycoord = y[i] / yscale
		if ycoord < 0:
			continue
		if xcoord != 0:
			temp += plane[int(ycoord)][:xcoord]  
		temp += '*'
		if xcoord != len(plane[int(ycoord)]):
			temp += plane[int(ycoord)][xcoord+ 1:]
		plane[int(ycoord)] = temp	
	plane.reverse()
	plane[-1] += ' ' + str(max(x))
	print('\n\t' + str(14 * yscale))
	for line in plane:
		print('\t' + line)

#Function to evaluate the value of the equation by subbing in the value of the variables
def Equate(eq):
	#print(eq)

	#If eq is a number or variable sub in value
	if eq.isdigit() or eq[1:].isdigit():
		#print "returned"
		return float(eq)
	elif '.' in eq:
		#print "returned"
		j = eq.index('.')
		if (eq[:j].isdigit() or eq[1:j].isdigit()) and eq[j + 1:].isdigit():
			return float(eq)	
	elif eq in vars:
		return values[vars.index(eq)]

#Math operations	
	
	#Brackets
	if eq.find('[') != -1:
		start = eq.index('[')
		end = eq.index(']')
		j = len(eq) - 1
		while j >= 0:
			if eq[j] == ']':
				end = j
				break
			j -= 1

		st = ''
		if start != 0:
			st += eq[:start]
		st += str(Equate(eq[start + 1:end]))
		if end != len(eq):
			st += eq[end + 1:]
		return Equate(st) 
	#Subtraction
	if eq.find('-') != -1:
		i = eq.index('-')
		if i != 0 and eq[i-1] != '@' and eq[i-1] != '*' and eq[i-1] != '/':
			return Equate(eq[:i]) - Equate(eq[i + 1:]) 
	#Addition
	if eq.find('+') != -1:
		i = eq.index('+')
		return Equate(eq[:i]) + Equate(eq[i + 1:]) 
	#Multiplication
	if eq.find('*') != -1:
		i = eq.index('*')
		return Equate(eq[:i]) * Equate(eq[i + 1:]) 
	#Division
	if eq.find('/') != -1:
		i = eq.index('/')
		return Equate(eq[:i]) / Equate(eq[i + 1:]) 	
	#Exponents
	if eq.find('@') != -1:
		i = eq.index('@')
		return Equate(eq[:i]) ** Equate(eq[i + 1:])
	#Exponents
	if eq.find('%') != -1:
		i = eq.index('%')
		return Equate(eq[:i]) % Equate(eq[i + 1:])	 

################################################################## MAIN ################################################################## 

#Start program
print("Program start.............\n")

#Parse the equation 
Parse(equation)

#Commands to manipulate variables and equate results
comm = input('~~~: ')
while comm != 'quit':

	#Assign a new value to a variable
	if 'sub' in comm:
		#Variable and new value
		var = comm[comm.index('sub') + 4:comm.index('sub') + 5]
		val = float(comm[comm.index('=') + 2:])
		
		if var in vars:
			#Change value
			values[vars.index(var)] = val
			print("\tVALUE CHANGED: " + var + " = " + str(val))
		else:
			#Invalid var message
			print("\t ERR: That variable does not exist. Try again")	
	
	#Equate the result and use the variable values 
	elif comm == 'eq':
		print("\t"+ equation +"\tRESULT: " + str(Equate(equation)))  	
	
	#Equate the result of the equation using a range of values for a variable
	elif 'eq -r ' in comm:
		#Get command arguments
		args = comm.split(' ');

		#Check if all arguments are provided
		if len(args) < 6:
			print("\t ERR: Invalid number of arguments for range equate command")
		else:	
			#The variable name
			var = args[2]

			#Check if variable exists
			if var not in vars:
				print("\t ERR: That variable does not exist. Try again")
			else:
				#Range start value	
				start = float(args[3])
				#Range end value
				end = float(args[4])
				#Increment for start-end
				incr = float(args[5])
				#Store the previous value of the variable to reassign later
				prev = values[vars.index(var)]
			
				#Loop over range
				while start <= end:
					#Assign value to variable
					values[vars.index(var)] = start
					#Print result
					print('[' +var + ' = ' + str(start) + ']' + "\t"+ equation +"\tRESULT: " + str(Equate(equation)))
					#Increment
					start += incr
				#Reassign original variable value
				values[vars.index(var)] = prev

	#Graph equation
	elif 'graph' in comm:
		var = comm.split(' ')[1]
		x = range(0, int(comm.split(' ')[2]) + 1);
		Graph(equation, x, vars.index(var))
	#Print the value of a variable					
	elif 'val' in comm:
		var = comm.split(' ')[1]
		#Check if variable exists
		if var in vars:
			print(var + " = " + str(values[vars.index(var)]))
		else:
			print("\t ERR: That variable does not exist. Try again")
	#Print variables
	elif 'vars' in comm:
		print("\tVar Name\t|\t      Value\t\t")
		print("------------------------|------------------------------")
		for i in range(len(vars)):
			print('\t   ' + vars[i] + '     \t|\t\t' + str(values[i]))			
	elif 'help' in comm:
		print("-----List of commands-----")
		#Eq command
		print("\neq")
		print("\tEquate the result of the given equation substituting in the updated variable values")
		#Eq Range command
		print("\neq -r [var_name] [start] [end] [incr]")
		print("\tEquate the result of the equation using a range of values for a variable")
		print("\t>var_name: name of variable")
		print("\t>start: starting value of the range")
		print("\t>end: ending value of the range")
		print("\t>incr: range stepping value")
		#Graph command
		print("\ngraph [var_name] [range_max]")
		print("\tDisplay a graphical representation of the equation(with x from 0 to range_max)")
		print("\t>var_name: name of variable")
		print("\t>range_max: maximum x coordinate")
		#Vars command
		print("\nquit")
		print("\tExit the program")
		#Sub command
		print("\nsub [var_name] = [value]")
		print("\tAssign a value to a specific variable which is part of the equation")
		print("\t>var_name: name of variable")
		print("\t>value: decimal / int value to be assigned to the var")
		#Val command
		print("\nval [var_name]")
		print("\tPrint the value of a specific variable")
		print("\t>var_name: name of variable")
		#Vars command
		print("\nvars")
		print("\tPrint the value and name of all variables")

	#Invalid command
	else:
		print("\t ERR: Invalid command. Try again")
	comm = input('~~~: ') 

#End program
print('\n..............End Program')

