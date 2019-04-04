#!/usr/bin/env python

# Save customized viewpoint of structure from VMD visulization state
inp_name = 'setview.vmd'
out_name = 'orient.tcl'

with open(inp_name, 'r') as inp_file, open(out_name, 'w') as out_file:
    for each_line in inp_file:
        if each_line.startswith('set viewpoints'):
            out_str = 'set viewplist {}\n' + \
                       each_line + \
                      'lappend viewplist [molinfo top]\n' + \
                      'foreach v $viewplist {\n' + \
                      '  molinfo $v set {center_matrix rotate_matrix scale_matrix global_matrix} $viewpoints($v)\n' + \
                      '}\n' + \
                      'unset viewplist\n'
            out_file.write('%s'%out_str)
            break