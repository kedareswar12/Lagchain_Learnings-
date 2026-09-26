#include <iostream>

/*
 * pointers.cpp
 *
 * This file provides a brief tutorial on pointers in C++ and demonstrates
 * pointer arithmetic. It is intended for educational purposes and can be
 * compiled with any standard‑conforming C++ compiler (e.g., g++ -std=c++17).
 *
 * What is a pointer?
 * -------------------
 * A pointer is a variable that stores the memory address of another object.
 * The type of a pointer indicates the type of the object it points to. For
 * example, `int *p` is a pointer to an `int`.
 *
 * Basic operations:
 *   - Declaration:   T *ptr;            // ptr can hold address of a T
 *   - Assignment:    ptr = &var;         // store address of var in ptr
 *   - Dereference:   *ptr = 42;          // read/write the value pointed to
 *   - Address‑of:    &var                // yields the address of var
 *
 * Pointer arithmetic
 * -------------------
 * When a pointer points into an array (or any contiguous block of memory), it
 * can be incremented, decremented, or offset by an integer. The arithmetic is
 * performed in units of the pointed‑to type, not raw bytes. The compiler
 * automatically scales the integer by `sizeof(T)`.
 *
 *   int arr[5] = {10, 20, 30, 40, 50};
 *   int *p = arr;            // points to arr[0]
 *   ++p;                     // now points to arr[1]
 *   p = p + 2;               // points to arr[3]
 *   std::cout << *p;         // prints 40
 *
 * The following operations are defined for pointers to elements of the same
 * array (or one past the last element):
 *   - p + n   : points n elements forward
 *   - p - n   : points n elements backward
 *   - p1 - p2 : distance (number of elements) between two pointers
 *   - ++p / --p, p++, p-- : move by one element
 *
 * Important rules:
 *   1. Pointer arithmetic is only valid within the bounds of a single array.
 *      Accessing memory outside those bounds results in undefined behavior.
 *   2. Adding/subtracting a pointer and an integer yields another pointer of
 *      the same type.
 *   3. Subtracting two pointers of the same type yields a signed integer of
 *      type `ptrdiff_t` (defined in <cstddef>), representing the element count.
 *   4. The expression `&arr[0] + n` is equivalent to `arr + n`.
 *
 * Example program
 * ----------------
 * The `main` function below demonstrates declaration, dereferencing, and
 * pointer arithmetic with an integer array.
 */

int main() {
    // Declare and initialise an array of five integers
    int numbers[5] = {10, 20, 30, 40, 50};

    // Pointer to the first element of the array
    int *ptr = numbers; // same as &numbers[0]

    std::cout << "Initial pointer points to: " << *ptr << "
"; // 10

    // Move the pointer forward by two elements (pointer arithmetic)
    ptr = ptr + 2; // now points to numbers[2]
    std::cout << "After ptr + 2, points to: " << *ptr << "
"; // 30

    // Increment the pointer (equivalent to ptr = ptr + 1)
    ++ptr; // now points to numbers[3]
    std::cout << "After ++ptr, points to: " << *ptr << "
"; // 40

    // Demonstrate pointer subtraction: distance between two pointers
    int *start = numbers; // points to numbers[0]
    std::ptrdiff_t distance = ptr - start; // number of elements between them
    std::cout << "Distance from start to current ptr: " << distance << " elements
"; // 4

    // Access the last element using a pointer one‑past‑the‑end
    int *end = numbers + 5; // points one past the last element (allowed)
    // *(end - 1) gives the last element
    std::cout << "Last element via pointer arithmetic: " << *(end - 1) << "
"; // 50

    // Demonstrate that pointer arithmetic respects element size
    std::cout << "Size of int: " << sizeof(int) << " bytes
";
    std::cout << "Address of numbers[0]: " << static_cast<void*>(numbers) << "
";
    std::cout << "Address of numbers[1] (numbers + 1): " << static_cast<void*>(numbers + 1) << "
";

    return 0;
}
