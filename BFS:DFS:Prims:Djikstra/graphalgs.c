/* * * * * * *
 * Module containing various graph algorithms.
 *
 * created for COMP20007 Design of Algorithms 2020
 * by Tobias Edwards <tobias.edwards@unimelb.edu.au>
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "list.h"
#include "priorityqueue.h"
#include "graph.h"
#include "graphalgs.h"

#define INFTY -1
#define NO_PREV -1

// ----- Prototypes for non-exposed functions -----

// Recursive explore function which explores from node u in the graph.
// order and visited are arrays of length n_vertices, n_visited is a pointer
// to the number of nodes which have already been visited.
//
// order[i] == k means that vertex k was visited ith in the order, while
// visited[i] == true means that node i has been visited
void dfs_explore(Graph *graph, int u, int *order, bool *visited, int *n_visited);

// Iterative explore function which explores from node u in the graph.
// order and visited are arrays of length n_vertices, n_visited is a pointer
// to the number of nodes which have already been visited.
//
// order[i] == k means that vertex k was visited ith in the order, while
// visited[i] == true means that node i has been visited
void bfs_explore(Graph *graph, int u, int *order, bool *visited, int *n_visited);

// ----- Function implementations -----

// Runs a depth first search on the given graph, returning a dynamically
// allocated array of integers representing the order in which the DFS
// visits the nodes in the graph.
//
// The resultant array will be of size n_vertices and must be freed after use.
int *dfs(Graph *graph) {
  int n = graph_num_vertices(graph);
  int *order = malloc(sizeof(int) * n);
  assert(order);
  // Use calloc to allocate and set all memory to 0
  bool *visited = calloc(n, sizeof(bool));
  assert(visited);

  int n_visited = 0;

  for (int u = 0; u < n; u++) {
    if (!visited[u]) {
      dfs_explore(graph, u, order, visited, &n_visited);
    }
  }

  free(visited);
  return order;
}

// Recursive explore function which explores from node u in the graph.
// order and visited are arrays of length n_vertices, n_visited is a pointer
// to the number of nodes which have already been visited.
//
// order[i] == k means that vertex k was visited ith in the order, while
// visited[i] == true means that node i has been visited
void dfs_explore(Graph *graph, int u, int *order, bool *visited, int *n_visited) {
  visited[u] = true;
  order[*n_visited] = u;
  (*n_visited)++;

  // Create an array to hold the neighbors of u
  int n_neighbours = graph_out_degree(graph, u);
  int *neighbours = malloc(sizeof(int) * n_neighbours);
  // Retrieve these neighbours from the graph
  graph_get_neighbours(graph, u, neighbours, NULL, n_neighbours);

  int v;
  for (int i = 0; i < n_neighbours; i++) {
    v = neighbours[i];
    if (!visited[v]) {
      dfs_explore(graph, v, order, visited, n_visited);
    }
  }

  free(neighbours);
}

// Runs a breadth first search on the given graph, returning a dynamically
// allocated array of integers representing the order in which the DFS
// visits the nodes in the graph.
//
// The resultant array will be of size n_vertices and must be freed after use.
int *bfs(Graph *graph) {
  int n = graph_num_vertices(graph);
  int *order = malloc(sizeof(int) * n);
  assert(order);
  // Use calloc to allocate and set all memory to 0
  bool *visited = calloc(n, sizeof(bool));
  assert(visited);

  int n_visited = 0;

  for (int u = 0; u < n; u++) {
    if (!visited[u]) {
      bfs_explore(graph, u, order, visited, &n_visited);
    }
  }

  free(visited);
  return order;
}

// Iterative explore function which explores from node u in the graph.
// order and visited are arrays of length n_vertices, n_visited is a pointer
// to the number of nodes which have already been visited.
//
// order[i] == k means that vertex k was visited ith in the order, while
// visited[i] == true means that node i has been visited
void bfs_explore(Graph *graph, int start, int *order, bool *visited, int *n_visited) {
  List *queue = new_list();
  list_add_end(queue, start);

  int node;
  while (!list_is_empty(queue)) {
    node = list_remove_start(queue);
    if (visited[node]) continue;
    visited[node] = true;
    order[*n_visited] = node;
    (*n_visited)++;

    // Create an array to hold the neighbors of u
    int n_neighbours = graph_out_degree(graph, node);
    int *neighbours = malloc(sizeof(int) * n_neighbours);
    // Retrieve these neighbours from the graph
    graph_get_neighbours(graph, node, neighbours, NULL, n_neighbours);

    int next;
    for (int i = 0; i < n_neighbours; i++) {
      next = neighbours[i];
      if (!visited[next]) {
        list_add_end(queue, next);
      }
    }

    free(neighbours);
    neighbours = NULL;
  }

  free_list(queue);
  queue = NULL;
}

// Runs Prim's algorithm on a given graph and stores the edges in the
// arrays from and to (such that each from[i], to[i] pair forms an edge
// in the minimium spanning tree).
//
// from and to should already be malloc'd and have length n - 1.
//
// Returns whether or not the algorithm was succesful.
bool prims(Graph *graph, int *from, int *to) {
  // Note that this algorithm is longer than it should be and should be
  // split into smaller functions if this was an assessable task.

  // edges added to the tree so far
  int n = graph_num_vertices(graph);
  int edges_added = 0;

  // Initialise a cost array to store the current cost to each node.
  int *cost = malloc(n * sizeof(int));
  // Initialise an array storing the node at which the min-cost edge to each
  // edge comes from.
  int *prev = malloc(n * sizeof(int));
  // Initialise an array of whether each node has been explored so we don't
  // keep updating nodes which are already a part of the mst.
  bool *explored = malloc(n * sizeof(int));
  for (int i = 0; i < n; i++) {
    cost[i] = INFTY;
    prev[i] = NO_PREV;
    explored[i] = false;
  }
  PriorityQueue *p_queue = new_priority_queue();

  // Let's arbitrarily select node 0 to start with.
  cost[0] = 0;
  priority_queue_insert(p_queue, 0, cost[0]);

  while (!priority_queue_is_empty(p_queue)) {
    int node = priority_queue_remove_min(p_queue);
    explored[node] = true;
    // When we remove a node from the priority queue we add the min-cost
    // edge so far to this node to the minimum spanning tree by adding
    // the edge to the (from, to) arrays.
    if (prev[node] != NO_PREV) {
      from[edges_added] = prev[node];
      to[edges_added] = node;
      edges_added++;
    }

    // Create an array to hold the neighbors of u
    int n_neighbours = graph_out_degree(graph, node);
    int *neighbours = malloc(sizeof(int) * n_neighbours);
    int *weights = malloc(sizeof(int) * n_neighbours);
    // Retrieve these neighbours from the graph
    graph_get_neighbours(graph, node, neighbours, weights, n_neighbours);
    for (int i = 0; i < n_neighbours; i++) {
      int neighbour = neighbours[i];
      if (explored[neighbour]) continue;
      int weight = weights[i];
      if (cost[neighbour] == INFTY) {
        printf("Found %d from %d (%d)\n", neighbour, node, weight);
        cost[neighbour] = weight;
        prev[neighbour] = node;
        priority_queue_insert(p_queue, neighbour, weight);
      } else if (cost[neighbour] > weight) {
        printf("Updating %d from %d (%d)\n", neighbour, node, weight);
        cost[neighbour] = weight;
        prev[neighbour] = node;
        priority_queue_update(p_queue, neighbour, weight);
      }
    }

    free(neighbours);
    free(weights);
  }

  free_priority_queue(p_queue);
  free(cost);
  free(prev);
  free(explored);

  if (edges_added == n - 1) {
    return true;
  } else {
    // If the mst is not connected (and thus not spanning).
    return false;
  }
}

// Run Dijkstra's algorithm on a given graph and finds the distances to each
// of the reachable nodes.
//
// dist must be an array with n elements and will be filled with distances to
// each node, or -1 if the node is not reachable.
void dijkstras(Graph *graph, int start, int *dist) {
  int n = graph_num_vertices(graph);
  // Initialise an array of whether each node has been explored so we don't
  // keep updating nodes which have already been explored.
  bool *explored = malloc(n * sizeof(int));

  for (int i = 0; i < n; i++) {
    dist[i] = INFTY;
    explored[i] = false;
  }
  PriorityQueue *p_queue = new_priority_queue();

  // We start at the given starting point
  dist[start] = 0;
  priority_queue_insert(p_queue, start, dist[start]);

  while (!priority_queue_is_empty(p_queue)) {
    int node = priority_queue_remove_min(p_queue);
    explored[node] = true;

    // Create an array to hold the neighbors of u
    int n_neighbours = graph_out_degree(graph, node);
    int *neighbours = malloc(sizeof(int) * n_neighbours);
    int *weights = malloc(sizeof(int) * n_neighbours);

    // Retrieve these neighbours from the graph
    graph_get_neighbours(graph, node, neighbours, weights, n_neighbours);
    for (int i = 0; i < n_neighbours; i++) {
      int neighbour = neighbours[i];
      if (explored[neighbour]) continue;
      int new_cost = dist[node] + weights[i];
      if (dist[neighbour] == INFTY) {
        printf("Found %d from %d (%d)\n", neighbour, node, new_cost);
        dist[neighbour] = new_cost;
        priority_queue_insert(p_queue, neighbour, new_cost);
      } else if (dist[neighbour] > new_cost) {
        printf("Updating %d from %d (%d)\n", neighbour, node, new_cost);
        dist[neighbour] = new_cost;
        priority_queue_update(p_queue, neighbour, new_cost);
      }
    }

    free(neighbours);
    free(weights);
  }

  free_priority_queue(p_queue);
  free(explored);
}
