import os, sys, subprocess, re

input_file = sys.argv[1] #tableized clinvar P/LP file
query_gene = sys.argv[2] #gene to filter for
# output_file = input_file.rsplit(".", 1)[0]+".out"

# pdb_file = sys.argv[2]

# outfile = open(output_file, "w")
# outfile.write("select resi ")

with open(input_file, "r") as f:
	query_list = []
	for line in f:
		if query_gene in line and "/" in line.split()[8]: #and "p." in line:
			# print(line)
			line = line.split()
			AA = line[8]
			# print(AA)
			pos = line[7]
			# print(pos)
			# if pos.isdigit():
			# 	if int(pos) >= 1590 and int(pos) <= 1657:
			query_list.append(str(pos))

# outfile.write("MYH7 ")
# print(query_gene)
# count = 0
select_line = "sele resi " + "+".join(query_list)
print("\n"+select_line)
print("\n"+str(len(query_list))+" residues found! Copy and paste statment above into pymol. Manually select the right chain, e.g. sele chain A and resi...")
# for res in query_gene:
# 	outfile.write(str(res)+"+")
# 	if count % 20 == 0 and not count == 0:
# 		outfile.write("\nselect resi ")
# 	count += 1

# outfile.close()
