#include <iostream>
#include <stdio.h>
#include <type_traits>
using namespace std;
#include <limits.h>
double findMedianSortedArrays(int a[], int al, int b[], int bl) {
	// todo
  int total_nums = al + bl;
  if (total_nums == 0) {
    // error
  } else if (total_nums == 1) {
    // whichever a or b has elems
  }
  if ((total_nums % 2) == 0) {
    // even
    // median = average of two middle numbers
  } else {
    // odd
    // median = the middle number
  }

  int a_index = 0;
  int b_index = 0;

  // iterate both together, whichever is less increase that index
  printf("\ntotal_nums = %d, running iteration %d times", total_nums, (total_nums/2 - 1));
  for (int i = 0; i < (total_nums/2 - 1); i++) {  // it will actually stop at total_nums/2
    printf("\niteration [%d], a_index [%d], b_index [%d]", i, a_index, b_index);

    if ((a_index < al) && (b_index < bl)) {
      // elems remaining in both
      if (a[a_index] <= b[b_index]) {
        printf("\na_index++");
        a_index++; // move a_index fwd
      } else {
        printf("\nb_index++");
        b_index++; // move b_index fwd
      }
    } else if (a_index == al) { // a is finished
        printf("\n a is finished, hence b_index++");
        b_index++;
    } else {
      // b is finished
        printf("\n b is finished, hence a_index++");
      a_index++;
    }
  }

  printf("\nend of loop: a_index %d, b_index %d", a_index, b_index);
  float result = -1;

  if ((total_nums % 2) == 0) {
    // even
    // median = average of two middle numbers
    // Correction can be made.
    // so now we have a_index. b_index. 
    // For average, one input is min(a[a_index],b[b_index])
    //              other input is min(max(a[a_index],b[b_index]), a[a_index+1], b[b_index+1])
    
    // a_index+1 and b_index+1 
    int ave_input_1 = -1;
    int ave_input_2 = -1;
    if (a_index == al) { // a finished
        ave_input_1 = b[b_index];
        ave_input_2 = b[b_index + 1];
    } else if (b_index == bl) { // b is finished
        ave_input_1 = a[a_index];
        ave_input_2 = a[a_index + 1];  
    } else {
        // none is finished
        ave_input_1 = min(a[a_index],b[b_index]);
        ave_input_2 = min(
            max(a[a_index],b[b_index]),
            min(
                (a_index + 1 == al)? INT_MAX: b[b_index + 1],
                (b_index + 1 == bl)? INT_MAX: a[a_index + 1]
               )
            );
    }
    printf("\n");
    float average = ((float)ave_input_1 + (float)ave_input_2) / 2;
    
    printf("\npicking combined median from a and b = ave(%d, %d) = %f", ave_input_1, ave_input_2, average);
    result = average;
  } else {
    // odd
    // median = the middle number
    if (a_index == al) {
      // a is finished
      printf("\npicking combined median from b as %d\n\n", b[b_index + 1]);    
      result = b[b_index + 1];
    } else if (b_index == bl) {
      // b is finished
      printf("\npicking combined median from a as %d\n\n", a[a_index + 1]);    
      result = a[a_index + 1];
    } else if ((a[a_index] > b[b_index])) {
      printf("\npicking combined median from a as %d\n\n", a[a_index]);
      result = (float)a[a_index];
    } else {
      printf("\npicking combined median from b as %d\n\n", b[b_index]);
      result = (float)b[b_index];
    }
  }

	return result;
}

/**
* int doTestsPass()
* Returns 1 if all tests pass. Otherwise returns 0.
*/
int doTestsPass() {
  // todo: implement more tests, please
  // feel free to make testing more elegant
  int result = 1;

  int a[] = {1, 3, 5, 7};
  int b[] = {2, 4, 6};

  int c[] = {};
  int d[] = {1,2,3};

  int e[] = {1,2,3,4};
  int f[] = {5,6};

  int al = sizeof(a) / sizeof(*a);
  int bl = sizeof(b) / sizeof(*b);
  int cl = sizeof(c) / sizeof(*c);
  int dl = sizeof(d) / sizeof(*d);
  int el = sizeof(e) / sizeof(*c);
  int fl = sizeof(f) / sizeof(*f);

  result &= findMedianSortedArrays(a, al, b, bl) == 4.0;
  result &= findMedianSortedArrays(c, cl, d, dl) == 2.0;
  result &= findMedianSortedArrays(e, el, f, fl) == 3.5;

  return result;
}

/**
* Execution entry point.
*/
int main() {
	if(doTestsPass())
	{
		printf("All tests pass\n");
	}
	else
	{
		printf("There are test failures\n");
	}

	return 0;
}

