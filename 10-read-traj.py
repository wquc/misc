import struct

def process_dcd(dcd_name):
    with open(dcd_name, 'rb') as inp_file:
        ### Process header1[100]
        fileBuffer = inp_file.read(100)
        NFILE   = struct.unpack("i", fileBuffer[8:12])[0]
        has_pbc = 1==struct.unpack("i",fileBuffer[48:52])[0]
        NTITLE  = struct.unpack("i",fileBuffer[96:])[0]
        ### Process title[NTITLE*80]
        for _ in range(NTITLE):
            fileBuffer = inp_file.read(80)
            print fileBuffer
        ### Retrieve NATOM from header2[16]
        fileBuffer = inp_file.read(16)
        NATOM  = struct.unpack("i",fileBuffer[8:12])[0]
        xoffset = 15 if has_pbc else 1
        yoffset = NATOM+17 if has_pbc else NATOM+3
        zoofset = 2*NATOM+19 if has_pbc else 2*NATOM+5
        SZFRAME = 3*(4*NATOM+8)+56 if has_pbc else 3*(4*NATOM+8)
        for _ in range(NFILE):
            fileBuffer = inp_file.read(SZFRAME)
            coorBufLen = len(fileBuffer)/3
            ### DCD file format for frame[SZFRAME]: 
            ### 1*int+NATOM*float+1*int + 1*int+NATOM*float+1*int + 1*int+NATOM*float+1*int
            ### ^^^^^^^^^^^^^^^^^^^^^^^x  ^^^^^^^^^^^^^^^^^^^^^^^y  ^^^^^^^^^^^^^^^^^^^^^^^z
            struct_fmt = 'i%dfi'%NATOM
            xcoor = struct.unpack(struct_fmt, fileBuffer[0*coorBufLen:1*coorBufLen])[1:-1]
            ycoor = struct.unpack(struct_fmt, fileBuffer[1*coorBufLen:2*coorBufLen])[1:-1]
            zcoor = struct.unpack(struct_fmt, fileBuffer[2*coorBufLen:3*coorBufLen])[1:-1]
            yield NATOM, xcoor, ycoor, zcoor

if __name__=='__main__'	:
    dcd_name = '1ubq.dcd'
    ### Print Number of atoms, coordinates of 1st atom in 1st frame for testing.
    for natom, xcoor, ycoor, zcoor in process_dcd(dcd_name):
        print natom, xcoor[0], ycoor[0], zcoor[0]
        break
