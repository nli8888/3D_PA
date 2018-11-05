import os, sys, subprocess, re

input_file = sys.argv[1] #MYH7_and_paralogues_tableized.txt
output_file = input_file.rsplit(".", 1)[0]+".out"

# pdb_file = sys.argv[2]

outfile = open(output_file, "w")
# outfile.write("select resi ")

with open(input_file, "r") as f:
	MYH7list = []
	MYH14list = []
	for line in f:
		line = line.split()
		if line[6] == "MYH7":
			pos = line[7]
			AA = line[8].split("/")
			print(AA)
			if (
				len(AA) == 2 and 
				not "-" in pos #and
				# int(pos) >= 1590 and
				# int(pos) <= 1657
				):
				MYH7list.append(pos)

				# outfile.write(str(pos)+"+")
		elif line[6] == "MYH14":
			pos = line[7]
			AA = line[8].split("/")
			print(AA)
			if (
				len(AA) == 2 and 
				not "-" in pos
				):
				MYH14list.append(pos)
				# outfile.write(str(pos)+"+")

outfile.write("MYH7 ")
for res in MYH7list:
	outfile.write(str(res)+"+")
outfile.write("\nMYH14 ")
for res in MYH14list:
	outfile.write(str(res)+"+")

outfile.close()

# with open(pdb_file, "r") as g:
# 	for line in g:
