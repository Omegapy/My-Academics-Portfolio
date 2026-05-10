# Recommendation Guide: When to Choose Each Search Algorithm

## Overview

Choosing the right search algorithm depends on the dataset structures, how many searches need to be performed, and whether the data is already preprocessed, such as sorted. This guide provides decision criteria to help select between linear search and binary search.

---

## When to Use Linear Search

Linear search is the better choice when:

1. If the dataset is small (fewer than ~100 elements). At this small scale, both algorithms return results in microseconds, and the simplicity of linear search is better than the overhead and speed advantage of binary search.

2. If the data is unsorted and you only need one or a few searches. Sorting first takes O(n log n) time, this exceeds the O(n) cost of a single linear search. In other words, if you will not reuse the sorted order, the preprocessing cost is wasted.

3. If the data structure does not support random access. Binary search requires jumping to indices in O(1) time. Linked lists, streams, and generator-based data sources only support sequential access, making linear search the only option.

4. If the data changes frequently. If elements are constantly being inserted or removed, keeping the data sorted is expensive. A linear scan on the unsorted dataset may be simpler and faster.

5. If you need to find all occurrences. Linear search naturally visits every element, so collecting all matches requires no extra logic.

---

## When to Use Binary Search

Binary search is the better choice when:

1. If the dataset is large and already sorted (or sorting is acceptable). Binary search's O(log n) performance delivers dramatic savings at scale For example, searching 1,000,000 sorted elements requires at up to ~20 comparisons versus up to 1,000,000 for linear search.

2. If multiple searches will be performed on the same data. The one-time O(n log n) overhead sorting cost is amortized over many O(log n) searches. After just a few queries, the total cost is lower than the cost of repeated multiple linear scans.

3. If the data is stored in a random-access structure (array, Python list, NumPy array). Binary search uses O(1) index lookups, which helps achieve its logarithmic performance.

4. Response time matters. In real-time systems, search latency must be predictable. Binary search provides a worst-case time complexity of O(log n), which is an essential predictable performance for latency-sensitive applications such as autocomplete, database index lookups, and game engines.

---

## Decision Diagram

The following diagram replaces the text-only flowchart with a cleaner visual decision guide. It shows how sorted order, dataset size, and search frequency influence the recommended algorithm.

{{RECOMMENDATION_DECISION_DIAGRAM}}

---

## Practical Summary

| Criterion                    | Linear Search          | Binary Search             |
|------------------------------|------------------------|---------------------------|
| Dataset size                 | Small (< ~100)         | Medium to large           |
| Data order                   | Any (sorted or not)    | Must be sorted            |
| Number of searches           | One-time / few         | Repeated / many           |
| Data structure               | Any (list, linked, stream) | Random-access only    |
| Preprocessing needed         | None                   | O(n log n) sort           |
| Worst-case comparisons       | n                      | log₂(n)                   |
| Implementation complexity    | Trivial                | Moderate                  |

---

## Key Takeaway

In practice, there is no universally best algorithm; choosing the best-suited search algorithm depends heavily on the context. For a single lookup in unsorted data, linear search is simpler and faster. For repeated lookups in a large, sorted dataset, binary search is significantly more efficient. Understanding 'when' each algorithm is advantageous to implement is as important as understanding 'how' each algorithm works.
