import os, sys, subprocess, re, math
import numpy as np
from scipy import spatial, stats

# Run in termal as "python Search_space_scanning_on_aligned_pdb.py ../Pfams/Pfam_meta_domains/data/clinvar/clinvar_20190114/clinvar_20190114_GRCh37_onlyPathogenic_and_Likely_pathogenic.out_no_plugin_tableized_for_pfam_analysis clinvar_20201114_GRCh37_onlyBenign_and_Likely_benign_SCN5A.out_no_plugin_tableized_for_pfam_analysis SCN5A SCN2A Structures/Phyre_SCN5A_aligned_with_Phyre_SCN2A.prb.pdb SCN5A SCN2A"

tableized_file = sys.argv[1] #tableized clinvar P/LP file e.g. "../Pfams/Pfam_meta_domains/data/clinvar/clinvar_20190114/clinvar_20190114_GRCh37_onlyPathogenic_and_Likely_pathogenic.out_no_plugin_tableized_for_pfam_analysis"
benign_tableized_file = sys.argv[2] #e.g. clinvar_20201114_GRCh37_onlyBenign_and_Likely_benign_SCN5A.out_no_plugin_tableized_for_pfam_analysis
query_gene = sys.argv[3] #gene1 to filter for e.g. "SCN5A"
ref_gene = sys.argv[4] #gene2 to filter for e.g. "SCN2A"
aligned_pdb = sys.argv[5] #TM-align pdb file e.g. "Structures/Phyre_SCN5A_aligned_with_Phyre_SCN2A.prb.pdb"
aligned_pdb_chain_A_gene = sys.argv[6] #e.g. "SCN5A"
aligned_pdb_chain_B_gene = sys.argv[7] #e.g. "SCN2A"
# output_file = input_file.rsplit(".", 1)[0]+".out"

# pdb_file = sys.argv[2]

# outfile = open(output_file, "w")
# outfile.write("select resi ")

AA_dict = {
"R":"ARG", 
"H":"HIS",
"K":"LYS",
"D":"ASP",
"E":"GLU",
"S":"SER",
"T":"THR",
"N":"ASN",
"Q":"GLN",
"C":"CYS",
"G":"GLY",
"P":"PRO",
"A":"ALA",
"I":"ILE",
"L":"LEU",
"M":"MET",
"F":"PHE",
"W":"TRP",
"Y":"TYR",
"V":"VAL"
}

with open(tableized_file, "r") as f:
	query_list = []
	ref_list = []
	for line in f:			
		# print(line)
		line = line.split()

		if line[6] == query_gene: 
			AA = line[8].split("/")[0]
			pos = line[7]
			query_list.append(AA_dict[AA]+" "+str(pos))
		elif line[6] == ref_gene:
			AA = line[8].split("/")[0]
			pos = line[7]
			ref_list.append(AA_dict[AA]+" "+str(pos))

with open(benign_tableized_file, "r") as f:
	benign_query_list = []
	for line in f:			
		# print(line)
		line = line.split()

		if line[6] == query_gene: 
			AA = line[8].split("/")[0]
			pos = line[7]
			benign_query_list.append(AA_dict[AA]+" "+str(pos))
		# elif line[6] == ref_gene:
		# 	AA = line[8].split("/")[0]
		# 	pos = line[7]
		# 	ref_list.append(AA_dict[AA]+" "+str(pos))

with open(aligned_pdb, "r") as g:
	query_pdb_dict = {}
	query_pdb_coord_array = []
	# query_pdb_x_coords = {}
	# query_pdb_y_coords = {}
	# query_pdb_z_coords = {}

	benign_query_pdb_dict = {}
	benign_query_pdb_coord_array = []

	ref_pdb_dict = {}
	ref_pdb_coord_array = []
	# ref_pdb_x_coords = {}
	# ref_pdb_y_coords = {}
	# ref_pdb_z_coords = {}
	for line in g:
		if line.startswith("ATOM"):
			if line[21] == "A" and line[13:15] == "CA" and line[17:20] + " " + line[22:26].strip() in query_list:
				query_pdb_dict[float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())] = line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()
				query_pdb_coord_array.append([float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())])
				# query_pdb_x_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[30:38].strip()
				# query_pdb_y_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[38:46].strip()
				# query_pdb_z_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[46:54].strip()

			elif line[21] == "A" and line[13:15] == "CA" and line[17:20] + " " + line[22:26].strip() in benign_query_list:
				benign_query_pdb_dict[float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())] = line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()
				benign_query_pdb_coord_array.append([float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())])

			elif line[21] == "B" and line[13:15] == "CA" and line[17:20] + " " + line[22:26].strip() in ref_list:
				ref_pdb_dict[float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())] = line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()
				ref_pdb_coord_array.append([float(line[30:38].strip()), float(line[38:46].strip()), float(line[46:54].strip())])
				# ref_pdb_x_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[30:38].strip()
				# ref_pdb_y_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[38:46].strip()
				# ref_pdb_z_coords[line[6:11]+" "+line[13:15]+" "+line[17:20]+" "+line[21]+" "+line[22:26].strip()] = line[46:54].strip()

# print(ref_pdb_coord_array)

output_file = open(aligned_pdb.rsplit(".", 1)[0]+".P_LP_distance_calculated_out" ,"w")

p_distance_list = []
print("P/LP "+query_gene+" variants")
for residue in query_pdb_coord_array:
	# print(residue)
	distance = spatial.KDTree(ref_pdb_coord_array).query(residue)[0]
	print(query_pdb_dict[tuple(residue)], ref_pdb_dict[tuple(ref_pdb_coord_array[spatial.KDTree(ref_pdb_coord_array).query(residue)[1]])], distance)
	p_distance_list.append(distance)
	output_file.write(str(query_pdb_dict[tuple(residue)])+","+str(ref_pdb_dict[tuple(ref_pdb_coord_array[spatial.KDTree(ref_pdb_coord_array).query(residue)[1]])])+","+str(distance)+"\n")
p_RMSD = math.sqrt(np.mean([i ** 2 for i in p_distance_list]))
print(np.mean(p_distance_list), np.std(p_distance_list), p_RMSD)
output_file.close()

output_file = open(aligned_pdb.rsplit(".", 1)[0]+".B_LB_distance_calculated_out" ,"w")

b_distance_list = []
print("B/LB "+query_gene+" variants")
for residue in benign_query_pdb_coord_array:
	distance = spatial.KDTree(ref_pdb_coord_array).query(residue)[0]
	print(benign_query_pdb_dict[tuple(residue)], ref_pdb_dict[tuple(ref_pdb_coord_array[spatial.KDTree(ref_pdb_coord_array).query(residue)[1]])], distance)
	b_distance_list.append(distance)
	output_file.write(str(benign_query_pdb_dict[tuple(residue)])+","+str(ref_pdb_dict[tuple(ref_pdb_coord_array[spatial.KDTree(ref_pdb_coord_array).query(residue)[1]])])+","+str(distance)+"\n")
b_RMSD = math.sqrt(np.mean([i ** 2 for i in b_distance_list]))
print(np.mean(b_distance_list), np.std(b_distance_list), b_RMSD)
output_file.close()

print(stats.ks_2samp(p_distance_list, b_distance_list))
print(stats.ttest_ind(p_distance_list, b_distance_list, equal_var = False))

