import os, sys, subprocess, re

input_file = sys.argv[1]
output_file = input_file.rsplit(".", 1)[0]+".out"

# pdb_file = sys.argv[2]

outfile = open(output_file, "w")
outfile.write("select resi ")

with open(input_file, "r") as f:
	MYH7list = []
	for line in f:
		if "MYH7" in line and "p." in line:
				print(line)
				line = line.split("p.")
				AA = line[1].split(";")[0]
				print(AA)
				pos = AA[3:-3]
				print(pos)
				if pos.isdigit():
					if int(pos) >= 1590 and int(pos) <= 1657:
						MYH7list.append(pos)

# outfile.write("MYH7 ")
print(MYH7list)
count = 0
for res in MYH7list:
	outfile.write(str(res)+"+")
	if count % 20 == 0 and not count == 0:
		outfile.write("\nselect resi ")
	count += 1

outfile.close()
