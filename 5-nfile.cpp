/***************************************************
Description:
    Correct NFILE record in dcd header of trajectory 
        from CHARMM AFM simulation.
Usage:
    Compile with: g++ nfile.cpp -o nfile.exe
    Run with: ./nfile.exe inptraj.dcd
***************************************************/

#include <iostream>
#include <fstream>

int main(int argc, char* argv[]) {
    if (argc<2) {
        std::cout << "ERROR> No input trajectory file deteced!\n";
        return 1;
    } else {
        std::cout << "INFO> This program will modify the original trajectory file.\n" 
                  << "INFO> Make backups if necessary.\n";
    }
    
    char* dcd_name = argv[1];
    std::ifstream tmp_file(dcd_name, std::ifstream::ate | std::ifstream::binary);
    int file_size = tmp_file.tellg(); 
    tmp_file.close();
    
    char dcd_head1[100];
    char dcd_title1[80];
    char dcd_title2[80];
    char dcd_head2[16];

    std::fstream inp_file(dcd_name, std::ios::binary | std::ios::in | std::ios::out);
    inp_file.read(dcd_head1, 100);
    inp_file.read(dcd_title1, 80);
    inp_file.read(dcd_title2, 80);
    inp_file.read(dcd_head2, 16);

    int n_file = *(int*)(&dcd_head1[8]);
    int q_cell = *(int*)(&dcd_head1[48]);
    int n_atom = *(int*)(&dcd_head2[8]);
    int sz_frame = q_cell ? (3*(4*n_atom+8)+56) : (3*(4*n_atom+8));
    
    std::cout << "INFO> " << n_atom << " atoms detected.\n"
              << "INFO> " << n_file << " frames expected.\n";
    n_file = (file_size - 260) / sz_frame;
    std::cout << "INFO> After correction, " << n_file << " frames will be used.\n";
    inp_file.seekp(8, std::ios::beg);
    inp_file.write(reinterpret_cast<const char*>(&n_file), 4);
    inp_file.close();
    std::cout << "Done.\n";

    return 0;
}
