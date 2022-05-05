/*
 * This module provides functionality for generating random arrays of integers.
 *
 * Authors: Tobias Edwards <tobias.edwards@unimelb.edu.au>
 *    Date: April 2019
 */

#define MAX_ELT 1000

#define ARRAY_RANDOM 1
#define ARRAY_SORTED 2
#define ARRAY_REVERSED 3
#define ARRAY_ALMOST 4

// Generates an array of n random integers from the range [0, MAX_ELT)
// according to some type.
//
// The possible types are: ARRAY_RANDOM, ARRAY_SORTED, ARRAY_REVERSED,
// ARRAY_ALMOST.
//
// The pointer to the start of the array is returned. This array needs to
// be freed manually.
int *generate_array(int n, int type);

// Prints out an array of integers, optionally with a label.
//
// The format will be:
//   Label = [0, 0, 0, 0]
//   -- OR --
//   [0, 0, 0, 0]
void print_array(int *array, int n, char *label);
