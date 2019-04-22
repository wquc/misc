/************************************
> Calculate RMSF of a trajectory.
> Compile with: g++ calc-rmsf.cpp
                      Q.W.(20190420)
************************************/
#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <regex>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <valarray>
#include <algorithm>

/* User defined data name or type*/
using Int  = size_t;
using Real = float;
using Str  = std::string;
struct PsfAtom {
    Int  atomid;
    Int  resid;
    Str  resname;
    Str  type;
    Real mass;
    PsfAtom() {}
    PsfAtom(Int a, Int r, Str n, Str t, Real m):
        atomid(a),resid(r),resname(n),type(t),mass(m) {}
};
using PsfResi = std::vector<PsfAtom>;

/* Global containers */
std::list<PsfResi>   all_residue;
std::valarray<float> all_rmsf;
std::valarray<float> x_avg;
std::valarray<float> y_avg;
std::valarray<float> z_avg;
std::valarray<float> x_tmp;
std::valarray<float> y_tmp;
std::valarray<float> z_tmp;

/* Helper functions declaration */
bool is_queried_atom(const PsfAtom& atom, const int& mode);
Int  read_psf(const Str& inp_name, const int& mode, const bool is_debugging);
void init_data(const Int& size);
void calc_rmsf(const Str& inp_name, Int psf_natom, const bool is_debugging);
void write_rmsf(const Str& out_name);

template<typename T>
bool is_in(const T& inp_mode, std::initializer_list<T> avail_modes) {
    return std::find(std::begin(avail_modes), std::end(avail_modes), inp_mode) != std::end(avail_modes);
}

template<typename T>
void DEBUG(T inpinfo) { 
    std::cout << "DEBUG> " << inpinfo << "\n"; 
}

/* Read PSF and DCD to calculate RMSF */
int main(int argc, char* argv[]) {
    std::ios_base::sync_with_stdio(false);
    std::cout << "EZ-RMSF> Calculate residue-wise Root Mean Square Fluctuations (version 1.0)\n"
              << "EZ-RMSF> Note current version does not support numerical atom type.\n";
    if (argc<5) {
        std::cerr << "ERROR> Insufficient input file!\n"
                  << "Usage> ./ez-rmsf ${mode} ${psfname} ${dcdname} ${outname}\n"
                  << "Usage> where:\n"
                  << "Usage>      mode | meaning\n"
                  << "Usage>      -----|--------\n"
                  << "Usage>        -1 | debug mode (all atoms)\n"
                  << "Usage>         0 | CA atoms\n"
                  << "Usage>         1 | Heavy atoms\n";
        return 1;
    }
    /* Parse input */
    int inp_mode = std::atoi(argv[1]);
    if(!is_in(inp_mode, {-1, 0, 1})) {
        std::cerr << "ERROR> Invalid mode.\n";
        return 1;
    }
    Str psf_name = argv[2];
    Str dcd_name = argv[3];
    Str out_name = argv[4];
    const bool is_debugging = (-1==inp_mode) ? true : false;
    /* Resize container and calculate RMSF */
    const auto psf_natom = read_psf(psf_name, inp_mode, is_debugging);
    init_data(psf_natom);
    calc_rmsf(dcd_name, psf_natom, is_debugging);
    write_rmsf(out_name);

    return 0;
}

/* Helper functions definition */
void init_data(const Int& size) {
    all_rmsf.resize(size);
    x_avg.resize(size);
    y_avg.resize(size);
    z_avg.resize(size);
    x_tmp.resize(size);
    y_tmp.resize(size);
    z_tmp.resize(size);
}

bool is_queried_atom(const PsfAtom& atom, const int& mode) {
    if(mode==-1 ) return true;
    if(mode==0 && "CA"==atom.type) return true;
    if(mode==1 && atom.type.front()!='H') return true;
    /* mode 2 is not implemented, unless Glycines are padded */
    if(mode==2 && atom.type.front()!='H' && atom.type!="C" && atom.type!="O" 
               && atom.type!="N" && atom.type!="CA") return true;
    return false;
}

Int read_psf(const Str& inp_name, const int& mode, const bool is_debugging) {
    std::cout << "ReadPSF> Reading PSF info from file: " << inp_name << "\n";
    std::ifstream inp_file(inp_name);
    if(!inp_file.is_open()) std::cerr << "Cannot open PSF file.\n";
    /* PSF records after reading.*/
    Int natom = 0;
    /* local variables */
    Int iatom = 0;
    Int iresi = 0;
    bool is_atom_entry  = false;
    bool is_new_residue = false;
    std::stringstream each_stream;
    Str place_holder, each_line;
    PsfAtom this_atom, last_atom;
    PsfResi tmp_residue;
    /* process PSF file */
    std::regex r_psfatom("^\\s+\\d+\\s!NATOM");
    while (getline(inp_file, each_line)) {
        if (std::regex_match(each_line, r_psfatom)) {
            is_atom_entry = true;
            Str natom_entry;
            std::stringstream entry_stream(each_line);
            entry_stream >> natom_entry;
            natom = std::atoi(natom_entry.c_str());
            continue;
        }
        if (is_atom_entry) {
            is_atom_entry = (++iatom < natom) ? true : false;
            each_stream.clear();
            each_stream.str(each_line);
            each_stream >> this_atom.atomid >> place_holder
                        >> this_atom.resid
                        >> this_atom.resname
                        >> this_atom.type   >> place_holder >> place_holder
                        >> this_atom.mass;
            if (this_atom.resid!=last_atom.resid) {
                iresi++;
                all_residue.push_back(tmp_residue);
                tmp_residue.clear();    
            }
            if (is_queried_atom(this_atom, mode)) tmp_residue.push_back(this_atom);            
            last_atom = this_atom;
            if (!is_atom_entry) all_residue.push_back(tmp_residue);
        }
    }
    all_residue.pop_front(); // the 0-th residue is desgined to be empty.
    /********* DEBUG *********/
    if (is_debugging) {
        DEBUG("(PSF) Recorded atoms:");
        for (const auto& each_residue : all_residue) {
            for (const auto& each_atom : each_residue) {
                std::cout << "DEBUG> " << each_atom.resname 
                          << " " << std::setw(10) << each_atom.resid << " ";
                          break;
            }
            for (const auto& each_atom : each_residue) {
                std::cout << each_atom.type << " ";
            }
            std::cout << "\n";
        }
    }
    /********* DEBUG *********/
    return natom;
}

void calc_rmsf(const Str& inp_name, Int psf_natom, const bool is_debugging) {
    std::cout << "ReadDCD> Processing DCD info from: " << inp_name << "\n";
    std::ifstream inp_file(inp_name, std::ios::binary);
    if(!inp_file.is_open()) std::cerr << "Cannot open DCD file.\n";
    /* Read and process header */
    char hdrbuf[100];
    inp_file.read(hdrbuf, 100);
    if(strncmp(&hdrbuf[4], "CORD", 4)!=0) std::cerr << "ERROR> Wrong DCD format.\n";
    const auto nframe = *(int*)(&hdrbuf[8]);
    const auto is_pbc = (1==*(int*)(&hdrbuf[48])) ? true:false;
    /* Read and print title */    
    const auto ntitle = *(int*)(&hdrbuf[96]);
    for (int i=0; i<ntitle; ++i) {
        inp_file.read(hdrbuf, 80);
        std::cout << "ReadDCD> " << hdrbuf << "\n";
    }
    /* Check if psf and dcd files match */
    inp_file.read(hdrbuf, 16);
    const auto dcd_natom = *(int*)(&hdrbuf[8]);
    if (dcd_natom != psf_natom) std::cerr << "ERROR> PSF and DCD file mismatch!\n";
    const auto pos = 100+80*ntitle+16;
    /* Process each frame to calculate average */
    const auto x_offset = (is_pbc) ? (15)                   : (1);	
    const auto y_offset = (is_pbc) ? (dcd_natom+17)         : (dcd_natom+3);
    const auto z_offset = (is_pbc) ? (2*dcd_natom+19)       : (2*dcd_natom+5);
    const auto sz_frame = (is_pbc) ? (3*(4*dcd_natom+8)+56) : (3*(4*dcd_natom+8));
    std::cout << "ReadDCD> Averaging structure ...\n";
    std::valarray<float> corbuf(sz_frame);
    for (auto iframe=0; iframe < nframe; ++iframe) {
        inp_file.read(reinterpret_cast<char*>(&corbuf[0]), sz_frame);
        x_avg += corbuf[std::slice(x_offset, dcd_natom, 1)];
        y_avg += corbuf[std::slice(y_offset, dcd_natom, 1)];
        z_avg += corbuf[std::slice(z_offset, dcd_natom, 1)];
    }
    x_avg /= nframe;
    y_avg /= nframe;
    z_avg /= nframe;
    /* Revisit each frame to calculate fluctuation */
    std::cout << "ReadDCD> Calculating fluctuation ...\n";
    inp_file.seekg(pos, std::ios::beg);
    for (auto iframe=0; iframe < nframe; ++iframe) {
        inp_file.read(reinterpret_cast<char*>(&corbuf[0]), sz_frame);
        x_tmp = corbuf[std::slice(x_offset, dcd_natom, 1)];
        y_tmp = corbuf[std::slice(y_offset, dcd_natom, 1)];
        z_tmp = corbuf[std::slice(z_offset, dcd_natom, 1)];
        all_rmsf += (x_tmp-x_avg)*(x_tmp-x_avg) + 
                    (y_tmp-y_avg)*(y_tmp-y_avg) +
                    (z_tmp-z_avg)*(z_tmp-z_avg);
        /********* DEBUG *********/
        if (is_debugging && 0==iframe) {
            DEBUG("(DCD) Coordinates of first atom in frame#1:");
            DEBUG(x_tmp[0]);
            DEBUG(y_tmp[0]);
            DEBUG(z_tmp[0]);
            DEBUG("(DCD) Coordinates of last  atom in frame#1:");
            DEBUG(x_tmp[dcd_natom-1]);
            DEBUG(y_tmp[dcd_natom-1]);
            DEBUG(z_tmp[dcd_natom-1]);
        }
        /********* DEBUG *********/
    }
    all_rmsf /= nframe;
    all_rmsf = std::sqrt(all_rmsf);
    inp_file.close();
}

void write_rmsf(const Str& out_name) {
    std::cout << "WriteRMSF> Writing RMSF data to file: " << out_name << "\n";
    std::ofstream out_file(out_name);
    if(!out_file.is_open()) std::cerr << "Cannot open output file.\n";
    out_file << std::fixed;
    for (const auto& each_residue : all_residue) {
        float residue_rmsf = 0.0;
        for (const auto& each_atom : each_residue) {
            residue_rmsf += all_rmsf[each_atom.atomid-1];
        }
        residue_rmsf /= each_residue.size();
        out_file << std::setw(12) << std::setprecision(6) << residue_rmsf << "\n";
    }
    out_file.close();
}
