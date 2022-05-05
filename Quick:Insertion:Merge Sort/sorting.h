/*
 * Sorting functionality for Lab 9.
 *
 * Authors: Tobias Edwards <tobias.edwards@unimelb.edu.au>
 *          Grady Fitzpatrick <grady.fitzpatrick@unimelb.edu.au>
 *    Date: April 2019
 */

#ifndef SORTING_H
#define SORTING_H

extern int global_partitions;

// Iteratively insertion sorts an array of n integers in ascending order.
void insertion_sort(int *array, int n);

// Quicksorts a given array of n integers in ascending order.
//
// Uses the provided partition function. The pivot selection strategy should
// be built into the partition function. The partition function should return
// the index of the pivot after partitioning.
void quicksort(int *array, int n, int (*partition)(int *array, int n));

// Partitions an array using the first element as the pivot.
//
// Returns the index of the first element with the same value as the pivot.
int partition_first_pivot(int *array, int n);

// Partitions an array using a random element as the pivot.
//
// Returns the index of the first element with the same value as the pivot.
int partition_random_pivot(int *array, int n);

// Partitions an array by looking at the first, middle and last element and
// the middle value as the pivot.
//
// Returns the index of the first element with the same value as the pivot.
int partition_median_of_three(int *array, int n);

// Sorts input based on the input size
//
void hybrid_sort(int *array, int n);

// Bottom-up merge sort the given array (iterative).
void merge_sort(int *array, int n);

#endif
