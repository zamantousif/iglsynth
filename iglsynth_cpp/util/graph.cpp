//
// Created by abhibp1993 on 2/23/20.
//

#include "types.h"
#include "graph.h"
#include <iostream>
#include <stdexcept>

namespace IGLSynth {

    // Read-Only Properties
    int Graph::num_edges(){
        return Graph::edges_.size();
    }

    int Graph::num_vertices(){
        return Graph::vemap_.size();
    }

    bool Graph::is_multigraph(){
        std::cerr << "Not Implemented Error" << std::endl;
    }
    
    std::string Graph::tostring(){
        return "<" + class_name_ + " object with id=" + id_ + ">";
    }

    // Containment checking
//    bool Graph::contains_vertex(Vertex &u);


//    bool contains_edge(Edge &e);
//
//    // Graph manipulation
    bool Graph::add_edge(boost::shared_ptr<Graph::Edge> e){
        // Return true: if added, false: if not added.
        try{
            // Edge already present in Graph
            if(Graph::edges_.find(e) != Graph::edges_.end()){
                std::cout << "The edge is already present in the Graph. Ignoring request to add." << std::endl;
                return false;
            }
            // Edge not present in Graph
            if(Graph::edges_.find(e) == Graph::edges_.end()){
                Graph::edges_.insert(e);
                std::cout << "Successfully added the edge" << std::endl;
                return true;
            }
        }
        catch(std::exception& ep){
            // Catch standard exceptions
            std::cout << "Error adding the Edge, exception : " << ep.what() << std::endl;
            return false;
        }
        catch(...){
            // Catch any other exception
            std::cout << "Error adding the Edge, some other exception occurred" << std::endl;
            return false;
        }

    }
//    bool add_edges(std::vector<Edge> &e);       // Return true: if added, false: if not added.
//    bool add_vertex(Vertex &u);                 // Return true: if added, false: if not added.
//    bool add_vertices(std::vector<Vertex> &e);  // Return true: if added, false: if not added.
//
//    bool rem_edge(Edge &e);                     // Return true: if added, false: if not added.
//    bool rem_edges(std::vector<Edge> &e);       // Return true: if added, false: if not added.
//    bool rem_vertex(Vertex &u);                 // Return true: if added, false: if not added.
//    bool rem_vertices(std::vector<Vertex> &e);  // Return true: if added, false: if not added.
//
//    std::vector<Edge> &get_edges(Vertex &u);
//
//    std::vector<Edge> &get_edges(Vertex &u, Vertex &v);
//
//    std::vector<Edge> &get_in_edges(Vertex &v);
//
//    std::vector<Edge> &get_out_edges(Vertex &u);
//
//    std::vector<Edge> &get_neighbors(Vertex &u);
//
//    std::vector<Edge> &get_in_neighbors(Vertex &v);
//
//    std::vector<Edge> &get_out_neighbors(Vertex &u);

}