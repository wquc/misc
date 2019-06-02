import numpy as np

def rotMatOf3dVec(vec_curr, vec_targ):
    a = (vec_curr / np.linalg.norm(vec_curr)).reshape(3)
    b = (vec_targ / np.linalg.norm(vec_targ)).reshape(3)
    v = np.cross(a,b)
    c = np.dot(a,b)
    s = np.linalg.norm(v)
    I = np.identity(3)
    x = '%f %f %f; %f %f %f;  %f %f %f'%(0, -v[2], v[1], v[2], 0, -v[0], -v[1], v[0], 0)
    k = np.matrix(x)
    r = I + k + np.matmul(k,k) * ((1 -c)/(s**2))
    return r

class PdbAtom():
    def __init__(self, s):
        self.header   = s[0:6]
        self.atomid   = int(s[6:11])
        self.atomname = s[12:16]
        self.resname  = s[17:20]
        self.chain    = s[21:22]
        self.resid    = int(s[22:26])
        self.coor     = np.array(map(float,[s[30:38], s[38:46], s[46:54]]))
        self.occu     = float(s[54:60])
        self.beta     = float(s[60:66])
        self.atomtype = s[76:78]
    def trans_by(self, dcoor):
        self.coor = self.coor + dcoor
    def rotate_by(self, rotamat):
        self.coor = np.array(np.dot(rotamat, self.coor))[0]
    def gen_entry(self):
        X = ' '
        return '%6s'%self.header + '%5d'%self.atomid + X + \
               '%4s'%self.atomname + X + \
               '%3s'%self.resname + X + \
               '%1s'%self.chain + '%4d'%self.resid + X*4 + \
               '%8.3f'%self.coor[0] + '%8.3f'%self.coor[1] + '%8.3f'%self.coor[2] + \
               '%6.2f'%self.occu + '%6.2f'%self.beta + X*10 + '%2s'%self.atomtype

if __name__=='__main__':

    # 0. User specification 
    inp_pdb_name = '5vjh.pdb'
    inp_chl_name = 'channel.dat'
    target_chl_vec = (0, 0, 1)
    query_3dfit  = True
    out_pdb_name = 'result.pdb'

    # 1. Read system from input PDB file
    with open(inp_pdb_name, 'r') as inp_file:
        pdb_atom = [PdbAtom(line) for line in inp_file if line.startswith(('ATOM','HETA'))]

    # 2. Center the system
    offset = -1.0*np.mean([each_atom.coor for each_atom in pdb_atom], axis=0)
    map(lambda each_atom:each_atom.trans_by(offset), pdb_atom)
    
    # 3. find the best fitted vector along the channel - channel vector (normalized)
    #    np.linalg.svd() will return U, D, and V.  Thus [2] refers to V and [0] refers 
    #    to the vector with largest singluar value.
    chl_data = np.genfromtxt(inp_chl_name)
    chl_mean = chl_data.mean(axis=0)
    chl_vec = np.linalg.svd(chl_data - chl_mean)[2][0]
    chl_vec = chl_vec / np.linalg.norm(chl_vec)
    
    # 4. Calculate the rotation matrix and apply to the system.
    rotamat = rotMatOf3dVec(chl_vec, target_chl_vec)
    map(lambda each_atom:each_atom.rotate_by(rotamat), pdb_atom)
    with open(out_pdb_name, 'w') as out_file:
        out_file.write('\n'.join(each_atom.gen_entry() for each_atom in pdb_atom ))

    # 5. Visualize fitting result if queried
    if query_3dfit:
        import matplotlib.pyplot as plt
        import mpl_toolkits.mplot3d as m3d
        dims = int(np.max(np.max(chl_data, axis=0)-np.min(chl_data, axis=0)))
        linepts = chl_vec * np.mgrid[-dims:dims:2j][:, np.newaxis]
        linepts = linepts + chl_mean
        linevec = linepts[1] - linepts[0]
        linevec = linevec/np.linalg.norm(linevec)
        ax = m3d.Axes3D(plt.figure())
        ax.scatter3D(*chl_data.T)
        ax.plot3D(*linepts.T)
        plt.show()