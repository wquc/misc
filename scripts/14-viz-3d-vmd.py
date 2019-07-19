import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import textwrap

class Viz3dVmd(object):
    def __init__(self, x, y, z, w):
        self.x = w*x.flatten()
        self.y = w*y.flatten()
        self.z = w*z.flatten()
    def write_xyz(self, out_pref):
        with open(out_pref+'.xyz', 'w') as out_file:
            out_file.write('%d\n\n'%len(self.z))
            for x, y, z in zip(self.x, self.y, self.z):
                out_file.write("A %12.6f %12.6f %12.6f\n"%(x, y, z))
    def write_pdb(self, out_pref):
        # Implement this when handling different "layers" of data,
        # which can be colored based on ResName, Chain, etc.
        pass
    def write_tcl(self, out_pref):
        # Output script will read XYZ file by default.
        # Here the coordinate will be labeled when interacting with VMD.
        # However, more complicated information can be implemented such as
        # the system composition in high dimensional phase diagrams.
        with open(out_pref+'.tcl', 'w') as out_file:
            out_file.write("%s" % textwrap.dedent("""\
                # clear all text labels
                proc clear_label {} {
                    set molid [molinfo top get id]
                    draw delete all
                    mol showrep $molid 0 on
                    mol showrep $molid 1 off
                    puts "Label cleared" 
                }
                # interact and highlight a single atom then show information
                proc query_atom { args } {
                    global vmd_pick_atom vmd_pick_mol
                    draw delete all
                    set sele [atomselect $vmd_pick_mol "index $vmd_pick_atom"]
                    mol showrep $vmd_pick_mol 1 on
                    mol modselect 1 $vmd_pick_mol "index $vmd_pick_atom"
                    set coor [lindex [$sele get {x y z} ] 0]
                    set x [lindex $coor 0]
                    set y [lindex $coor 1]
                    set z [lindex $coor 2]
                    draw color blue
                    set info [format "%%4.3f %%4.3f %%4.3f" $x $y $z]
                    draw text "$x $y $z" $info size 1 thickness 2
                }
                #rep 0: original representation
                mol new %s type xyz
                set molid [molinfo top get id]
                mol modselect   0 $molid all
                mol modmaterial 0 $molid AOChalky
                mol modstyle    0 $molid VDW 1.0 20.0
                mol modcolor    0 $molid ResName
                # rep 1: highlighted atom
                mol addrep  $molid
                mol showrep $molid 1 off
                mol modmaterial 1 $molid Goodsell
                mol modstyle    1 $molid VDW 1.1 20.0
                mol modcolor    1 $molid ResName
                # activate trace of atom
                trace variable vmd_pick_atom w query_atom 
                user add key w { mouse mode pick }
                user add key q { clear_label }""" % (out_pref+'.xyz')))
        
if __name__ == "__main__":
    w = np.linspace(0, np.pi, 100)
    x, y = np.meshgrid(w, w)
    z = np.sin(x)**2+np.sin(y)**2
    demo =  Viz3dVmd(x, y, z, 100)
    demo.write_xyz('demo')
    demo.write_tcl('demo')
    Axes3D(plt.figure()).scatter(x, y, z, c=z.flatten(), cmap='jet', alpha=1)
    plt.show()