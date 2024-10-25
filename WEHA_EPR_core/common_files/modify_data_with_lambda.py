import numpy as np
from decimal import Decimal
import sys

#lamb = 0.5
lamb = float(sys.argv[1])
# The number of rows in the section
section_length = 40
# Number of columns in the section
num_columns = 5
# Input prmtop
input_file = sys.argv[2]
# Output prmtop
output_file2 = "mod2.prmtop"
output_file3 = "mod3.prmtop"
output_file4 = "mod4.prmtop"
output_file5 = "mod5.prmtop"
output_file4 =  sys.argv[3]

# Read all the lines from the input file
file = open(input_file)
lines = file.readlines()
file.close()

# Open the output file for writing
file = open(output_file2, 'w')

# Loop through all the lines in the file
for ind, l in enumerate(lines):
        # If the line contains the phrase in question
        if "FLAG LENNARD_JONES_ACOEF" in l:
                # Write the current and next line to the file
                file.write(l)
                file.write(lines[ind+1])
                # Index at the end of the section
                last_ind = ind + section_length + 2
                # Pull out the section of the list to modify
                x = np.array(lines[ind+2:last_ind])
                # List to contain all the newly calculated values
                new_vals = []
                # Loop through the array
                for l in x:
                        # Loop through the numeric values in the line
                        for n in l.split('  ')[1:]:
                                # Trim the newline characters
                                if "\n" in n:
                                        n = n[:-1]
                                # Convert to float and multiply by the lambda
                                new_vals.append(float(n.lower()) * lamb)
                # This is the new line to be saved to the file
                new_line = ''
                # Loop through all the new values
                for idx, val in enumerate(new_vals):
                        # Convert to scientific notation
                        sci = '  %.8E' % Decimal(val)
                        # Add to the new line
                        new_line += sci
                        # If it's the last in the column or out of values
                        if idx % num_columns == 4 or len(new_vals) - 1 == idx:
                                # Add new line character and write to the file 
                                new_line += '\n'
                                file.write(new_line)
                                new_line = ''
                # Break once we hit the section
                break
        else:   
                # Write all the lines on the way to the section
                file.write(l)

# Write all the lines after breaking
for l in lines[last_ind:]:
        file.write(l)
             
file.close() # Nice




file = open(output_file2)
lines = file.readlines()
file.close()

# Open the output file for writing
file = open(output_file3, 'w')

# Loop through all the lines in the file
for ind, l in enumerate(lines):
        # If the line contains the phrase in question
        if "FLAG LENNARD_JONES_BCOEF" in l:
                # Write the current and next line to the file
                file.write(l)
                file.write(lines[ind+1])
                # Index at the end of the section
                last_ind = ind + section_length + 2
                # Pull out the section of the list to modify
                x = np.array(lines[ind+2:last_ind])
                # List to contain all the newly calculated values
                new_vals = []
                # Loop through the array
                for l in x:
                        # Loop through the numeric values in the line
                        for n in l.split('  ')[1:]:
                                # Trim the newline characters
                                if "\n" in n:
                                        n = n[:-1]
                                # Convert to float and multiply by the lambda
                                new_vals.append(float(n.lower()) * lamb)
                # This is the new line to be saved to the file
                new_line = ''
                # Loop through all the new values
                for idx, val in enumerate(new_vals):
                        # Convert to scientific notation
                        sci = '  %.8E' % Decimal(val)
                        # Add to the new line
                        new_line += sci
                        # If it's the last in the column or out of values
                        if idx % num_columns == 4 or len(new_vals) - 1 == idx:
                                # Add new line character and write to the file 
                                new_line += '\n'
                                file.write(new_line)
                                new_line = ''
                # Break once we hit the section
                break
        else:   
                # Write all the lines on the way to the section
                file.write(l)

# Write all the lines after breaking
for l in lines[last_ind:]:
        file.write(l)
             
file.close() # Nice








file = open(output_file3)
lines = file.readlines()
file.close()

# Open the output file for writing
file = open(output_file4, 'w')

# Loop through all the lines in the file
for ind, l in enumerate(lines):
        # If the line contains the phrase in question
        if "FLAG DIHEDRAL_FORCE_CONSTANT " in l:
                # Write the current and next line to the file
                file.write(l)
                file.write(lines[ind+1])
                # Index at the end of the section
                last_ind = ind + section_length + 2
                # Pull out the section of the list to modify
                x = np.array(lines[ind+2:last_ind])
                # List to contain all the newly calculated values
                new_vals = []
                # Loop through the array
                for l in x:
                        # Loop through the numeric values in the line
                        for n in l.split('  ')[1:]:
                                # Trim the newline characters
                                if "\n" in n:
                                        n = n[:-1]
                                # Convert to float and multiply by the lambda
                                new_vals.append(float(n.lower()) * lamb)
                # This is the new line to be saved to the file
                new_line = ''
                # Loop through all the new values
                for idx, val in enumerate(new_vals):
                        # Convert to scientific notation
                        sci = '  %.8E' % Decimal(val)
                        # Add to the new line
                        new_line += sci
                        # If it's the last in the column or out of values
                        if idx % num_columns == 4 or len(new_vals) - 1 == idx:
                                # Add new line character and write to the file 
                                new_line += '\n'
                                file.write(new_line)
                                new_line = ''
                # Break once we hit the section
                break
        else:   
                # Write all the lines on the way to the section
                file.write(l)

# Write all the lines after breaking
for l in lines[last_ind:]:
        file.write(l)
             
file.close() # Nice


section_length = 12368
file = open(output_file4)
lines = file.readlines()
file.close()

# Open the output file for writing
file = open(output_file5, 'w')

# Loop through all the lines in the file
for ind, l in enumerate(lines):
        # If the line contains the phrase in question
        if "FLAG CHARGE" in l:
        #if "FLAG LENNARD_JONES_ACOEF" in l:
                # Write the current and next line to the file
                file.write(l)
                file.write(lines[ind+1])
                # Index at the end of the section
                last_ind = ind + section_length + 2
                # Pull out the section of the list to modify
                x = np.array(lines[ind+2:last_ind])
                print(x)
                new_vals = []
                # Loop through the array
                for l in x:
                        # Loop through the numeric values in the line
                        for n in l.split():
                                # Trim the newline characters

                                # Convert to float and multiply by the lambda
                                print(n)
                                new_vals.append(float(n.lower()) *lamb**2)
                # This is the new line to be saved to the file
                new_line = ''
                # Loop through all the new values
                for idx, val in enumerate(new_vals):
                        if val < 0:
                                sci = ' %.8E' % Decimal(val)
                        else:
                                # Convert to scientific notation
                                sci = '  %.8E' % Decimal(val)
                        # Add to the new line
                        new_line += sci
                        # If it's the last in the column or out of values
                        if idx % num_columns == 4 or len(new_vals) - 1 == idx:
                                # Add new line character and write to the file 
                                new_line += '\n'
                                file.write(new_line)
                                new_line = ''
                # Break once we hit the section
                break
        else:   
                # Write all the lines on the way to the section
                file.write(l)

# Write all the lines after breaking
for l in lines[last_ind:]:
        file.write(l)

             
file.close() # Nice


