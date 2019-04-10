/***************************************************************
 Build with: g++ -std=c++11 medial_axis.cpp
 Run with: ./a.out input_coor.dat
   where input_coor.dat contains the 2D coordinates 
   of consecutive segments encompass a polygon.
 Output format:
   TRIV> contains trivial vertices which are same as input
   SGMT> contains segments encompass the polygon
   VRTX> contains all Voronoi vertices
   EDGE> contains part of Voronoi vertices with finite endpoints.
                                                          by Q.W.
*****************************************************************/

#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <sstream>
#include <fstream>
#include <boost/format.hpp>
#include <boost/polygon/voronoi.hpp>
#include <boost/polygon/segment_data.hpp>

using boost::polygon::voronoi_builder;
using boost::polygon::voronoi_diagram;
using boost::polygon::point_data;
using boost::polygon::segment_data;

int main(int argc, char* argv[]) {
	const size_t SCALE = 1000000;
	// 0. Read input file of consecutive segments
	std::string inp_name;
	if(argc !=2 ) {
		std::cerr << "ERROR> Missing input file!" << std::endl;
		return 1;
	} else {
		std::cout << "INFO> Reading vertices of polygon from file [" 
			  << inp_name.assign(argv[1]) << "]" << std::endl
			  << "INFO> Expected in CW or CCW order"<< std::endl;
	}
	// 1. Retrive vertices from input
	std::vector<point_data<double> > points;
	std::ifstream inp_file(inp_name);
	std::string each_line;
	std::stringstream each_stream;
	double xcoor = 0.0;
	double ycoor = 0.0;
	while(std::getline(inp_file, each_line)) {
		if(each_line.empty()) continue;
		each_stream.clear();
		each_stream.str(each_line);
		each_stream >> xcoor >> ycoor;
		point_data<double> point(SCALE*xcoor, SCALE*ycoor);
		points.push_back(point);
	}
	// 2. Generate segments
	std::vector<segment_data<double> > segments;
	for (auto it1=points.cbegin(); it1!=points.cend(); ++it1) {
		auto it2 = (points.cend()-1==it1) ? points.cbegin() : std::next(it1);
		point_data<double> point1(it1->x(), it1->y());
		point_data<double> point2(it2->x(), it2->y());
		segments.push_back(segment_data<double>(point1, point2));

	}
	// 3. Construction of the Voronoi Diagram.
	voronoi_diagram<double> vd;
	construct_voronoi( segments.begin(), segments.end(), &vd);
	// 4. Write trivial vertices (TRIV), polygon segments (SGMT), 
	//    Voronoi vertices (VRTX), and Voronoi edges (EDGE) to output file
	std::string out_name = "vd_data_" + inp_name;
	std::ofstream out_file(out_name);
	for (auto it = points.cbegin(); it!= points.cend(); ++it) {
		out_file << "TRIV> "
  			 << boost::format("%11.6f")%(it->x()/SCALE) << " " 
  			 << boost::format("%11.6f")%(it->y()/SCALE) << std::endl;	
	}
	out_file << std::endl;
	for (auto it = segments.cbegin(); it != segments.cend(); ++it) {
		out_file << "SGMT> "
			 << boost::format("%11.6f")%(it->low().x()/SCALE)  << " "
			 << boost::format("%11.6f")%(it->low().y()/SCALE)  << " "
			 << boost::format("%11.6f")%(it->high().x()/SCALE) << " "
			 << boost::format("%11.6f")%(it->high().y()/SCALE) << std::endl;
	}
	out_file << std::endl;
	for (auto it = vd.vertices().begin(); it != vd.vertices().end(); ++it) {
		out_file << "VRTX> " 
  			 << boost::format("%11.6f")%(it->x()/SCALE) << " " 
  			 << boost::format("%11.6f")%(it->y()/SCALE) << std::endl;	
  		
	}
	out_file << std::endl;
	for (auto it = vd.edges().begin(); it != vd.edges().end(); ++it) {
		const voronoi_diagram<double>::edge_type& edge = *it;
		if (edge.is_finite()) {
			out_file << "EDGE> " 
				 << boost::format("%11.6f")%(edge.vertex0()->x()/SCALE) << " " 
				 << boost::format("%11.6f")%(edge.vertex0()->y()/SCALE) << " " 
				 << boost::format("%11.6f")%(edge.vertex1()->x()/SCALE) << " " 
				 << boost::format("%11.6f")%(edge.vertex1()->y()/SCALE) << std::endl;
		}
	}
	out_file.close();
	std::cout << "INFO> Voronoi diagram data written to file [" 
		  << out_name << "]" << std::endl;

	return 0;
}
