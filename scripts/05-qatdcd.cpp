/*********************************************************
 Usage:
 1. Compile the program with: 
    g++ qatdcd.cpp -o qatdcd
 2. Merge trajectories with: 
    ./qatdcd alltraj.dcd traj1.dcd traj2.dcd ... trajn.dcd
             ^^^^^^^^^^^ name of final trajectory.
                                              Q.W.20190202
*********************************************************/

#include <iostream>
#include <fstream>
#include <cstring>
#include <vector>

using std::cout;
using std::endl;
using std::cerr;

int main(int argc, char** argv) {
    cout << "INFO> QATDCD version 1.1" << endl
         << "INFO> This program does NOT check sanity of trajectory files." << endl
         << "INFO> Merged trajectory will have same header as the first input except NFILE and NSTEP." << endl
         << "INFO> --------------------------------" << endl;
    if (argc<3) {
        cerr << "ERROR> Not enough input arguments!" << endl;
        return 1;
    }
    int  frame_counter = 0;
    int  step_counter  = 0;
    char dcd_head1[100];
    char dcd_title1[80];
    char dcd_title2[80];
    char dcd_head2[16];
    std::vector<float> dcd_buffer;
    std::ofstream out_file(argv[1], std::ios::binary);
    for (int i=2; i<argc; ++i) {
        char* dcd_name = argv[i];
        std::ifstream inp_file(dcd_name, std::ios::binary);
        if(!inp_file.is_open()) {
            cerr << "ERROR> Cannot open DCD file." << dcd_name << endl;
            return 1;
        } else {
            cout << "INFO> Reading trajectory: " << dcd_name << endl;
        }
        inp_file.read(dcd_head1, 100);
        inp_file.read(dcd_title1, 80);
        inp_file.read(dcd_title2, 80);
        inp_file.read(dcd_head2, 16);
        int n_file = *(int*)(&dcd_head1[8]);
        int n_priv = *(int*)(&dcd_head1[12]);
        int n_savc = *(int*)(&dcd_head1[16]);
        int n_step = *(int*)(&dcd_head1[20]);
        int q_cell = *(int*)(&dcd_head1[48]);
        int n_atom = *(int*)(&dcd_head2[8]);
        int sz_frame = q_cell ? (3*(4*n_atom+8)+56) : (3*(4*n_atom+8));
        dcd_buffer.resize(sz_frame*n_file);
        if(2==i) {   
            out_file.write(dcd_head1, 100);
            out_file.write(dcd_title1, 80);
            out_file.write(dcd_title2, 80);
            out_file.write(dcd_head2, 16);
        }
        inp_file.read(reinterpret_cast<char*>(&dcd_buffer[0]), sz_frame*n_file);
        out_file.write(reinterpret_cast<char*>(&dcd_buffer[0]), sz_frame*n_file);
        inp_file.close();
        frame_counter += n_file;
        step_counter  += n_step;
    }
    out_file.seekp(8, std::ios::beg);
    out_file.write(reinterpret_cast<const char*>(&frame_counter), 4);
    out_file.seekp(20, std::ios::beg);
    out_file.write(reinterpret_cast<const char*>(&step_counter), 4);
    cout << "INFO> --------------------------------" << endl
         << "INFO> DCD merge completed." << endl
         << "INFO> Overall number of frames: " << frame_counter << endl
         << "INFO> Overall number of steps:  " << step_counter  << endl;
    out_file.close();

    return 0;
}