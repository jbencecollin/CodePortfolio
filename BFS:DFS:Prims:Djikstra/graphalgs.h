/* * * * * * *
 * Module containing various graph algorithms.
 *
 * created for COMP20007 Design of Algorithms 2020
 * by Tobias Edwards <tobias.edwards@unimelb.edu.au>
 */

#ifndef GRAPHALGS_H
#define GRAPHALGS_H

#include "graph.h"

// Runs a depth first search on the given graph, returning a dynamically
// allocated array of integers representing the order in which the DFS
// visits the nodes in the graph.
//
// The resultant array will be of size n_vertices and must be freed after use.
int *dfs(Graph *graph);

// Runs a breadth first search on the given graph, returning a dynamically
// allocated array of integers representing the order in which the DFS
// visits the nodes in the graph.
//
// The resultant array will be of size n_vertices and must be freed after use.
int *bfs(Graph *graph);

// Runs Prim's algorithm on a given graph and stores the edges in the
// arrays from and to (such that each from[i], to[i] pair forms an edge
// in the minimium spanning tree).
//
// from and to should already be malloc'd and have length n - 1.
//
// Returns whether or not the algorithm was succesful.
bool prims(Graph *graph, int *from, int *to);

// Run Dijkstra's algorithm on a given graph and finds the distances to each
// of the reachable nodes.
//
// dist must be an array with n elements and will be filled with distances to
// each node, or -1 if the node is not reachable.
void dijkstras(Graph *graph, int start, int *dist);

#endif
