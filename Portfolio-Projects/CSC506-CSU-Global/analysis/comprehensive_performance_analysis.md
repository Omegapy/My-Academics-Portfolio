# Comprehensive Performance Analysis

## Executive Overview

This project brings together fundamental computer science algorithm and data structure. 
The tool includes search algorithms, sorting and selection algorithms, set operations, 
linked structures, tree-backed maps, hash tables, priority queues, and graph algorithms. 

The purpose of this analysis is to examine how the integrated portfolio behaves both 
theoretically and practically. Theoretical analysis uses Big-O notation to describe how 
performance grows as datasets become larger. Practical analysis uses the saved benchmark 
CSV files, charts, and written analyses from different modules labs. Together, 
those sources make it possible to compare algorithm growth, implementation tradeoffs, 
and workload fit across the full portfolio. The analysis is also based on material from
the CSC506 Design and Analysis of Algorithms course curriculum of Colorado State University Global (CSU Global)

It is important to note that the same algorithm idea can behave very
differently depending on input order, representation choice, collision
distribution, tree shape, graph density, and implementation details
(GeeksforGeeks, 2026; Ricciardi, 2024). The saved results support that point
clearly. In particular, they show that binary search outperforms linear search
only when sorted order is available, Bubble Sort becomes expensive quickly on
unsorted data, Quickselect is better suited for rank selection than full
sorting, and hash tables perform best when key distribution remains healthy.

The lecture notes from CSC506 course the for each module also help frame the integrated story. 
The lecture notes describe sets as unordered collections of unique items and present Bubble Sort
and Quickselect as different responses to ordering problems (CSU Global,
n.d.-e; Tutorials Point, n.d.-b). That same idea extends across the whole
project. Different structures are useful because they optimize different
operations, not because one structure is automatically best in every context.

## Search Algorithms: Linear Search vs Binary Search

Search algorithms are important in computer science because many applications
depend on locating a value quickly inside a dataset. In this project, the
search-comparison module evaluates two classic approaches: linear search and
binary search. Linear search checks values one by one from left to right.
Binary search repeatedly cuts the remaining search range in half, but only when
the dataset is sorted (GeeksforGeeks, 2026; Ricciardi, 2024).

From a Big-O perspective, the two algorithms have very different growth
patterns. Linear search has worst-case `O(n)` runtime because it may need to
inspect every item in the dataset. Binary search has worst-case `O(log n)`
runtime because each comparison eliminates half of the remaining search
interval. This difference is one of the clearest examples in the portfolio of
how lower-growth algorithms scale better as input size increases
(GeeksforGeeks, 2026; Ricciardi, 2024).

In practice, the saved benchmark results show that difference clearly. 
In the search comparison module, linear search grows from `0.0031 ms` 
at `100` items to `1.7176 ms` at `50,000` items. Over the same sizes, 
binary search changes only from `0.0011 ms` to `0.0020 ms`. 
The comparison counts are just as useful. Linear search requires
`100` comparisons at `100` items and `50,000` comparisons at `50,000` items,
while binary search needs only `7` comparisons at `100` items and `16`
comparisons at `50,000` items. These results show that the measured behavior
matches the Big-O analysis very closely.

It is also important to note that binary search is not always the better
practical choice. It depends on sorted order, and that requirement introduces a
preprocessing cost. If a dataset is small, unsorted, or changing often, linear
search can still be more practical because it works immediately without sorting
overhead. In practical terms, the search module shows that algorithm choice
depends not only on growth rate, but also on whether the data is already in the
right form for the algorithm to work well (GeeksforGeeks, 2026; Ricciardi,
2024).

## Sorting and Selection: Bubble Sort, Sorting Context, Quickselect

Sorting and selection are important because many applications need ordered data
or need one specific rank inside a dataset. In the integrated portfolio, this
area combines two kinds of evidence. The  provides the broader sorting
comparison among Bubble Sort, Selection Sort, Insertion Sort, and Merge Sort.
The Quickselect Sets module adds Bubble Sort and Quickselect as a focus.

The purpose of the sorting evidence is to show how strongly growth rate and
input order affect runtime. The critical thinking assignment lab from the module 3 of the 
CSC506 course shows that the gap between `O(n^2)` and `O(n log n)`
behavior becomes very large as the dataset grows (CSU Global,n.d.-a). 
On `random_unsorted` data at `10,000` items, the saved Module 3 lab results
report `3664.6691 ms` for Bubble Sort, `1722.0950 ms` for Selection Sort,
`1956.6832 ms` for Insertion Sort, and only `21.2856 ms` for Merge Sort. 
These results make it clear that simple quadratic sorts are useful for teaching,
but they do not scale well on larger unsorted workloads.

From a Big-O perspective, Bubble Sort has mixed behavior. With early exit, its
best case is `O(n)` when the dataset is already sorted. Its average and
worst-case behavior remain `O(n^2)` because it can still require repeated full
passes through the list. The Bubble Sort reference describes it as a
comparison-based algorithm that repeatedly swaps adjacent out-of-order elements
and is not suitable for large datasets under average and worst-case `O(n^2)`
behavior (Tutorials Point, n.d.-b). Additionally,Bubble Sort is easy to trace, 
but expensive when disorder is high (CSU Global, n.d.-e).

In practice, the benchmark results support that point clearly. 
In the bubble quickselect module benchmark lab results,
Bubble Sort finishes in `0.020791 ms` on sorted input of size `250`, but
requires `3.828625 ms` on reverse-sorted input of the same size. These results
show how much the early-exit optimization matters. When no swaps happen, the
algorithm stops quickly. When many adjacent values are out of order, the
quadratic cost becomes much more visible.

Quickselect solves a different kind of problem. The main goal is not to fully
sort the data, but to find one requested rank such as the kth-smallest value.
It is an important distinction between full ordering and partial selection (CSU Global, n.d.-e). 
From a Big-O perspective, Quickselect has average `O(n)` behavior because it 
only continues into the side of the partition that can still contain the requested rank. 
However, its worst case is still `O(n^2)` when poor pivot choices repeatedly create very uneven
partitions.

In practice, the saved Quickselect results show both the strength and the
limitation of this implementation. At size `250`, Quickselect completes in
`0.073292 ms` on `partially_sorted` data and `0.085875 ms` on `random` data,
but slows to `1.615583 ms` on `sorted` data and `1.375250 ms` on
`reverse_sorted` data. These results show that the deterministic rightmost
pivot used in this project is good for trace reproducibility, but it creates
clear weak cases on highly ordered inputs.

One more practical point is important. The built-in Python `sorted` baseline is
still faster than the custom Python implementations in the saved bubble quickselect
module lab benchmark results. That does not mean the algorithm analysis is wrong. Instead, it shows
that an asymptotically favorable idea can still lose to a highly optimized
library implementation in measured runtime. Taken together, the sorting and
selection section shows that the best choice depends on whether the task is
full sorting, one-rank selection, classroom traceability, or raw runtime
performance (CSU Global, n.d.-a; CSU Global, n.d.-e).

## Sets: Uniqueness, Static Operations, Dynamic Mutations

Sets are important in computer science because they solve a different kind of
problem from lists, queues, or trees. A set is useful when the main goal is to
store unique values, support membership checks, and build derived
relationships between collections. Sets can be defined as unordered collections of unique
items and emphasize that they are centered on membership rather than position 
(CSU Global, n.d.-e).

In this project, that definition directly shapes the `CourseSet`
implementation. The chosen design preserves first-seen order for readability by
using a dictionary-backed structure, but the main algorithmic behavior is still
set behavior. A value is either present or absent. Duplicates do not create new
entries. This means the key practical benefit is semantic clarity rather than
ordered access.

From a Big-O perspective, the Set ADT has two different behavior groups.
Dynamic operations such as `add` and `remove` mutate one target set and
typically run in average `O(1)` time because the implementation is hash-backed.
Static operations such as `union`, `intersection`, `difference`, and
`symmetric_difference` create new derived sets and usually require `O(n + m)`
work because the values of both operands need to be examined (CSU Global,
n.d.-e). This difference between membership maintenance and derived-result
construction is one of the most important lessons from the set section.

In practice, the set discussion in the integrated portfolio is more theoretical
and behavioral than timing-heavy. The saved benchmark CSV focuses on
Bubble Sort and Quickselect rather than on a separate set benchmark suite. Even
so, sets still make an important contribution to the overall analysis. They
show that not every performance question begins with ordering. Some workloads
depend more on uniqueness, membership, and collection relationships than on
position, rank, or traversal order.

These results and definitions support a clear recommendation. Use sets when the
problem depends on uniqueness, membership, or set algebra. Avoid them when the
main goal is sorted order, index-based access, or rank selection. In other
words, sets are a strong complement to the search and sorting modules because
they optimize a different kind of data question (CSU Global, n.d.-e).

## Linked Structures: Stack, Queue, Deque, Linked List

Linked structures are important because they show how different abstract data
types support different access patterns. In this portfolio, the linked
structures module includes a list-backed `Stack`, `Queue`, and `Deque`, plus a
custom doubly linked `LinkedList`. The purpose of this section is to examine
how those structures behave both theoretically and practically when they are
used for build, drain, search, and delete workloads.

It is important to note that the same abstract data type can behave very
differently depending on how it is implemented. Stacks, queues, deques, and 
linked lists can all support linear organization, but the underlying storage 
model determines whether operations stay efficient or become shift- or 
traversal-heavy (Lysecky & Vahid, 2019a). The saved benchmark results support 
that point clearly.

From a Big-O perspective, Stack is the most favorable structure in 
the Linked Structures module for repeated endpoint work. Its list-backed `push` 
and `pop` operations stay on the favorable end of the Python list, so the full 
workload remains close to linear overall. Queue and Deque are more mixed. In this 
implementation, some paths require repeated shifting because work happens on the 
unfavorable end of a Python list. LinkedList avoids that shifting cost, but 
traversal-heavy operations still grow with list length.

In practice, the saved results show those differences clearly. Average
`common_build` time is `0.780875 ms` for Stack, `92.360011 ms` for Queue, and
`92.272156 ms` for Deque. At `50,000` items, labs reesutl from the Linked Structures 
module show `351.2580 ms` for `Queue.enqueue`, `344.5407 ms` for `Deque.addRear_build`, 
and only `2.3620 ms` for `Stack.push`. Deque also shows strong end asymmetry: 
`addFront_build` at `50,000` items takes `1.5538 ms`, while `addRear_build` takes 
`344.5407 ms`. These results show that the same structure can look very different 
depending on which end receives most of the work.

LinkedList adds the node-based view to the comparison. It is slower than Stack
for simple bulk build, but it avoids the front-shifting penalties of the
list-backed Queue and Deque. It is strongest when cached endpoints can be used
directly. For example, `delete_head_single` remains effectively constant, while
`search_middle`, `delete_middle_single`, and `delete_tail_single` all grow with
traversal length. In practical terms, the linked structures module shows that
implementation details matter just as much as the ADT name when making
performance claims (Lysecky & Vahid, 2019a).

## Trees and Maps: BST, TreeMap, ListMap

Trees and maps are important because they combine key-based lookup with ordered
structure. In this portfolio, the tree map section compares a plain
`BinarySearchTree`, a BST-backed `TreeMap`, and a list-backed `ListMap`
baseline. The main purpose of this section is to show how tree shape changes
performance, even when the same basic BST rules are used.

It is important to note that the same BST idea can behave very differently
depending on insertion order. When the inserted keys keep the tree relatively
short, search follows a limited root-to-leaf path. When the keys are inserted
in sorted order, the tree can become heavily skewed and behave much more like a
linked list (CSU Global, n.d.-c; Tutorials Point, n.d.-a; Tutorials Point,
n.d.-d). The saved benchmark results support that point clearly.

From a Big-O perspective, a plain BST has two different performance stories.
Insert, search, delete, minimum, and maximum are all `O(h)`, where `h` is the
tree height. When the tree stays reasonably short, this is close to `O(log n)`.
When the tree becomes badly skewed, the same operations move toward `O(n)`.
`ListMap.search`, by contrast, stays at `O(n)` because it performs a linear
scan. That means TreeMap can be much better than ListMap, but only when the BST
shape remains favorable.

In practice, the saved results make that difference easy to see. Under
`random_insertion`, the BST height reaches `19` at `500` items, and the largest
saved random benchmark shows a maximum `TreeMap` speedup of `21.737x` relative
to `ListMap`. Under `sorted_insertion`, the same BST reaches height `499` at
`500` items and loses badly to `ListMap`. The benchmark data
also shows that when all saved workloads are pooled together, `TreeMap`
averages `1.589451 ms` on hit queries and `ListMap` averages `1.009202 ms`.
These results show that a plain BST is not self-correcting. Its practical value
depends strongly on tree shape.

In practical terms, this section supports a clear recommendation. Use tree-
backed maps when ordered traversal, minimum/maximum lookup, or faster-than-
linear search are important and insertion order is unlikely to create severe
skew. Use a simpler linear map when the dataset is small or when the tree is
likely to collapse toward chain-like behavior. Overall, the tree and map
section shows that asymptotic potential only becomes practical when the
structure stays close enough to its intended shape (CSU Global, n.d.-c;
Tutorials Point, n.d.-a).

## Hash Tables and Priority Queues

Hash tables and priority queues are important because they solve different
kinds of retrieval problems. A hash table is used when the main goal is fast
key-based lookup. A priority queue is used when the main goal is to repeatedly
remove the highest-priority or lowest-priority item. In the integrated
portfolio, this section combines the hash priority module's written analysis 
with the copied benchmark artifacts from the same module.

It is important to note that the same data structure idea can behave very
differently depending on how it is implemented. Hash tables depend heavily on
hash quality and collision behavior, while heaps depend on maintaining
parent-child ordering in a nearly complete binary tree (CSU Global, n.d.-b;
Lysecky & Vahid, 2019b). The saved benchmark results support that point
clearly. In particular, they show how strongly collision buildup and full
linear scans influence real performance.

From a Big-O perspective, the hash table is the strongest general lookup
structure in this portfolio under healthy conditions. Insert, search, and
delete are all average-case `O(1)` because the workload usually only needs one
bucket and a short chain. The worst case is still `O(n)` because too many keys
can fall into the same bucket. The hash-table reference explains why this kind
of associative storage can be very fast when indexing is computed effectively
(Tutorials Point, n.d.-c).

In practice, the saved results strongly support that description. At `10,000`
items, hash-table search finishes in roughly `0.2616 ms` for hits,
`0.3534 ms` for misses, and `0.3125 ms` for mixed queries. Over the same
workload sizes and query modes, the linear-search baseline requires
`36.4574 ms`, `70.2530 ms`, and `54.5457 ms`. These results show that the hash
table is the strongest lookup structure in the portfolio when the key
distribution is healthy.

The collision results are just as important because they show the limit of
hashing. Forced-collision search hits at size `100` already rise to
`0.83593 us` average per query with `95` collisions recorded, and the CTA-5
analysis shows that this becomes much worse at larger sizes. Separate chaining
preserves correctness, but it does not remove the cost of very poor bucket
distribution. In practical terms, the hash table is extremely strong, but only
when the hash function and collision distribution remain favorable (CSU Global,
n.d.-b; Lysecky & Vahid, 2019b).

Priority queues show a different pattern. From a Big-O perspective, `peek`
remains `O(1)`, while insert and `extract_top` are `O(log n)` because the heap
only needs to restore order along one path. Search-by-label and delete-by-label
are still `O(n)` because the heap property does not provide direct access to an
arbitrary item. In practice, the saved results show that clearly. At `10,000`
items, `insert_bulk` stays near `4.3` to `4.4 ms`, `peek` remains effectively
constant at `0.000034 ms`, and `search_misses` rises to about `70.2 ms`. These
results show that the priority queue is very effective when the workload needs
root access, but much less effective when the workload needs general lookup.

## Graphs: Representations, BFS, DFS, Dijkstra

Graphs are important because they model relationships between objects. In this
portfolio, the graph module compares two graph representations,
`AdjacencyListGraph` and `AdjacencyMatrixGraph`, and also evaluates BFS, DFS,
Dijkstra, and Bellman-Ford. The purpose of this section is to show how graph
density, representation choice, and edge rules affect both performance and
correctness.

It is important to note that representation choice depends strongly on the
workload. The list-based model stores real neighbor relationships, which makes
it a strong fit for sparse graphs. The matrix-based model allocates a
row-column position for each source-target pair, which can help in dense,
stable workloads where direct edge checks are common (CSU Global, n.d.-d;
Lysecky & Vahid, 2019c). The saved benchmark results support that point
clearly.

From a Big-O perspective, adjacency-list storage uses `O(V + E)` space, while
adjacency-matrix storage uses `O(V^2)` space. BFS and DFS fit naturally with
the list-based model because traversal requests the stored neighbors of the
current vertex instead of scanning many empty relationships. Matrix storage has
a clear theoretical advantage for direct adjacency checks because a known
source-target pair can be checked in `O(1)` time (CSU Global, n.d.-d; Lysecky &
Vahid, 2019c).

In practice, the saved graph results strongly favor adjacency lists on sparse
workloads. The list-based representation wins `23` of `24` sparse
operation-size buckets. At `100` sparse vertices, the saved results show
list-based storage winning build, neighbor scan, BFS, DFS, Dijkstra,
Bellman-Ford, and edge removal. The matrix remains important, but it is more
specialized. The dense saved workloads show that it can become competitive or
superior for some shortest-path cases, especially dense Dijkstra and dense
Bellman-Ford at the largest benchmark size.

The algorithm layer adds an important correctness lesson. BFS and DFS are both
traversal tools, but they visit vertices in different orders. Dijkstra and
Bellman-Ford are both shortest-path tools, but they are not interchangeable.
The saved CTA-7 analysis uses Dijkstra for the positive-weight Denver-to-Vail
route and Bellman-Ford for the negative-cost demo because correctness depends
on the edge rules, not just on speed (Rao & Murugan, 2019). In practical
terms, the graph section shows that the best-performing representation or
algorithm only matters after the chosen method is valid for the graph's density
and edge semantics.

## Cross-Module Benchmark and Big-O Comparison

Big-O notation is useful in this integrated portfolio because it explains why
the benchmark rankings are not accidental. Lower-growth algorithms and better-
aligned structures usually scale better, but the saved artifacts also show that
input order, tree shape, collision behavior, and graph density can change the
practical result. The table below summarizes the dominant operation model for
each major area of the portfolio.

**Table 1**  
*Cross-Module Benchmark and Big-O Comparison Summary*

| Domain             | Structure or Algorithm            | Typical Strength                                | Typical Cost Model                                   | Main Limitation                         | Practical Signal from Saved Artifacts                           |
|--------------------|-----------------------------------|-------------------------------------------------|------------------------------------------------------|-----------------------------------------|-----------------------------------------------------------------|
| Search             | Linear search                     | Works on unsorted data immediately              | `O(n)`                                               | Scales directly with dataset size       | `50,000` comparisons at `50,000` items                          |
| Search             | Binary search                     | Repeated search on sorted data                  | `O(log n)`                                           | Requires sorted order                   | `16` comparisons at `50,000` items                              |
| Sorting            | Bubble Sort                       | Traceable full sorting with early exit          | Best `O(n)`, average/worst `O(n^2)`                  | Very sensitive to unsorted input        | `3.828625 ms` on reverse-sorted size `250`                      |
| Sorting            | Merge Sort                        | Large full-sort workloads                       | `O(n log n)`                                         | More complex than elementary sorts      | `21.2856 ms` on CTA-3 random size `10,000`                      |
| Selection          | Quickselect                       | Find one rank without full sort                 | Average `O(n)`, worst `O(n^2)`                       | Pivot sensitivity                       | `0.085875 ms` random vs `1.615583 ms` sorted at size `250`      |
| Sets               | `CourseSet` membership            | Uniqueness and membership                       | Average `O(1)`                                       | Depends on hashing quality              | Behavioral strength rather than dedicated timing suite          |
| Sets               | Union / intersection / difference | Derived relationships between collections       | `O(n + m)`                                           | Must scan both operands                 | Best when semantics matter more than order                      |
| Linked Structures  | Stack                             | Recent-item access                              | `push/pop` friendly, workload close to `O(n)` total  | Not FIFO                                | Fastest common-build performer in linked structures module labs |
| Linked Structures  | Queue                             | FIFO removal semantics                          | Build can degrade to `O(n^2)` in this implementation | Front-shifting build cost               | `351.2580 ms` enqueue at `50,000`                               |
| Linked Structures  | Deque                             | Two-end access                                  | End-dependent; mixed `O(n)` and `O(n^2)`             | Same ADT, very different end costs      | `addFront_build` far faster than `addRear_build`                |
| Linked Structures  | LinkedList                        | Endpoint mutation without shifting              | Traversal-heavy operations `O(n)`                    | Middle access requires traversal        | Strong endpoint delete, weaker search and tail delete           |
| Trees / Maps       | BST / TreeMap                     | Ordered search and traversal                    | Typical `O(log n)` if height stays short             | Can degrade to `O(n)` when skewed       | Up to `21.737x` speedup over `ListMap` when shape is favorable  |
| Trees / Maps       | ListMap                           | Simple linear baseline                          | `O(n)`                                               | No structural speedup                   | Beats skewed TreeMap under sorted insertion                     |
| Hashing            | Hash table                        | Direct key lookup                               | Average `O(1)`                                       | Collisions can push toward `O(n)`       | Strongest lookup structure in healthy distributions             |
| Priority           | Binary heap priority queue        | Repeated root access                            | `peek O(1)`, insert/extract `O(log n)`               | Arbitrary label search is `O(n)`        | Excellent for top-priority removal, weak for general lookup     |
| Graphs             | Adjacency list                    | Sparse graph storage and traversal              | Space `O(V + E)`                                     | Less specialized for direct pair checks | Wins `23/24` sparse benchmark buckets                           |
| Graphs             | Adjacency matrix                  | Direct edge checks and selected dense workloads | Space `O(V^2)`                                       | Pays for all possible pairs             | Competitive in selected dense shortest-path workloads           |

*Note*: This table summarizes the dominant strength, cost model, and practical
limitation for each major structure or algorithm area,

Table 1 shows two important patterns. First, no single complexity class
dominates every area of the portfolio because the modules solve different kinds
of problems. Second, the strongest practical performers are the structures that
align closely with the main workload. Binary search is strongest for repeated
search on sorted data. Hash tables are strongest for direct key lookup. Heaps
are strongest for repeated top-priority access. Adjacency lists are strongest
for sparse traversal-heavy graphs. These patterns match the practical
recommendations made throughout the earlier modules.

## Practical Recommendation Matrix

The integrated benchmark evidence can also be translated into a workload-first
recommendation guide. The matrix below summarizes which structure or algorithm
is the best fit for common workload types.

**Table 2**  
*Practical Recommendation Matrix for Integrated Portfolio Workloads*

| Workload type                                                      | Recommended choice                                       | Why it fits                                              | Avoid when                                                           |
|--------------------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------|----------------------------------------------------------------------|
| One or two searches on small or unsorted data                      | Linear search                                            | No preprocessing required                                | Repeated search on large static data                                 |
| Repeated search on sorted or sortable static data                  | Binary search                                            | Logarithmic search growth                                | Data changes constantly or sorting cost dominates                    |
| Need a full sorted result for large datasets                       | Merge Sort or built-in `sorted` context                  | Near `O(n log n)` scaling                                | Classroom tracing is the primary goal                                |
| Need to teach or inspect adjacent-swap mechanics                   | Bubble Sort                                              | Transparent step-by-step behavior                        | Performance matters on unsorted medium or large data                 |
| Need only the `k`th smallest item                                  | `CourseSet`                                              | Natural match for unique-value semantics                 | Index order, rank, or traversal order is central                     |
| Need LIFO behavior                                                 | Stack                                                    | Strong endpoint operations                               | FIFO or double-ended access is required                              |
| Need FIFO behavior with this codebase                              | Queue only when semantics matter more than build speed   | Correct abstraction despite costly build path            | Large bulk-build workloads in the current list-backed implementation |
| Need flexible two-end access                                       | Deque, but favor the efficient end paths                 | Supports both ends in one abstraction                    | Symmetric performance at both ends is assumed                        |
| Need node-based endpoint mutation without list shifting            | LinkedList                                               | Good endpoint behavior and structural clarity            | Frequent middle access or arbitrary search dominates                 |
| Need ordered lookup plus traversal/min/max                         | TreeMap or BST-backed map                                | Provides search and ordering together                    | Insert order is likely to skew the plain BST badly                   |
| Need the fastest general key lookup                                | Hash table                                               | Average-case constant-time search                        | Bucket distribution is poor or keys are adversarial                  |
| Need repeated next-highest or next-lowest removal                  | Binary heap priority queue                               | Root access is the optimized path                        | Arbitrary key lookup is the main task                                |
| Need sparse graph storage and traversal                            | Adjacency list                                           | Stores only real neighbors and wins most saved workloads | Constant pair checks on a stable dense graph dominate                |
| Need dense graph pair checks or selected dense shortest-path cases | Adjacency matrix                                         | Direct access to source-target cells                     | Memory cost and sparse emptiness dominate                            |

*Note*: This matrix translates the saved benchmark results and Big-O analysis
into workload-based recommendations for when each structure or algorithm is the
best fit in the integrated portfolio.

In practical terms, the matrix supports one clear course-level lesson. The best
choice is almost never "the most advanced structure." The better rule is to
choose the structure whose strongest operation matches the operation that the
workload repeats the most. That is the clearest recommendation the integrated
portfolio provides.

## Conclusion and References

The results of the integrated portfolio show that the chosen algorithms and
data structures behave the way algorithm analysis predicts. Search becomes much
faster when sorted order is available. Quadratic sorting becomes expensive
quickly on larger unsorted data. Quickselect is better suited for rank
selection than full ordering. Sets are strongest when uniqueness and membership
are central. Hash tables are strongest for key-based lookup when collisions are
limited. Tree-backed maps perform well when shape remains healthy, and graph
representations behave differently depending on density and edge rules.

At the same time, the saved benchmark results show that theory is only part of
the story. Input order, implementation details, collision distribution, tree
shape, and graph density all change the practical outcome. In other words, the
best choice depends not only on Big-O notation, but also on what the workload
does most often and on how the structure is actually implemented in code.

Taken together, the integrated modules show the main lesson of the CSC506 course.
The most useful question is not simply "Which algorithm is best?" The more
useful question is "Which algorithm or data structure is the best fit for this
data, this access pattern, and this implementation context?"

### References

CSU Global. (n.d.-a). *Lecture 3 - Sorting Algorithms* [Course lecture notes].
CSC506 - Design and Analysis of Algorithms. Canvas.

CSU Global. (n.d.-b). *Lecture 5: Hash tables, heaps, and treaps*
[Interactive lecture]. CSC506 - Design and Analysis of Algorithms. Canvas.

CSU Global. (n.d.-c). *Lecture 6: Comprehensive study of trees*
[Course lecture]. CSC506 - Design and Analysis of Algorithms. Canvas.

CSU Global. (n.d.-d). *Lecture 7: Graphs* [Course lecture]. CSC506 - Design
and Analysis of Algorithms. Canvas.

CSU Global. (n.d.-e). *Lecture 8: Sets and additional sorts* [Course lecture].
CSC506 - Design and Analysis of Algorithms. Canvas.

GeeksforGeeks. (2026, February 28). *Big O notation*.
https://www.geeksforgeeks.org/dsa/analysis-algorithms-big-o-analysis/

Lysecky, R., & Vahid, F. (2019a). *Module 4: Lists, stacks, and queues*.
Data structures essentials: Pseudocode with Python examples. zyBooks.

Lysecky, R., & Vahid, F. (2019b). *Module 5: Hash tables, heaps, and treaps*.
Data structures essentials: Pseudocode with Python examples. zyBooks.

Lysecky, R., & Vahid, F. (2019c). *Module 7: Graphs*. Data structures
essentials: Pseudocode with Python examples. zyBooks.

Rao, K. P. K., & Murugan, T. S. (2019). An efficient routing algorithm for
software defined networking using Bellman Ford algorithm. *International
Journal of Online Engineering, 15*(14), 87-95.
https://doi.org/10.3991/ijoe.v15i14.11546

Ricciardi, A. (2024, August 28). *Big-Oh notation: Key to evaluating algorithm
efficiency*. Omega.py.
https://www.alexomegapy.com/post/big-oh-notation

Tutorials Point. (n.d.-a). *Binary Search Tree*. Tutorials Point.
https://www.tutorialspoint.com/data_structures_algorithms/binary_search_tree.htm

Tutorials Point. (n.d.-b). *Bubble sort algorithm*. Tutorials Point.
https://www.tutorialspoint.com/data_structures_algorithms/bubble_sort_algorithm.htm

Tutorials Point. (n.d.-c). *Hash table data structure*. Tutorials Point.
https://www.tutorialspoint.com/data_structures_algorithms/hash_data_structure.htm

Tutorials Point. (n.d.-d). *Tree Data Structure*. Tutorials Point.
https://www.tutorialspoint.com/data_structures_algorithms/tree_data_structure.htm
