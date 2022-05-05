/*
graph.c

Set of vertices and edges implementation.

Implementations for helper functions for graph construction and manipulation.

Skeleton written by Grady Fitzpatrick for COMP20007 Assignment 1 2021
*/
#include <stdlib.h>
#include <assert.h>
#include <limits.h>
#include <string.h>
#include "graph.h"
#include "utils.h"
#include "pq.h"

#define INITIALEDGES 32
#define INF 999999

struct edge;

/* Definition of a graph. */
struct graph {
  int numVertices;
  int numEdges;
  int allocedEdges;
  struct edge **edgeList;
};

/* Definition of an edge. */
struct edge {
  int start;
  int end;
};

struct graph *newGraph(int numVertices){
  struct graph *g = (struct graph *) malloc(sizeof(struct graph));
  assert(g);
  /* Initialise edges. */
  g->numVertices = numVertices;
  g->numEdges = 0;
  g->allocedEdges = 0;
  g->edgeList = NULL;
  return g;
}

/* Adds an edge to the given graph. */
void addEdge(struct graph *g, int start, int end){
  assert(g);
  struct edge *newEdge = NULL;
  /* Check we have enough space for the new edge. */
  if((g->numEdges + 1) > g->allocedEdges){
    if(g->allocedEdges == 0){
      g->allocedEdges = INITIALEDGES;
    } else {
      (g->allocedEdges) *= 2;
    }
    g->edgeList = (struct edge **) realloc(g->edgeList,
      sizeof(struct edge *) * g->allocedEdges);
    assert(g->edgeList);
  }

  /* Create the edge */
  newEdge = (struct edge *) malloc(sizeof(struct edge));
  assert(newEdge);
  newEdge->start = start;
  newEdge->end = end;

  /* Add the edge to the list of edges. */
  g->edgeList[g->numEdges] = newEdge;
  (g->numEdges)++;
}

/* Frees all memory used by graph. */
void freeGraph(struct graph *g){
  int i;
  for(i = 0; i < g->numEdges; i++){
    free((g->edgeList)[i]);
  }
  if(g->edgeList){
    free(g->edgeList);
  }
  free(g);
}

/* Finds:
  - Number of connected subnetworks (before outage) (Task 2)
  - Number of servers in largest subnetwork (before outage) (Task 3)
  - SIDs of servers in largest subnetwork (before outage) (Task 3)
  - Diameter of largest subnetworks (after outage) (Task 4)
  - Number of servers in path with largest diameter - should be one more than
    Diameter if a path exists (after outage) (Task 4)
  - SIDs in path with largest diameter (after outage) (Task 4)
  - Number of critical servers (before outage) (Task 7)
  - SIDs of critical servers (before outage) (Task 7)
*/
struct solution *graphSolve(struct graph *g, enum problemPart part,
  int numServers, int numOutages, int *outages){
  struct solution *solution = (struct solution *)
    malloc(sizeof(struct solution));
  assert(solution);
  /* Initialise solution values */
  initaliseSolution(solution);

  /* if branch for task 2 */
  if(part == TASK_2){
    /* call function to create transitive table */
    int **trans_table = make_transitive(g, numServers);
    /* call function to calculate number of subnetworks */
    num_subnetworks(trans_table, solution, numServers);

  /* if branch for task 3 */
  } else if(part == TASK_3) {
    /* call function to create transitive table */
    int **trans_table = make_transitive(g, numServers);
    /* call function to calculate number and names of nodes in longest subnetwork */
    largest_subnetwork(trans_table, solution, numServers);

  /* if branch for task 4 */
  } else if(part == TASK_4) {
    /* call function to remove nodes of outages from graph struct */
    g = remove_outage_nodes(g, numOutages, outages);
    /* call function to create transitive table */
    int **trans_table = make_transitive(g, numServers);
    /* call function to calculate length and nodes in largest diameter of all subnetworks */
    diameter_helper(g, solution, trans_table, numServers);

  /* if branch for task 7 */
  } else if(part == TASK_7) {
    // no clue how to implement this part. forgive me coding gods. 
  }
  return solution;
}

/* alter the network graph to account for outages */
struct graph *remove_outage_nodes(struct graph *g, int numOutages, int *outages){
  int i, j;
/* iterate through every possible path between nodes */
  for(i = 0; i < numOutages; i++){
    for(j = 0; j < g->numEdges; j++){
      /* remove the edges if they involve the outage nodes */
      if((g->edgeList[j]->start == outages[i])||(g->edgeList[j]->end == outages[i])){
        g->edgeList[j]->start = 0;
        g->edgeList[j]->end = 0;
      }
    }
  }
  return g;
}

/* calculates the longest shortest route present within graph with outages removed */
void diameter_helper(struct graph *g, struct solution *solution, int **trans_table, int numServers){
  int **floyd_table = make_floyd(g, numServers);
  int longest_subnet = 0, max_row = 0, index_count = 0;
  /* iterate through every possible path between nodes */
  for(int row=0; row<numServers; row++){
    for(int column=0; column<numServers; column++){
      /* record the row index of the transitive table containing the largest diameter and its length*/
      if(floyd_table[row][column]>longest_subnet&&floyd_table[row][column]!=INF){
        solution->postOutageDiameterCount = 1;
        longest_subnet = floyd_table[row][column];
        max_row = row;
      }
      /* increment the tally of largest diameter count if two match lengths */
      else if(floyd_table[row][column]==longest_subnet){
        solution->postOutageDiameterCount++;
      }
    }
  }
  /* allocate memory for an array storing nodes in longest diameter */
  int *largest_diameter_nodes;
  largest_diameter_nodes = (int *)malloc(sizeof(int)*numServers);
  memset(largest_diameter_nodes, 0, numServers);
  for(int column=0; column<numServers; column++){
    if(trans_table[max_row][column]==1){
      largest_diameter_nodes[index_count] = column;
      index_count++;
    }
  }
  /* assign solution as required */
  solution->postOutageDiameter = longest_subnet;
  solution->postOutageDiameterSIDs = largest_diameter_nodes;
  return;
}

/* helper function to find length of, and nodes included in the longest subnetwork */
void largest_subnetwork(int **trans_table, struct solution *solution, int numServers){
  int len_subnetwork = 0, largest_subnet = 0, row_total = 0, index_count = 0;
  /* iterate through every possible path between nodes */
  for(int row=0; row<numServers; row++){
    len_subnetwork = 0;
    /* calculate and record length of subnetwork */
    for(int column=0; column<numServers; column++){
      if(trans_table[row][column] == 1){
        len_subnetwork++;
      }
    }
    /* compare current subnetwork length with greatest recorded */
    if(len_subnetwork > largest_subnet){
      largest_subnet = len_subnetwork;
    }
  }
  /* allocate memory to store nodes in largest subnetwork */
  solution->largestSubnet = largest_subnet;
  int *largest_subnet_nodes;
  largest_subnet_nodes = (int *)malloc(largest_subnet*sizeof(int));
  /* iterate through every possible path between nodes */
  for(int row=0; row<numServers; row++){
    row_total = 0;
    for(int column=0; column<=numServers; column++){
      if(trans_table[row][column]==1){
        /* tally nodes in current subnetwork */
        row_total++;;
      }
    }
    /* ensure we are storing values of subnetwork with largest length then store */
    if(row_total==solution->largestSubnet){
      for(int column=0; column<numServers; column++){
        if(trans_table[row][column]==1){
          largest_subnet_nodes[index_count] = column;
          index_count++;
        }
      }
      /* assign values as required */
      solution->largestSubnetSIDs = largest_subnet_nodes;
      return;
    }
  }
}

/* finds the number of subnetworks in supplied network */
int num_subnetworks(int **trans_table, struct solution *solution, int numServers){
  int count = 0;
  /* iterate through every possible path between nodes */
  for(int row=0; row<numServers; row++){
    int status=0;
    for(int i=0; i<row; i++){
      status=1;
      /* check if both columns match */ 
      for(int column=0; column<=numServers; column++){
        if(trans_table[row][column]!=trans_table[i][column]){
          status=0;
        }
        if(status==1){
          break;
        }
      }
    }
    /* if no match is found, increment counter */
    if(status==0){
      count += 1;
    }
  }
  /* assign values as required */ 
  solution->connectedSubnets = count;
  return count;
}

/* apply Worshall's algorithm to derive transitive table */
int **make_transitive(struct graph *g, int numServers){
  int **trans_table, k, i, j, edge;
  trans_table = malloc(sizeof(int*) * numServers);   
  /* allocate memory for the transitive table */ 
  for(i = 0; i < numServers; i++) {
    trans_table[i] = malloc(sizeof(int*) * numServers);
  }
  /* set the values of the array to be 0 */ 
  for (k = 0; k < numServers; k++){
    for (i = 0; i < numServers; i++){
      trans_table[k][i] = 0;
    }
  }
  /* enter value of 1 into array for routes that exist */ 
  for (edge = 0; edge < g->numEdges; edge++){
    trans_table[g->edgeList[edge]->end][g->edgeList[edge]->start] = 1;
    trans_table[g->edgeList[edge]->start][g->edgeList[edge]->end] = 1;
  }
  /* check if nodes can be connected via other nodes */ 
  for (k = 0; k < numServers; k++){
    for (i = 0; i < numServers; i++){
      for (j = 0; j < numServers; j++){
        if (trans_table[i][k] && trans_table[k][j]){
          trans_table[i][j] = 1;
        }
      }
    }
  }
  return trans_table;
}

/* apply Flloyd's algorithm to derive (cost inclusive) transitive table */
int **make_floyd(struct graph *g, int numServers){
  int **floyd_table, k, i, j, edge;
  floyd_table = malloc(sizeof(int*) * numServers);  
  /* allocate memory for the cost inclusive transitive table */  
  for(i = 0; i < numServers; i++) {
    floyd_table[i] = malloc(sizeof(int*) * numServers);
  }
  /* set the values of the array to be INF */ 
  for (k = 0; k < numServers; k++){
    for (i = 0; i < numServers; i++){
      floyd_table[k][i] = INF;
    }
  }
  /* enter value of 1 into array for routes that exist */
  for (edge = 0; edge < g->numEdges; edge++){
    floyd_table[g->edgeList[edge]->end][g->edgeList[edge]->start] = 1;
    floyd_table[g->edgeList[edge]->start][g->edgeList[edge]->end] = 1;
  }
  /* enter value of 0 into array for node routes to itself */
  for (k = 0; k < numServers; k++){
    for (i = 0; i < numServers; i++){
      if(i == k){floyd_table[k][i]=0;}
    }
  }
  /* check if nodes can be connected via other nodes and if so, tally cost */
  for (k = 0; k < numServers; k++){
    for (i = 0; i < numServers; i++){
      for (j = 0; j < numServers; j++){
        if ((floyd_table[i][k] != INF) && (floyd_table[k][j] != INF) 
        && floyd_table[i][j] > (floyd_table[i][k] + floyd_table[k][j])){
          floyd_table[i][j] = floyd_table[i][k] + floyd_table[k][j];
        }
      }
    }
  }
  return floyd_table;
}