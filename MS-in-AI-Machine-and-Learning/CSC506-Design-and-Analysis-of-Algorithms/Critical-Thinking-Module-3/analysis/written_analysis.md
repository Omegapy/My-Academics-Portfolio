# Written Analysis: Sorting Algorithm Performance

## Overview

Sorting is one of the core operations in computer science because many other tasks become easier once data is arranged in a predictable order. Searching, reporting, duplicate detection, and grouped analysis all benefit from ordered data. For that reason, sorting algorithms are commonly studied not only as programming exercises, but also as examples of how algorithmic design choices affect runtime, memory usage, and scalability. In this project, four comparison-based sorting algorithms were implemented and tested: Bubble Sort, Selection Sort, Insertion Sort, and Merge Sort.

The purpose of this analysis is to examine how each algorithm behaves both theoretically and practically. Theoretical analysis uses Big-O notation to describe how performance grows as input size `n` increases. Practical analysis uses benchmark results collected from the Benchmark Lab feature across four dataset types: random unsorted data, already sorted data, reverse-sorted data, and partially sorted data. The benchmark sizes used in the generated report are `1,000`, `5,000`, `10,000`, and `50,000` elements, which makes it possible to observe how quickly performance differences widen as the dataset becomes larger.

It is important to note that simple quadratic sorting algorithms are useful for understanding algorithm mechanics, but they do not scale well for large datasets. Insertion Sort can perform well on nearly sorted data, while Merge Sort is more efficient on large datasets because of its `O(n log n)` running time. The benchmark results in this project support those points clearly and show how input order can strongly influence the relative performance of the algorithms (CSU Global, n.d.).

---

## Bubble Sort

Bubble Sort repeatedly compares adjacent values and swaps them when they are out of order. After each pass through the list, the largest remaining unsorted value moves toward its final position, which is why the algorithm is described as having elements "bubble" to the top. Bubble Sort includes an early-exit optimization. If a full pass completes without any swaps, the algorithm stops immediately because the list is already sorted (CSU Global, n.d.).

From a Big-O perspective, Bubble Sort has a best-case time complexity of `O(n)` when the list is already sorted and the early-exit logic is present. Its average-case and worst-case time complexities are both `O(n^2)`. Its auxiliary space usage is `O(1)` because it sorts in place, and it is considered stable because equal values do not need to cross one another during adjacent swaps.

In practice, Bubble Sort is useful primarily as a teaching algorithm. It is easy to visualize, easy to trace step by step, and helpful for demonstrating how repeated passes gradually reduce disorder in a list. However, the benchmark results also show that its performance becomes poor very quickly on unsorted datasets. On random unsorted data at `50,000` elements, Bubble Sort required `93,351.50 ms`, while Merge Sort completed the same scenario in `123.05 ms`. That difference shows how severe quadratic growth becomes at larger sizes.

Bubble Sort does have one scenario where it performs extremely well: already sorted data. In this benchmark, Bubble Sort was the fastest algorithm for sorted datasets at every tested size. At `1,000` elements, it completed in only `0.0460 ms`, and at `50,000` elements, it still completed in only `2.5783 ms`. This matches the theoretical expectation that early-exit Bubble Sort can run in linear time on sorted input.

---

## Selection Sort

Selection Sort works by repeatedly finding the smallest value in the unsorted portion of the list and swapping it into the first unsorted position. After the first pass, the smallest value is fixed in place. After the second pass, the second-smallest value is fixed in place, and the process continues until the list is sorted.

The course lecture notes describe Selection Sort as simple to understand but inefficient, and the benchmark results strongly support that description (CSU Global, n.d.). Selection Sort has best-case, average-case, and worst-case time complexity of `O(n^2)` because it still scans the unsorted portion of the list completely on every pass, even when the data is already ordered. Its auxiliary space is `O(1)` because it is an in-place sort, but it is not stable because a swap can change the original relative order of equal elements.

One notable strength of Selection Sort is that it minimizes swaps. In the benchmark results, its swap count remained dramatically lower than Bubble Sort on reverse-sorted and random datasets. For example, on random unsorted data at `50,000` elements, Selection Sort performed only `49,990` swaps, while Bubble Sort performed `624,111,362` swaps. That does not make Selection Sort fast overall, but it does help explain why it sometimes outperformed Bubble Sort and Insertion Sort on difficult quadratic cases even though all three are `O(n^2)` algorithms.

Even so, Selection Sort was never the top performer in any benchmark scenario. On already sorted data at `50,000` elements, it still required `43,670.53 ms`, while Bubble Sort needed `2.5783 ms` and Insertion Sort needed `4.8566 ms`. This makes Selection Sort a poor choice for general-purpose sorting, although it remains useful as an instructional example and in rare cases where minimizing writes is more important than minimizing comparisons.

---

## Insertion Sort

Insertion Sort builds a sorted portion of the array one element at a time. For each new element, it shifts larger sorted values to the right until the current value can be inserted into the correct position. The lecture materials explain that Insertion Sort is especially useful when data is already mostly sorted, and the Benchmark Lab results reflect that very clearly.

Its best-case time complexity is `O(n)` because each new element is already in the correct position when the data is sorted. Its average-case and worst-case time complexities are `O(n^2)`. It uses `O(1)` extra space and is stable because equal values can retain their original order during insertion. Although it is still a quadratic algorithm, it is more adaptive than Bubble Sort and Selection Sort because it does less work when the list is close to sorted order.

This adaptive behavior is most visible in the partially sorted scenarios. At `5,000` elements, Insertion Sort completed in `113.47 ms`, which is much faster than Bubble Sort at `660.48 ms` and Selection Sort at `433.11 ms`. At `50,000` elements on partially sorted data, Insertion Sort required `11,676.09 ms`. That is still much slower than Merge Sort, but it is far better than the other two quadratic algorithms and supports the idea that Insertion Sort is a practical choice for small or nearly sorted datasets.

Insertion Sort also performed very well on already sorted input. At `1,000` elements, it completed in `0.0897 ms`, and at `50,000` elements, it completed in `4.8566 ms`. These results confirm the standard Big-O analysis and reinforce why insertion-based methods are commonly used as the small-array base case inside hybrid sorting implementations.

---

## Merge Sort

Merge Sort is a divide-and-conquer algorithm. It recursively splits the input list into smaller halves until each subproblem contains zero or one element. Those small sublists are then merged back together in sorted order. The course materials emphasize that Merge Sort performs well on large datasets because it reduces the sorting problem into smaller recursive subproblems and combines the results efficiently (CSU Global, n.d.).

Its time complexity is `O(n log n)` in the best, average, and worst cases. This is its major advantage over the three quadratic algorithms tested in this assignment. Merge Sort is also stable, which is important when sorting records that contain duplicate keys where original order should be preserved. Its main disadvantage is auxiliary space usage of `O(n)` because an additional structure is needed during the merge process. That means it is not in place in the same way as Bubble Sort, Selection Sort, and Insertion Sort.

The benchmark results show that Merge Sort dominated almost every scenario. It was the fastest algorithm for all random unsorted, reverse-sorted, and partially sorted datasets at every tested size. On random unsorted data at `10,000` elements, Merge Sort completed in `21.2719 ms`, while the next-fastest algorithm, Selection Sort, required `1,727.1232 ms`. At `50,000` elements on reverse-sorted data, Merge Sort completed in `104.3031 ms`, while Selection Sort required `46,693.9315 ms`. These numbers provide strong practical confirmation of the difference between `O(n log n)` and `O(n^2)` growth.

The only scenario where Merge Sort was not the winner was already sorted data. In that case, Bubble Sort and Insertion Sort both benefited from linear best-case behavior, while Merge Sort continued to perform its recursive splitting and merging work. Even there, however, Merge Sort remained predictable and scalable, finishing the `50,000`-element sorted scenario in `102.21 ms`.

---

## Comparative Big-O Analysis

Big-O notation is useful in this project because it explains why the relative rankings seen in the benchmark results are not accidental. The notation focuses on how the amount of work grows as `n` becomes large, not just on a single timing measurement from one machine. As the dataset sizes increase from `1,000` to `50,000`, the difference between `O(n^2)` growth and `O(n log n)` growth becomes dramatic.

**Table 1**  
*Theoretical Complexity Comparison of The Sorting Algorithms*

| Algorithm | Best Case | Average Case | Worst Case | Extra Space | Stable | In-Place |
|-----------|-----------|--------------|------------|-------------|--------|----------|
| Bubble Sort | `O(n)` | `O(n^2)` | `O(n^2)` | `O(1)` | Yes | Yes |
| Selection Sort | `O(n^2)` | `O(n^2)` | `O(n^2)` | `O(1)` | No | Yes |
| Insertion Sort | `O(n)` | `O(n^2)` | `O(n^2)` | `O(1)` | Yes | Yes |
| Merge Sort | `O(n log n)` | `O(n log n)` | `O(n log n)` | `O(n)` | Yes | No |

*Note*: The table summarizes the standard asymptotic time and space behavior of each sorting algorithm as implemented in the Benchmark Lab feature.

Table 1 shows two important patterns. First, Merge Sort is the only algorithm in this project with `O(n log n)` growth across all major cases, which explains why it scales so much better for medium and large datasets. Second, Bubble Sort and Insertion Sort both have `O(n)` best-case behavior, which explains why they perform so well on already sorted data. Selection Sort lacks this adaptive property, so it remains quadratic even when the input is already in perfect order.

---

## Benchmark Results and Interpretation

The benchmark lab measured runtime, comparisons, swaps, and writes for every combination of four algorithms, four dataset types, and four dataset sizes. Each algorithm received a fresh copy of the same scenario dataset so that the results would be fair and reproducible.

**Table 2**  
*Benchmark Results for All Sorting Scenarios*

{{BENCHMARK_RESULTS_TABLE}}

*Note*: The table shows the measured runtime and operation counts for each algorithm across all dataset types and sizes tested in the Benchmark Lab feature.

**Table 3**  
*Fastest Algorithm by Dataset Type and Size*

{{SCENARIO_WINNERS_TABLE}}

*Note*: The winner table summarizes which algorithm completed each scenario fastest and identifies the runner-up for comparison.

**Figure 1**  
*Runtime Comparison Chart*

{{RUNTIME_CHART}}

*Note*: The chart visualizes how runtime changes across dataset sizes and input patterns, making the scaling gap between `O(n^2)` and `O(n log n)` algorithms easier to see.

The benchmark results reveal four major conclusions. First, Merge Sort is the best general-purpose algorithm in this project. It won every random unsorted, reverse-sorted, and partially sorted scenario from `1,000` through `50,000` elements. Second, Bubble Sort was the fastest option on already sorted data because its early-exit optimization reduced the work to one pass through the list. Third, Insertion Sort was consistently the strongest of the quadratic algorithms on partially sorted input because it adapts well when only a limited number of values are out of place. Fourth, Selection Sort remained predictable but uncompetitive because its comparison count stayed quadratic regardless of input order.

The random unsorted cases provide one of the clearest examples of algorithmic scaling. At `1,000` elements, Merge Sort completed in `1.6003 ms`, while the fastest quadratic competitor, Selection Sort, required `17.4511 ms`. At `50,000` elements, Merge Sort required `123.0534 ms`, while Selection Sort required `43,440.3886 ms`. This widening gap is exactly what Big-O analysis predicts: as `n` grows, the lower-growth algorithm becomes overwhelmingly preferable.

The reverse-sorted cases show how damaging worst-case input can be for quadratic algorithms. Bubble Sort and Insertion Sort both performed especially poorly because they had to make the maximum possible amount of movement through the list. In contrast, Merge Sort remained efficient because the initial order of the data does not change its asymptotic behavior in the same way.

The partially sorted cases are important because they show that not all `O(n^2)` algorithms behave identically in practice. Insertion Sort benefited from the limited disorder and substantially outperformed Bubble Sort and Selection Sort, but it still could not match Merge Sort on the tested sizes. This is a good reminder that theoretical complexity gives the broad expectation, while benchmark data reveals how implementation details and input characteristics affect real performance.

---

## Conclusion

This project demonstrates that the best sorting algorithm depends on both theory and context. Merge Sort is the strongest overall choice for large or unpredictable datasets because its `O(n log n)` runtime remains efficient across all major input patterns tested. Bubble Sort and Insertion Sort can be excellent on already sorted or nearly sorted data because they are adaptive and can approach linear behavior in those cases. Selection Sort is easy to understand and uses very few swaps, but it is not a strong general-purpose choice because its runtime remains quadratic regardless of dataset order.

The benchmark evidence aligns closely with the Module 3 course content. Simple quadratic algorithms are valuable for learning and for a few specialized scenarios, but they do not scale well as datasets become larger. Merge Sort, by contrast, demonstrates why divide-and-conquer algorithms are so important in algorithm analysis: they solve the same problem while growing much more slowly as the input size increases.

In practical terms, the Benchmark Lab results support the following guidance. If the data is large or the input order is unknown, choose Merge Sort. If the data is already sorted or nearly sorted and the dataset is small, Insertion Sort or Bubble Sort may be competitive. If minimizing swaps is more important than minimizing comparisons, Selection Sort may still have limited value. Overall, the assignment confirms that Big-O analysis and benchmark testing work best together: theory explains the pattern, and measurement proves how large the difference becomes in real use.

---

## References

CSU Global. (n.d.). *Lecture 3 - Sorting Algorithms* [Course lecture notes]. CSC506 -
Design and Analysis of Algorithms. Canvas.
