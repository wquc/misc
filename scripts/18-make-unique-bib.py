inp_name = "reference-raw.bib"
out_name = "reference-new.bib"

entries = {}
with open(inp_name, 'r') as inp_file:
    for each_line in inp_file:
        if each_line.startswith("@"):
            each_bib   = ""
            each_entry = each_line.strip().split("{")[1][:-1]
        each_bib += each_line
        if each_line.startswith("}"):
            entries[each_entry] = each_bib
        
with open(out_name, 'w') as out_file:
    out_file.write("\n".join(entries.values()))
