/********************************************************
* >Usage:                                               *
*  Run the program with 1 or 2:                         *
*    1. qatcor input.psf inp1.cor inp2.cor ... inpN.cor *
*    2. qatcor input.psf $(ls -v *.cor)                 *
*  Output dcd will be:                                  *
*    input.dcd                                          *
* >Notes:                                               *
*  1. Use file prefix of PSF file for output dcd.       *
*  2. Use NATOM and TITLE of PSF file for dcd header    *
********************************************************/

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdlib>
#include <vector>

using Int = unsigned int;
using Str = std::string;
using StrVec = std::vector<std::string>;
using NumVec = std::vector<float>;

NumVec X;
NumVec Y;
NumVec Z;

struct DcdHeader {
    int32_t natom;
    int32_t nfile;
    int32_t npriv;
    int32_t nsavc;
    int32_t nstep;
    int32_t ifpbc;
    int32_t ntitle;
    float delta;
    StrVec title;
    DcdHeader() {}
    DcdHeader(int32_t natom, int32_t nfile, int32_t npriv, 
              int32_t nsavc, int32_t nstep, int32_t ifpbc, 
              float delta, const StrVec& title):
              natom(natom), nfile(nfile), npriv(npriv),
              nsavc(nsavc), nstep(nstep), ifpbc(ifpbc),
              delta(delta), title(title) {
                this->ntitle = this->title.size();
    }
};

const struct DcdPads {
    const int32_t pad0   = 0;
    const int32_t pad2   = 2;
    const int32_t pad4   = 4;
    const int32_t pad24  = 24;
    const int32_t pad84  = 84;
    const int32_t pad164 = 164;  
} dcdpads;

bool process_psf(const Str& psf_name, Int& natom, StrVec& title);
bool process_cor(const Str& cor_name, Int& natom, NumVec& X, NumVec& Y, NumVec& Z);
void write_dcdheader(std::ofstream& dcd_file, const DcdHeader& dcdheader);
void write_dcdframes(std::ofstream& dcd_file, const int& natom, 
                     const float* fX, const float* fY, const float* fZ);

int main(int argc, char* argv[]) {
    if(argc < 3) {
        std::cerr << "ERROR> Not enough parameter"
                  << std::endl
                  << "ERROR> Usage: qatcor input.psf inp1.cor inp2.cor ... inpN.cor"
                  << std::endl;
        return EXIT_FAILURE;
    } else {
        std::cout << "INFO> QATCOR version 1.0"
                  << std::endl
                  << "INFO> NOTE: This program does NOT check NATOMs." 
                  << std::endl;
    }

    const int NFILE = argc - 2;
    const Str psfname = argv[1];
    const Str outpref = psfname.substr(0, psfname.length()-4);
    
    Int NATOM;
    StrVec TITLE;
    if(!process_psf(psfname, NATOM, TITLE)) return EXIT_FAILURE;
    
    X.resize(NATOM);
    Y.resize(NATOM);
    Z.resize(NATOM);

    /* 1. Write dcd header */
    std::ofstream out_file(outpref + ".dcd", std::ios::binary);
    const DcdHeader dcdheader(NATOM, NFILE, 0, 1, NFILE, 0, 1, TITLE);
    write_dcdheader(out_file, dcdheader);

    /* 2. Write dcd frames */
    for (auto ifile=0; ifile<NFILE; ++ifile) {
        process_cor(argv[2+ifile], NATOM, X, Y, Z);
        write_dcdframes(out_file, NATOM, X.data(), Y.data(), Z.data());
    }
    out_file.close();
    
    return EXIT_SUCCESS;
}

bool process_psf(const Str& psf_name, Int& natom, StrVec& title) {
    std::ifstream inp_file(psf_name);
    if (!inp_file.is_open()) {
        std::cerr << "ERROR> Cannot open file: "  << psf_name 
                  << std::endl;
        return false;
    } else {
        std::cout << "INFO> Reading PSF information from: " << psf_name 
                  << std::endl;
    }
    Str each_line;
    std::stringstream each_stream;
    while(std::getline(inp_file, each_line)) {
        if (0 == each_line.length()) continue;
        if ('*' == each_line.front()) {
            title.push_back(each_line);
        } else if ("!NATOM" == each_line.substr(each_line.length()-6)) {
            each_stream.str(each_line);
            each_stream >> natom;
        }
    }
    inp_file.close();
    return true;
}

bool process_cor(const Str& cor_name, Int& natom, NumVec& X, NumVec& Y, NumVec& Z) {
    std::ifstream inp_file(cor_name);
    if (!inp_file.is_open()) {
        std::cerr << "ERROR> Cannot open file: " << cor_name
                  << std::endl;
        return false;
    } else {
        std::cout << "INFO> Reading COR information from: " << cor_name
                  << std::endl;
    }
    Str each_line, tmp;
    std::stringstream each_stream;
    float x, y, z;
    unsigned int i;
    while(std::getline(inp_file, each_line)) {
        if (each_line.length() < 6) continue;
        if ('*' == each_line.front()) continue;
        each_stream.str(each_line);
        each_stream >> i >> tmp >> tmp >> tmp >> x >> y >> z;
        X[i-1] = x;
        Y[i-1] = y;
        Z[i-1] = z;
    }
    inp_file.close();
    return true;
}

void write_dcdheader(std::ofstream& dcd_file, const DcdHeader& dcdheader) {
    /* dcd header part 1. */
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad84), 4);
    dcd_file.write("CORD", 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.nfile), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.npriv), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.nsavc), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.nstep), 4);
    for(int i=0; i<5; ++i)
        dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad0), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.delta), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.ifpbc), 4);
    for(int i=0; i<8; ++i)
        dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad0), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad24), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad84), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad164), 4);
    dcd_file.write(reinterpret_cast<const char*>(&(dcdheader.ntitle)), 4);
    /* dcd header part 2. */
    for(const auto& t : dcdheader.title)
        dcd_file.write(t.data(), 80);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad164), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad4), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdheader.natom), 4);
    dcd_file.write(reinterpret_cast<const char*>(&dcdpads.pad4), 4);
}

void write_dcdframes(std::ofstream& dcd_file, const int& natom, 
                     const float* fX, const float* fY, const float* fZ) {
    const int32_t pad4N = 4*natom;
    /* write x coordinates. */
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
    dcd_file.write(reinterpret_cast<const char*>(fX), pad4N);
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
    /* write y coordinates. */
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
    dcd_file.write(reinterpret_cast<const char*>(fY), pad4N);
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
    /* write z coordinates. */
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
    dcd_file.write(reinterpret_cast<const char*>(fZ), pad4N);
    dcd_file.write(reinterpret_cast<const char*>(&pad4N), 4);
}
