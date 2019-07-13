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
#include <iomanip>

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
    
    std::fstream inp_file(dcd_name, std::ios::binary | std::ios::in | std::ios::out);
    char hdrbuf[100];
    inp_file.read(hdrbuf, 100);
    auto n_file = *(int*)(&hdrbuf[8]);
    const auto is_pbc = (1==*(int*)(&hdrbuf[48])) ? true:false;
    /* Read and print title */    
    const auto ntitle = *(int*)(&hdrbuf[96]);
    for (int i=0; i<ntitle; ++i) {
        inp_file.read(hdrbuf, 80);
        std::cout << "ReadDCD> " << hdrbuf << "\n";
    }
    /* Check if psf and dcd files match */
    inp_file.read(hdrbuf, 16);
    const auto n_atom = *(int*)(&hdrbuf[8]);
    const auto sz_header = 100+80*ntitle+16;
    const auto sz_frame  = is_pbc ? (3*(4*n_atom+8)+56) : (3*(4*n_atom+8));
    
    std::cout << "INFO> NFILE before correction: "<< n_file << "\n";
    n_file = (file_size - sz_header) / sz_frame;
    inp_file.seekp(8, std::ios::beg);
    inp_file.write(reinterpret_cast<const char*>(&n_file), 4);
    inp_file.close();
    std::cout << "INFO> NFILE after  correction: "<< n_file << "\n";

    return 0;
}
