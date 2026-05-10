# Bubble Sort, Quickselect, and Set Operations Analysis

## Overview

Sets, Bubble Sort, and Quickselect are important in computer science because
they solve different kinds of problems. A set is used when the main goal is to
store unique values and support fast membership checking. Bubble Sort is used
when the main goal is to illustrate comparison-based sorting in a simple,
traceable way. Quickselect is used when the main goal is to find one rank, such
as the kth-smallest value, without paying for a complete sorted order.

The purpose of this analysis is to examine how each Bubble Sort and Quickselect
both theoretically and practically. Theoretical analysis uses Big-O notation to
describe how performance grows as input size `n` increases. Practical analysis
uses benchmark results collected from this section Benchmark Lab, across four
timed workload groups: `Bubble Sort full sort`, `Python sorted full sort`,
`Quickselect kth selection`, and `Python sorted kth selection`. The benchmark
sizes in the saved report are `25`, `100`, and `250` items, and the dataset
scenarios are `random`, `sorted`, `reverse_sorted`, `duplicate_heavy`, and
`partially_sorted`. Together, those cases make it possible to observe both
general growth and input-specific behavior.

It is important to note that the same algorithm idea can behave very
differently depending on how it is implemented. Bubble Sort depends strongly on
input order and benefits greatly from early exit when the data is already
sorted. Quickselect depends heavily on pivot behavior, especially when the pivot
choice is deterministic. Set performance depends on hashing quality and on
whether the workload is focused on membership or full derived-set construction.
The benchmark results in this project support those points clearly.

One additional point matters in this module: the benchmark CSV focuses on the
sorting and selection workloads, not a separate set-timing suite. For that
reason, the set discussion below is primarily theoretical and behavioral, while
the runtime discussion is centered on Bubble Sort, Quickselect, and the Python
`sorted` baselines.

---

## Set ADT Behavior

A set stores unique values and is designed around membership rather than
position. In this project, `CourseSet` is implemented with a hash-backed Python
dictionary. That choice preserves first-seen order for classroom readability
while still modeling the central set rule: each value is either present or
absent. In other words, duplicates are ignored, and membership is the central
operation.

From a Big-O perspective, the Set ADT has a favorable performance profile for
single-value membership changes. `add`, `remove`, and `contains` are average-
case `O(1)` because hashing usually allows direct access to the relevant key.
The worst case can still move toward `O(n)` if hashing degrades badly, but the
expected classroom behavior is constant-time lookup. Static set operations such
as `union`, `intersection`, `difference`, and `symmetric_difference` are
typically `O(n + m)` because they need to scan the values of both operands.

In practice, the Set Lab reinforces that distinction clearly. Dynamic
operations such as `add` and `remove` mutate one target set and report whether
the set actually changed. Static operations produce a new derived result and
leave both source operands unchanged. That difference is important because it
separates direct state mutation from derived-result construction, which is one
of the central lessons of working with sets in algorithm design.

**Table 1**  
*Core Set Operation Meanings in This Project*

| Operation                  | Meaning                                    | Example Result                                        |
|----------------------------|--------------------------------------------|-------------------------------------------------------|
| `union`                    | Values in either set                       | `{1, 2}` union `{2, 3}` gives `{1, 2, 3}`             |
| `intersection`             | Values in both sets                        | `{1, 2}` intersection `{2, 3}` gives `{2}`            |
| `difference`               | Values in the first set only               | `{1, 2}` difference `{2, 3}` gives `{1}`              |
| `symmetric_difference`     | Values in exactly one set                  | `{1, 2}` symmetric difference `{2, 3}` gives `{1, 3}` |

*Note*: The implementation preserves first-seen order for readability, but the
important set behavior is uniqueness and membership rather than display order.

---

## Bubble Sort

Bubble Sort repeatedly compares adjacent values and swaps them when the left
value is greater than the right value. The Bubble Sort reference explains that
this kind of algorithm is easy to understand because it only works with one
neighboring pair at a time. In this project, the implementation also uses an
early-exit optimization. If one pass completes with no swaps, the list is
already sorted and the algorithm stops immediately.

From a Big-O perspective, Bubble Sort has a mixed profile. The best case is
`O(n)` when the data is already sorted and early exit ends the algorithm after
one pass. The average and worst cases remain `O(n^2)` because the nested-pass
design can require repeated scans through most of the list. Auxiliary space is
`O(1)`, which makes Bubble Sort conceptually in-place.

In practice, the benchmark results strongly support that description. The
average runtime for `Bubble Sort full sort` grows from `0.033758 ms` at `25`
items to `0.486292 ms` at `100` items and `2.401383 ms` at `250` items. That
is a `71.13x` increase from the smallest to the largest tested size. The input
pattern also matters a great deal. At `250` items, sorted input finishes in
only `0.020791 ms`, while reverse-sorted input requires `3.828625 ms`, which
is about `184.15x` slower. Those results make the early-exit effect easy to
see.

The operation counts tell the same story. On sorted input of size `250`,
Bubble Sort performs only `249` comparisons and `0` swaps. On reverse-sorted
input of the same size, it requires `31,125` comparisons, `31,095` swaps, and
`62,190` writes. These results show that Bubble Sort is useful for teaching
algorithm mechanics, but it becomes expensive quickly when the data is not
already close to sorted order.

---

## Quickselect Analysis

Quickselect finds one target rank without fully sorting the dataset. It
partitions the active region around a pivot, then continues only into the side
that can still contain the requested rank. In this project, the implementation
uses a deterministic Lomuto-style partition with the rightmost active value as
the pivot. That choice is useful for classroom trace reproducibility, but it
also creates predictable weak cases.

From a Big-O perspective, Quickselect is attractive because its average-case
runtime is `O(n)`. When the pivot tends to remove a meaningful portion of the
search space, only part of the dataset needs to be revisited. However, the
worst case is still `O(n^2)` when the pivot repeatedly lands at or near one
end, which causes very unbalanced partitions.

In practice, the benchmark results show both the strength and the limitation of
this implementation. The average runtime for `Quickselect kth selection` grows
from `0.020242 ms` at `25` items to `0.207358 ms` at `100` items and
`0.654900 ms` at `250` items. That is a `32.35x` increase from the smallest to
the largest tested size. This is substantially better scaling than Bubble Sort,
but still much more sensitive to input order than the Python `sorted`
baselines.

The dataset-specific results are especially important. At `250` items,
Quickselect requires only `0.073292 ms` on `partially_sorted` input,
`0.085875 ms` on `random` input, and `0.124500 ms` on `duplicate_heavy` input.
However, it rises sharply to `1.375250 ms` on `reverse_sorted` input and
`1.615583 ms` on `sorted` input. The sorted case is about `18.81x` slower than
the random case at the same size. These results show that the deterministic
rightmost pivot is efficient on many everyday inputs, but performs much worse
when the pivot repeatedly behaves like an extreme value.

Another practical point is also important. In this Python environment,
Quickselect is not faster than the `Python sorted kth selection` baseline. At
`250` items, the average Quickselect runtime is `0.654900 ms`, while the
average full-sort kth-selection baseline is only `0.006533 ms`, which is about
`100.24x` faster. That does not mean the algorithmic idea is wrong. Instead, it
shows that an asymptotically favorable algorithm can still lose in practice
when the baseline is implemented in highly optimized C and the custom
implementation is written in Python for traceability and instruction.

---

## Comparative Big-O Analysis

Big-O notation is useful in this project because it explains why the relative
rankings in the benchmark data are not accidental. Bubble Sort does repeated
adjacent comparisons and therefore grows quadratically on average. Quickselect
tries to avoid full sorting and therefore has linear average behavior, but it
still suffers when pivot choices are poor. Set membership is fast because it is
hash-based, while full set combination work must still scan the operand values.
Those same ideas appear in this project's benchmark results.

**Table 2**  
*Theoretical Complexity Comparison of the Core Module 8 Operations*

| Structure or Algorithm                | Best                                                                   | Average                          | Worst                                                        | Space                  | Key implementation note                                                 |
|---------------------------------------|------------------------------------------------------------------------|----------------------------------|--------------------------------------------------------------|------------------------|-------------------------------------------------------------------------|
| Set membership / `add` / `remove`     | `O(1)`                                                                 | `O(1)`                           | `O(n)`                                                       | `O(n)` overall storage | Hash-backed dictionary with insertion-order display                     |
| Set union / intersection / difference | Not usually expressed separately                                       | `O(n + m)`                       | `O(n + m)` with normal hashing, worse if hashing degrades    | `O(n + m)`             | Returns a new derived set and leaves operands unchanged                 |
| Bubble Sort with early exit           | `O(n)`                                                                 | `O(n^2)`                         | `O(n^2)`                                                     | `O(1)`                 | Adjacent comparison sorting with pass-level early exit                  |
| Quickselect                           | `O(n)`                                                                 | `O(n)`                           | `O(n^2)`                                                     | `O(1)` conceptual      | Rightmost-value Lomuto partition for kth-smallest selection             |
| Python `sorted` baseline              | Better on highly ordered inputs, but generally treated as `O(n log n)` | `O(n log n)`                     | `O(n log n)`                                                 | Depends on implementation details | Built-in Timsort baseline used for comparison and validation |

*Note*: The table reflects the specific implementations used in this project,
not every possible implementation of sets, sorting, or selection.

Table 2 matches the observed growth patterns well. Average `Bubble Sort full
sort` runtime grows `71.13x` from `25` to `250`, while average `Quickselect kth
selection` runtime grows `32.35x`. In contrast, `Python sorted full sort` grows
only `10.70x`, and `Python sorted kth selection` grows `7.00x`. These
different growth rates are exactly what should be expected when one workload is
quadratic, another is usually linear but pivot-sensitive, and the built-in
baseline comes from a heavily optimized library implementation.

---

## Benchmark Results

The Benchmark Lab measured runtime for every major workload at sizes `25`,
`100`, and `250` across five dataset scenarios: `random`, `sorted`,
`reverse_sorted`, `duplicate_heavy`, and `partially_sorted`.

### Workload Groups

- `Bubble Sort full sort` measures full adjacent-comparison sorting with early
  exit.
- `Python sorted full sort` measures the built-in Timsort baseline for complete
  ordering.
- `Quickselect kth selection` measures partition-based kth-smallest selection.
- `Python sorted kth selection` measures the assignment baseline of selecting
  the kth-smallest value by fully sorting first.

**Table 3**  
*Average Runtime by Operation and Size*

| Size  | Bubble Sort full sort | Python sorted full sort | Quickselect kth selection | Python sorted kth selection |
|-------|-----------------------|-------------------------|---------------------------|-----------------------------|
| `25`  | `0.033758 ms`         | `0.000967 ms`           | `0.020242 ms`             | `0.000933 ms`               |
| `100` | `0.486292 ms`         | `0.005183 ms`           | `0.207358 ms`             | `0.003133 ms`               |
| `250` | `2.401383 ms`         | `0.010350 ms`           | `0.654900 ms`             | `0.006533 ms`               |

**Table 4**  
*Dataset Sensitivity at Size `250`*

| Dataset type       | Bubble Sort full sort | Quickselect kth selection |
|--------------------|-----------------------|---------------------------|
| `random`           | `3.420042 ms`         | `0.085875 ms`             |
| `sorted`           | `0.020791 ms`         | `1.615583 ms`             |
| `reverse_sorted`   | `3.828625 ms`         | `1.375250 ms`             |
| `duplicate_heavy`  | `2.433208 ms`         | `0.124500 ms`             |
| `partially_sorted` | `2.304250 ms`         | `0.073292 ms`             |

The benchmark results show that the built-in Python baselines are the strongest
practical performers in this project. At `250` items, `Python sorted full sort`
averages only `0.010350 ms`, while `Bubble Sort full sort` averages
`2.401383 ms`. This means Bubble Sort is about `232.01x` slower than the
built-in full-sort baseline at the largest tested size. The same pattern
appears in kth selection. At `250` items, `Quickselect kth selection` averages
`0.654900 ms`, while `Python sorted kth selection` averages `0.006533 ms`.

However, the comparison inside the custom algorithms is still meaningful.
Quickselect is far more favorable than Bubble Sort when the task is selection
rather than full ordering. On random input of size `250`, Bubble Sort requires
`3.420042 ms`, while Quickselect needs only `0.085875 ms`. On partially sorted
input of the same size, Bubble Sort requires `2.304250 ms`, while Quickselect
needs only `0.073292 ms`. These results support the main algorithm lesson of
the module: finding one rank is a different problem from sorting everything,
and the choice of algorithm should reflect that difference.

The benchmark results also make input sensitivity easy to see. Bubble Sort is
helped enormously by already sorted data because early exit ends the work after
one no-swap pass. Quickselect, on the other hand, is hurt by sorted and reverse
sorted data in this implementation because the rightmost pivot repeatedly
creates poor partitions. Those contrasting results are especially useful for
teaching because they show that best-case, average-case, and worst-case
behavior are not abstract ideas. They appear directly in measured runtime,
comparison counts, swap counts, and write counts.

---

## Conclusion

The results of this project show that the chosen implementations behave the way
algorithm analysis predicts. The Set ADT is the right conceptual tool when the
problem depends on uniqueness, membership, and derived set relationships. The
Bubble Sort implementation clearly demonstrates adjacent-comparison sorting and
the value of early exit, but its quadratic growth makes it unsuitable for
larger workloads. Quickselect is the more appropriate custom algorithm when the
goal is to find one rank rather than produce a complete sorted order, although
its deterministic pivot choice still creates clear weak cases.

The benchmark results also reinforce an important practical lesson. The
algorithm with the better asymptotic story is not automatically the fastest
implementation in a real Python program. Python `sorted` remains the strongest
measured baseline in this project because it is highly optimized. Taken
together, the results support the central Module 8 takeaway: the best algorithm
depends on the exact task, the input pattern, and the quality of the
implementation, not only on the name of the technique.



