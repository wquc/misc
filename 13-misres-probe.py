import sys

inp_name = sys.argv[1]

# 1. Record each chain and corresponding residue
chains = {}
with open(inp_name, 'r') as inp_file:
    for each_line in inp_file:
        if not each_line.startswith('ATOM'):
            continue
        if each_line[12:16].strip() != 'CA':
            continue
        each_chain = each_line[21:22]
        each_resid = int(each_line[22:26])
        if each_chain in chains:
            chains[each_chain].append(each_resid)
        else:
            chains[each_chain] = [each_resid]

# 2. Probe missing residues in each chain
for each_chain in sorted(chains.keys()):
    residues = chains[each_chain]
    sys.stdout.write("-----> chain [%s] (%5d) to (%5d)\n" % 
        (each_chain, residues[0], residues[-1]))
    ref_resid = residues[0]
    for each_resid in residues:
        if ref_resid != each_resid:
            sys.stdout.write("missing residue: (%5d) to (%5d)\n" % 
                (ref_resid, each_resid-1)) 
            ref_resid = each_resid
        ref_resid += 1
    sys.stdout.write("\n")