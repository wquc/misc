import struct

def process_dcd(dcd_name):
    with open(dcd_name, 'rb') as inp_file:
        ### Process header1[100]
        fileBuffer = inp_file.read(100)
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
        fileBuffer = inp_file.read(SZFRAME)
        coorBufLen = len(fileBuffer)/3
        ### DCD file format for frame[SZFRAME]: 
        ### 1*int+NATOM*float+1*int + 1*int+NATOM*float+1*int + 1*int+NATOM*float+1*int
        ### ^^^^^^^^^^^^^^^^^^^^^^^x  ^^^^^^^^^^^^^^^^^^^^^^^y  ^^^^^^^^^^^^^^^^^^^^^^^z
        struct_fmt = 'i%dfi'%NATOM
        xcoor = struct.unpack(struct_fmt, fileBuffer[0*coorBufLen:1*coorBufLen])[1:-1]
        ycoor = struct.unpack(struct_fmt, fileBuffer[1*coorBufLen:2*coorBufLen])[1:-1]
        zcoor = struct.unpack(struct_fmt, fileBuffer[2*coorBufLen:3*coorBufLen])[1:-1]
    return NATOM, xcoor, ycoor, zcoor

if __name__=='__main__'	:
    dcd_name = '1ubq.dcd'
    natom, xcoor, ycoor, zcoor = process_dcd(dcd_name)
    print natom
    for x, y, z in zip(xcoor, ycoor, zcoor):
        print "%12.6f %12.6f %12.6f"%(x, y, z)
        break
