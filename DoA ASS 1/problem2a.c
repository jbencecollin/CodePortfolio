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
  int numEdges=0, visited[numHouses], tempStart, tempEnd, tempCost, x, y;
  int AdjArray[numHouses][numHouses];
  AdjArray[numHouses][numHouses] = (int)malloc(sizeof(int)*sizeof(AdjArray));
  memset(AdjArray, 0, sizeof(AdjArray));

// create adjacency array by reading through remaining data
  while((scanf("%d", &tempStart))!=EOF){
    scanf("%d", &tempEnd);
    scanf("%d", &tempCost);
    if (AdjArray[tempStart][tempEnd] != 0){
     if ((int)tempCost < AdjArray[tempStart][tempEnd]){
        AdjArray[tempStart][tempEnd] = (int)tempCost;
        AdjArray[tempEnd][tempStart] = (int)tempCost;
      }
    }
    else if (AdjArray[tempStart][tempEnd] == 0){
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
    for (int i = 0; i < numHouses; i++) {
      if (visited[i]) {
        for (int j = 0; j < numHouses; j++) {
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

// add the cheapest path cost to a running total and record that the new node has been connected
    cost += AdjArray[x][y];
    visited[y] = true;
    numEdges++;
  }

// make the final comparison to output the cheapest alternative
  if(cost>r){printf("r\n");}
  else if(r>cost){printf("c\n");}
  else{printf("b\n");}
return 0;
}