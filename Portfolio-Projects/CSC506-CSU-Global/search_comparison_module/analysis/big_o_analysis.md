# Big-O Analysis of Linear Search and Binary Search

Big-O notation is a standard way to describe how the running time or memory usage of an algorithm grows as the input size `n` becomes larger. Instead of focusing on exact seconds, processor speed, or programming language details, Big-O focuses on the growth rate of the work an algorithm performs. In practical terms, it gives an asymptotic upper bound on performance and is most often used to discuss worst-case behavior (GeeksforGeeks, 2026; Ricciardi, 2024).

Formally, Big-O describes a function `f(n)` in relation to another function `g(n)` when there are constants that make `f(n)` grow no faster than a constant multiple of `g(n)` for sufficiently large values of `n` (GeeksforGeeks, 2026; Ricciardi, 2024). One of the most important ideas in Big-O analysis is that constants and lower-order terms are ignored. For example, if one algorithm takes `3n + 2` steps and another takes `n`, both are still considered linear because the dominant term is `n`. This makes Big-O especially useful for comparing algorithms in a hardware-independent way, since it highlights how performance scales rather than how fast one specific computer happens to run the code.

This project compares two search algorithms, linear search and binary search. Linear search has a worst-case time complexity of `O(n)`, while binary search has a worst-case time complexity of `O(log n)`. In academia, linear search is often used as a classic linear-time example, and binary search is often used as a classic logarithmic-time example, to explain that lower-growth algorithms, such as binary search, scale better as the input size increases. This is used to make the argument that although both algorithms solve the same problem, their related growth rates become very important as datasets become larger.

---

## Linear Search: `O(n)`

Linear search checks each value in order from the beginning of the list until the searched value is found or the list ends. Because it may need to inspect every element within a dataset, its running time grows directly proportional to the size of the dataset. The algorithm is classified as a one-pass traversal and is a classic example of linear time (GeeksforGeeks 2026).

If a list contains `n` items, the worst case occurs when the searched value is either the last item or not present at all. In that situation, the algorithm must perform `n` comparisons, so its worst-case time complexity is `O(n)`. The average case is also linear because, on average, about half of the elements must be checked before a match is found. The best case is `O(1)` when the first element is the target.

**Table 1**  
*Linear Search Big-O Analysis*

| Case    | Comparisons | Big O    | Explanation                                                        |
|---------|-------------|----------|--------------------------------------------------------------------|
| Best    | `1`         | `Ω(1)`   | The target is the first item.                                      |
| Average | `n / 2`     | `Θ(n)` | The target is the middle of the dataset.                           |
| Worst   | `n`         | `O(n)`   | The target is last or not present.                                 |

*Note*: The table showcases the theoretical best, average, and worst cases for linear search.

In practice, linear search is simple and flexible. It works on unsorted data, requires no preprocessing, and uses constant extra space. Its weakness is scalability. If the dataset doubles in size, the number of potential comparisons also doubles. That straight-line growth is exactly what Big O notation captures with `O(n)`.

---

## Binary Search: `O(log n)`

Binary search is more efficient, but it only works correctly when the data is already sorted. Instead of checking every element one by one, binary search compares the searched value to the middle element of the current search range. If the searched value is smaller, the algorithm discards the upper half of the range. If the searched value is larger, it discards the lower half. Each comparison removes half of the remaining dataset search space.

This repeated halving produces a logarithmic growth rate. After one comparison, about `n / 2` elements remain; after two comparisons, about `n / 4`; after three, about `n / 8`and so on. In general, after `k` comparisons, the remaining range is about `n / 2^k`. The search stops when the range becomes empty or the target is found, which leads to `k ≈ log2(n)`. This logarithmic growth increases very slowly compared with linear or quadratic growth, making the search faster, especially for large datasets (Ricciardi, 2026).

**Table 2**  
*Binary Search Big-O Analysis*
| Case    | Comparisons | Big O          | Explanation                                                                    |
|---------|-------------|----------------|--------------------------------------------------------------------------------|
| Best    | `1`         | `Ω(1)`         | The searched value is at the midpoint.                                         |
| Average | `log2(n)`   | `Θ(log n)`     | On average, each comparison cuts the remaining search interval in half.        |
| Worst   | `log2(n)`   | `O(log n)`     | The searched value is not in the dataset or at the end of the halving process (at the beginning or at the end of the dataset) |

*Note*: The table showcases the theoretical best, average, and worst cases for binary search. 

In practice, the binary search is significantly more advantageous to use than the linear search on large datasets. For a dataset of 100,000 items, linear search may require up to 100,000 comparisons, while binary search needs only about 17 comparisons. That difference shows why `O(log n)` is considered far more scalable than `O(n)` for repeated searching on sorted data.

---

## Why `O(log n)` Beats `O(n)`

Big O notation describes how quickly work grows as `n` increases. The main alghorythmic function types used in algorithm analysis include constant, logarithmic, linear, and quadratic growth (Ricciardi 2024). Additionally, functions with lower growth rates scale better as problems or datasets get larger. In other words, a logarithmic algorithm implementation does not just save a few steps; it scales better as the problem/dataset size increases.

### Benchmark Results DataFrame

The following benchmark measures the execution time and number of comparisons for both algorithms on datasets with increasing size. 

**Table 3**  
*Benchmark Results*

{{BENCHMARK_RESULTS_DATAFRAME}}

*Note*: The table showcases the measured execution time and number of comparisons for both algorithms on datasets with increasing size.

{{BENCHMARK_RESULTS_SUMMARY}}

### Runtime Chart

The following chart shows that the runtime of a linear search increases more quickly than that of a binary search as the dataset size grows.

**Figure 1**  
*Runtime Chart*

{{BENCHMARK_TIME_CHART}}

*Note*: The chart shows the measured execution time for both algorithms on datasets with increasing dataset sizes.

The chart shows that linear search time rises as the dataset grows, while binary search time increases only slightly. This aligns with the Big O analysis, predicting that as the dataset grows larger, the algorithm with the smaller growth rate will be the better choice, performing significantly faster searches as the dataset size increases.

### Growth Pattern Diagram

The following chart illustrates the shape of each algorithm's growth. It provides a visual representation comparing the growth rates of linear and logarithmic growth. It illustrates well how linear search grows much slower than more slowly than the binary serach as the dataset scales.

**Figure 2**  
*Growth Pattern Diagram Using Big-O Analysis*

{{BIG_O_COMPARISON_DIAGRAM}}

*Note*: The chart shows the growth pattern of both algorithms, using Big-O notation, on datasets with increasing dataset sizes.

---

## Conclusion

Even though binary search is faster, it is not always the best choice as the algorithm requires sorted data to work properly. For example, if the dataset is small, unsorted, and only one or two searches are needed to be performed, a linear search may be more practical because it can be used without the overhead of sorting the data. A real-world application of the algorithm is searching for a specific name in a small dynamic dataset, such as a list of names in a phone book that is not in alphabetical order. 

On the other hand, if repeated searches are needed on a dataset, binary search becomes the better choice. The overhead of sorting the dataset one time can be justified because each future search benefits from faster lookups. A real-world application of the algorithm is searching for a specific term in a large static dataset, such as a dictionary.

In other words, the best algorithm depends just on theoretical complexity provided by a Big-O analysis, but also on the context of the usage (dynamic or static datasets), whether the data is preprocessed or not, such as whether the data is sorted or not, and how often searches need to be performed.

---

## References

GeeksforGeeks. (2026, February 28). *Big O notation*. https://www.geeksforgeeks.org/dsa/analysis-algorithms-big-o-analysis/

Ricciardi, A. (2024, August 28). *Big-Oh notation: Key to evaluating algorithm efficiency*. Omega.py. https://www.alexomegapy.com/post/big-oh-notation
