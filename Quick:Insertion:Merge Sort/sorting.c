/*
 * Sorting functionality for Lab 9.
 *
 * Authors: Tobias Edwards <tobias.edwards@unimelb.edu.au>
 *          Grady Fitzpatrick <grady.fitzpatrick@unimelb.edu.au>
 *    Date: April 2019
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "arrays.h"
#include "sorting.h"

int global_partitions = 0;

// ================= Function Prototypes for Helper Functions =================

// Naively paritions an array on pivot value given by pivot.
//
// This function will allocate a new array rather than partitioning in place,
// and requires 3 iterations of the array to partition, and then 1 to copy the
// result back to the input array.
//
// This is NOT the best we can do.
//
// [[ STUDENT TASK ]]
// Write a better version of this function.
//
// Use the time_function() function provided to determine what effect this will
// have.
int naive_partition_on_pivot(int *array, int n, int pivot);

// 1a - lomuto partitioning
int lomuto_partition_on_pivot(int *array, int n, int pivot);
// 1b - Hoare partitioning
int hoare_partition_on_pivot(int *array, int n, int pivot);

// ========================= Function Implementations =========================

// Iteratively insertion sorts an array of n integers in ascending order.
void insertion_sort(int *array, int n) {
  // i will be the number of elements at the start of the array which are
  // already sorted, j will be used to find the index in which the next element
  // should be inserted.
  int i, j, next;

  // Initially, A[0] is sorted as it's just one element. Thus we start at i = 1.
  for (i = 1; i < n; i++) {
    next = array[i];
    // Search for the index where we should insert next. Note that this is
    // better than having to perform swaps, as we don't insert next until we've
    // found where it should be inserted.
    for (j = i - 1; j >= 0 && array[j] > next; j--) {
      // Move the element to the right.
      array[j + 1] = array[j];
    }
    // Insert the next element to (j + 1), as the for loop will have
    // decremented it one too many positions.
    array[j + 1] = next;
  }
}

// Quicksorts a given array of n integers in ascending order.
//
// Uses the provided partition function. The pivot selection strategy should
// be built into the partition function. The partition function should return
// the index of the pivot after partitioning.
void quicksort(int *array, int n, int (*partition)(int *array, int n)) {
  int pivot_idx;

  // If n is 0 or 1 then array must already be sorted.
  if (n == 0 || n == 1) {
    return;
  }

  global_partitions++;
  pivot_idx = partition(array, n);

  // The two sections of the array to be sorted are now:
  // [0..pivot_idx - 1] and [pivot_idx + 1..n-1].
  quicksort(array, pivot_idx, partition);
  quicksort(array + pivot_idx + 1, n - (pivot_idx + 1), partition);
}

// Partitions an array using the first element as the pivot.
//
// Returns the index of the first element with the same value as the pivot.
int partition_first_pivot(int *array, int n) {
  int pivot, pivot_idx;
  assert(n > 0);

  // We're just selecting the first element to be the pivot.
  pivot = array[0];
  // pivot_idx = naive_partition_on_pivot(array, n, pivot);
  // pivot_idx = lomuto_partition_on_pivot(array, n, pivot);
  pivot_idx = hoare_partition_on_pivot(array, n, pivot);

  return pivot_idx;
}

// Partitions an array using a random element as the pivot.
//
// Returns the index of the first element with the same value as the pivot.
int partition_random_pivot(int *array, int n) {
  int pivot, pivot_idx;
  assert(n > 0);

  pivot = array[rand() % n];
  // pivot_idx = naive_partition_on_pivot(array, n, pivot);
  // pivot_idx = lomuto_partition_on_pivot(array, n, pivot);
  pivot_idx = hoare_partition_on_pivot(array, n, pivot);

  return pivot_idx;
}

int partition_median_of_three(int *array, int n) {
  int pivot_idx;
  assert(n > 0);

  int pivot_l = array[0];
  int pivot_m = array[n / 2];
  int pivot_r = array[n - 1];

  /* Insertion Sort 3 values. */
  int temp;
  if(pivot_l > pivot_m){
    temp = pivot_l;
    pivot_l = pivot_m;
    pivot_m = temp;
  }
  if(pivot_m > pivot_r){
    temp = pivot_m;
    pivot_m = pivot_r;
    pivot_r = temp;
    if(pivot_l > pivot_m){
      temp = pivot_l;
      pivot_l = pivot_m;
      pivot_m = temp;
    }
  }
  // pivot_idx = naive_partition_on_pivot(array, n, pivot);
  // pivot_idx = lomuto_partition_on_pivot(array, n, pivot);
  pivot_idx = hoare_partition_on_pivot(array, n, pivot_m);

  return pivot_idx;
}

// Naively paritions an array on pivot value given by pivot.
//
// This function will allocate a new array rather than partitioning in place,
// and requires 3 iterations of the array to partition, and then 1 to copy the
// result back to the input array.
//
// This is NOT the best we can do.
//
// [[ STUDENT TASK ]]
// Write a better version of this function.
//
// Use the time_function() function provided to determine what effect this will
// have.
int naive_partition_on_pivot(int *array, int n, int pivot) {
  // We'll use the tmp array to build up the partitioned result.
  int *tmp;
  // i will indicate our position in the original array, and j will indicate
  // the position in tmp.
  int i, j;
  int pivot_idx;

  tmp = malloc(sizeof(*tmp) * n);
  assert(tmp);
  // We haven't inserted anything into tmp yet, so j = 0;
  j = 0;

  // First, insert all elements less than pivot into tmp.
  for (i = 0; i < n; i++) {
    if (array[i] < pivot) {
      tmp[j++] = array[i];
    }
  }

  // Next element from here in tmp will be the pivot.
  pivot_idx = j;

  // Now, insert all the elements which are of equal value to the pivot
  // into tmp.
  for (i = 0; i < n; i++) {
    if (array[i] == pivot) {
      tmp[j++] = array[i];
    }
  }

  // Finally, insert all elements greater than the pivot into the tmp array.
  for (i = 0; i < n; i++) {
    if (array[i] > pivot) {
      tmp[j++] = array[i];
    }
  }

  // At this point we should have inserted n elements into tmp.
  assert(j == n);

  // Now all is left is to copy over all the elements from tmp to array
  // and free the tmp array
  for (i = 0; i < n; i++) {
    array[i] = tmp[i];
  }
  free(tmp);

  return pivot_idx;
}

/*
In-place partitioning using Lomuto Partitioning
*/
int lomuto_partition_on_pivot(int *array, int n, int pivot) {
  // i will indicate our position in the original array, and j will indicate
  // the position in tmp.
  int i;//, j;
  int pivot_idx;

  /* Smaller values start off at pivot. */
  int s = 0;

  /* Find pivot */
  for(i = 0; i < n; i++){
    if (array[i] == pivot){
      /* Found pivot */
      /* swap pivot into leftmost location */
      array[i] = array[s];
      array[s] = pivot;
      break;
    }
  }

  /* Lomuto */
  int tmp;
  for(i = 1; i < n; i++){
    if(array[i] < pivot){
      s = s + 1;
      /* Swap element s and element i */
      tmp = array[s];
      array[s] = array[i];
      array[i] = tmp;
    }
  }

  /* Swap partition into last smallest value */
  array[0] = array[s];
  array[s] = pivot;

  pivot_idx = s;

  return pivot_idx;
}

/*
In-place partitioning using Hoare Partitioning
*/
int hoare_partition_on_pivot(int *array, int n, int pivot) {
  // i will indicate our position in the original array, and j will indicate
  // the position in tmp.
  int lt, gt;
  int i;
  int pivot_idx;

  /* Smaller values start off at pivot. */
  lt = 0;
  /* Initially don't know whether values are  */
  gt = n;

  /* Find pivot */
  for(i = 0; i < n; i++){
    if (array[i] == pivot){
      /* Found pivot */
      /* swap pivot into leftmost location */
      array[i] = array[lt];
      array[lt] = pivot;
      break;
    }
  }

  /* Hoare */
  int tmp;
  /*
    Keep going until less than pointer crosses greater than pointer - if that
    occurs, finding a value greater than the pivot at the less than pointer no
    longer indicates an element on the wrong side of the array.
  */
  while(lt < gt){
    /* Find next value greater than the pivot */
    lt++;
    while(lt < n && array[lt] <= pivot){
      lt++;
    }
    /* Find next value less than the pivot */
    gt--;
    while(gt > 0 && array[gt] >= pivot){
      gt--;
    }
    if(lt < gt){
      tmp = array[gt];
      array[gt] = array[lt];
      array[lt] = tmp;
    }
  }

  /*
    Since pivot is in 0th index, we need to swap it into the pointer which
    will be pointing to the <= values after the completion of the rest of the
    partitioning, i.e. the greater than pointer.
  */
  array[0] = array[gt];
  array[gt] = pivot;

  pivot_idx = gt;

  return pivot_idx;
}

void hybrid_sort(int *array, int n){
  if(n < 30){
    insertion_sort(array, n);
  } else {
    quicksort(array, n, partition_random_pivot);
  }
}

void merge_sort(int *array, int n){
  int sortedSize = 1;
  int startFirst;
  int startSecond;
  int i, j, k;
  /* Space to build array in */
  int *buildSpace = (int *) malloc(sizeof(int) * n);
  assert(buildSpace);

  while(sortedSize < n){
    /* Use two variables to simplify non-power-of-2 inputs */
    startFirst = 0;
    startSecond = sortedSize;
    while(startSecond < n){
      /* Merge lists. */
      i = j = k = 0;
      while(i < sortedSize && j < sortedSize && (startSecond + j) < n){
        /* <= required for stability. < alone won't do. */
        if(array[startFirst + i] <= array[startSecond + j]){
          buildSpace[k] = array[startFirst + i];
          i++;
        } else {
          buildSpace[k] = array[startSecond + j];
          j++;
        }
        k++;
      }
      /* Finish any non-comparative additions */
      while(i < sortedSize){
        buildSpace[k] = array[startFirst + i];
        i++;
        k++;
      }
      while(j < sortedSize && (startSecond + j) < n){
        buildSpace[k] = array[startFirst + i];
        j++;
        k++;
      }
      /* Copy temporary space back in to original array */
      /* Note: We can skip this step if we alternate the array we're sorting
        every step instead - but this adds complexity to the logic. */
      for(i = 0; i < k; i++){
        array[startFirst + i] = buildSpace[i];
      }
      /* Move to next pair. */
      startFirst += sortedSize * 2;
      startSecond += sortedSize * 2;
    }

    /* After loop finishes, sorted lists are twice as long */
    sortedSize *= 2;
  }

  if(buildSpace){
    free(buildSpace);
  }
}
