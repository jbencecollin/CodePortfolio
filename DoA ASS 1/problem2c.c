// Prim's Algorithm in C

#include<stdio.h>
#include<stdbool.h> 
#include<string.h>
#include<stdlib.h>

#define INF 9999999

int main(int argc, char *argv[]){
  int radioCost, numHouses, numConnections, r, cost = 0;

// read in the three values of different formatting in document
  scanf("%d", &radioCost);
  scanf("%d", &numHouses);
  scanf("%d", &numConnections);

// calculate the cost of r for end comparison
  r = numHouses * radioCost; 

// set up variables required to make adjacency array
  int AdjArray[numHouses+1][numHouses+1], numEdges=0, visited[numHouses];
  AdjArray[numHouses][numHouses] = (int)malloc(sizeof(int)*sizeof(AdjArray));
  int tempStart, tempEnd, tempCost, x, y;
  memset(AdjArray, 0, sizeof(AdjArray));
  
// create adjacency array by reading through remaining data
  while((scanf("%d", &tempStart))!=EOF){
    scanf("%d", &tempEnd);
    scanf("%d", &tempCost);
    if (AdjArray[tempStart][tempEnd]!=0){
      if ((int)tempCost < AdjArray[tempStart][tempEnd]){
        AdjArray[tempStart][tempEnd] = (int)tempCost;
        AdjArray[tempEnd][tempStart] = (int)tempCost;
      }
    }
    else{
      AdjArray[tempStart][tempEnd] = (int)tempCost;
      AdjArray[tempEnd][tempStart] = (int)tempCost;
    }
  }

// create an array of nodes that have been 'connected'
  memset(visited, false, sizeof(visited));

// ensure we begin at the origin
  visited[0] = true;

// while not every node is connected, find the next cheapest path
  while (numEdges < numHouses) {
    int minCost = INF;
    for (int i = 0; i <= numHouses; i++) {
      if (visited[i]) {
        for (int j = 0; j <= numHouses; j++) {
          if (!visited[j] && AdjArray[i][j]) {  // not in visited and there is an edge
            if (minCost > AdjArray[i][j]) {
              minCost = AdjArray[i][j];
              x = i;
              y = j;
            }
          }
        }
      }
    }

// add the cheaper (r/c) to a running total and record that the new node has been connected
    if (radioCost<AdjArray[x][y]){
      cost += radioCost;
    }
    else {cost += AdjArray[x][y];}
    visited[y] = true;
    numEdges++;
  }

// output the cost using a mix of antennas and cables
  printf("%d\n",cost);
return 0;
}