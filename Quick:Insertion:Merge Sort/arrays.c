/*
 * This module provides functionality for generating random arrays of integers.
 *
 * Authors: Tobias Edwards <tobias.edwards@unimelb.edu.au>
 *    Date: April 2019
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "arrays.h"

// Compares two integers, for use with the qsort() function on arrays
// of integers.
int cmp_int(const void *a, const void *b);

// Reverses an array of n integers.
void reverse(int *array, int n);

// Introduce k * n random inversions.
// That is, choose i random indices to swap with either the left or right
// neighbour.
void introduce_inversions(int *array, int n, int k);

// Generates an array of n random integers from the range [0, MAX_ELT)
// according to some type.
//
// The possible types are: ARRAY_RANDOM, ARRAY_SORTED, ARRAY_REVERSED,
// ARRAY_ALMOST.
//
// The pointer to the start of the array is returned. This array needs to
// be freed manually.
int *generate_array(int n, int type) {
  int i;

  int *array = malloc(sizeof(*array) * n);
  assert(array);

  for (i = 0; i < n; i++) {
    array[i] = rand() % MAX_ELT;
  }

  if (type == ARRAY_RANDOM) {
    return array;
  } else if (type == ARRAY_SORTED) {
    qsort(array, n, sizeof(int), cmp_int);
    return array;
  } else if (type == ARRAY_REVERSED) {
    qsort(array, n, sizeof(int), cmp_int);
    reverse(array, n);
    return array;
  } else if (type == ARRAY_ALMOST) {
    qsort(array, n, sizeof(int), cmp_int);
    introduce_inversions(array, n, 10);
    return array;
  } else {
    fprintf(stderr, "Error: unrecognised type in generate_array()\n");
    exit(EXIT_FAILURE);
  }
}

// Prints out an array of integers, optionally with a label.
//
// The format will be:
//   Label = [0, 0, 0, 0]
//   -- OR --
//   [0, 0, 0, 0]
void print_array(int *array, int n, char *label) {
  int i;

  if (label != NULL) {
    printf("%s = ", label);
  }

  printf("[");
  for (i = 0; i < n; i++) {
    if (i != 0) {
      printf(", ");
    }
    printf("%d", array[i]);
  }
  printf("]\n");
}

// Compares two integers, for use with the qsort() function on arrays
// of integers.
int cmp_int(const void *a, const void *b) {
  return *((int *) a) - *((int *) b);
}

// Reverses an array of n integers.
void reverse(int *array, int n) {
  int i, tmp;

  // For each i in the first half of the array we'll swap the element
  // at i and at n - 1 - i.
  for (i = 0; 2 * i < n; i++) {
    tmp = array[i];
    array[i] = array[n - 1 - i];
    array[n - 1 - i] = tmp;
  }
}

// Introduce k * n random inversions.
// That is, choose i random indices to swap with either the left or right
// neighbour.
void introduce_inversions(int *array, int n, int k) {
  int i, idx, tmp;
  for (i = 0; i < n * k; i++) {
    // We'll swap every second element left, and the others right.
    if (i % 2 == 0) {
      // Choose from {0, ..., n - 2} then swap right.
      idx = rand() % (n - 1);
      tmp = array[idx];
      array[idx] = array[idx + 1];
      array[idx + 1] = tmp;
    } else {
      // Choose from {1, ..., n - 1} then swap left.
      idx = rand() % (n - 1) + 1;
      tmp = array[idx];
      array[idx] = array[idx - 1];
      array[idx - 1] = tmp;
    }
  }
}
