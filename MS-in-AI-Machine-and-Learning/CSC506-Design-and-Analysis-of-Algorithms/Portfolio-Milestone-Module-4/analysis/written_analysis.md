# Data Structure Performance Analysis

## Overview

Linear data structures are important in computer science because they determine how data is stored, inserted, removed, and traversed. Stacks, queues, deques, and linked lists are often studied not only as programming exercises, but also as examples of how implementation choices affect runtime, memory usage, and scalability. In this project, four structures were implemented and tested: `Stack`, `Queue`, `Deque`, and a custom doubly linked `LinkedList`.

The purpose of this analysis is to examine how each structure behaves both theoretically and practically. Theoretical analysis uses Big-O notation to describe how performance grows as input size `n` increases. Practical analysis uses benchmark results collected from the Benchmark Lab feature across several operation groups, including common build, common drain, peek/front, deque-only operations, and linked-list-only operations. The benchmark sizes used in the generated report are `1,000`, `5,000`, `10,000`, and `50,000` elements, which makes it possible to observe how quickly performance differences widen as the workload becomes larger.

It is important to note that the same abstract data type can behave very differently depending on how it is implemented. The Module 4 materials explain that stacks, queues, deques, and linked lists can be built in more than one way, and the benchmark results in this project support that point clearly (Lysecky & Vahid, 2019). In particular, the results show how strongly list shifting, cached endpoint access, and full traversal influence real performance.

---

## Stack

A stack follows the last-in, first-out (LIFO) rule, which means the most recently inserted value is the first one removed. The stack reference identifies `push()`, `pop()`, and `peek()` as the fundamental stack operations and emphasizes that all activity occurs at the top of the structure (*Stack Data Structure*, n.d.). In this project, the stack is implemented with a Python list, so those operations stay focused on one favorable end of the underlying structure.

From a Big-O perspective, stack operations are very favorable in this implementation. Repeated `push` operations produce a linear build workload, repeated `pop` operations produce a linear drain workload, and `peek` remains constant time because it only reads the top item. Those are exactly the kinds of operation patterns that stacks are designed to support.

In practice, Stack is the strongest general performer in the common build group. `Stack.push` is the fastest common build operation at every tested size, increasing from `0.0484 ms` at `1,000` items to `2.3620 ms` at `50,000` items. `Stack.pop` also remains highly competitive in the common drain workload, finishing the `50,000`-item drain in `5.6118 ms`. These results show that Stack is an excellent choice when the workload only needs recent-item access.

---

## Queue

A queue follows the first-in, first-out (FIFO) rule, so the earliest inserted item is the first one removed. The queue reference describes `enqueue()`, `dequeue()`, and `peek()` as the basic operations and explains that data enters at one end and leaves through the other (TutorialsPoint, n.d.-c). Additionally, in an array-based queue, enqueue can be `O(N)` while dequeue remains `O(1)` (Lysecky & Vahid, 2019).

From a Big-O perspective, Queue is more mixed in this project than Stack. The common drain workload remains linear because each `dequeue` removes one item at a time, and `front` remains constant time because it only reads the next value to be removed. However, the common build workload is much more expensive because each `enqueue` shifts existing elements in the internal list.

The benchmark results strongly support that description. At `50,000` items, `Queue.enqueue` requires `351.2580 ms`, while `Queue.dequeue` requires only `5.4459 ms`. Compared with the `Stack.push` common build time of `2.3620 ms`, the queue build is `148.7x` slower at the largest tested size. This does not mean FIFO is a weak abstraction. It means this specific list-backed implementation pays a large shifting cost as the workload grows.

---

## Deque

A deque, or double-ended queue, allows insertion and removal at both the front and the back. The course materials describe `PushFront`, `PushBack`, `PopFront`, `PopBack`, `PeekFront`, and `PeekBack` as common deque operations and explain that a deque can be implemented with either an array or a linked list (Lysecky & Vahid, 2019). That makes deque more flexible than stack or queue, but it does not guarantee equal performance at both ends.

From a Big-O perspective, Deque is the most asymmetric structure in the project. Some operations stay close to the favorable end of the list and perform well, while others force repeated shifting and become much slower. That difference is especially important because deque exposes both-end operations directly.

The benchmark results show that this asymmetry is very large in practice. At `50,000` items, `Deque.addFront_build` completes in `1.5538 ms`, while `Deque.addRear_build` takes `344.5407 ms`, making the rear build workload `221.7x` slower. The same pattern appears in removal: `Deque.removeFront_drain` completes in `4.2062 ms`, but `Deque.removeRear_drain` requires `155.3099 ms`, which is `36.9x` slower. These results make it clear that having access to both ends is not the same as getting the same cost at both ends.

---

## LinkedList

A linked list stores data in nodes connected by pointers rather than in contiguous array slots. The linked-list reference explains that nodes are connected through links, that the structure begins at a head node and ends at a tail node, and that linked lists do not require contiguous memory (TutorialsPoint, n.d.-b). The doubly linked list reference adds that each node stores both `next` and `prev` links, which makes forward and backward traversal possible (TutorialsPoint, n.d.-a).

From a Big-O perspective, LinkedList is strongest when it can use cached endpoint access and weaker when it has to traverse the structure. `insert_rear` and `delete_head` support linear full workloads well, while positional delete and search operations still depend on how far the traversal must travel through the list.

In practice, the custom `LinkedList` provides the clearest contrast with the list-backed structures because it is the only node-based implementation in the project. `LinkedList.insert_rear` reaches `13.4627 ms` at `50,000` items, which is still far better than the slow front-shifting builds in Queue and Deque. The most dramatic result appears in the single-delete workloads: `delete_head_single` takes only `0.0007 ms` at `50,000` items, while `delete_middle_single` takes `0.6257 ms` and `delete_tail_single` takes `1.2615 ms`. Search results show the same pattern. At `50,000` items, `search_middle` takes `0.6186 ms`, while `search_missing` takes `1.2122 ms` because the missing-value case must walk the full list before failing. These results confirm the main linked-list tradeoff: cached endpoint operations are very efficient, but middle access still requires traversal.

---

## Comparative Big-O Analysis

Big-O notation is useful in this project because it explains why the relative rankings in the benchmark data are not accidental. The course materials emphasize that array-based queue enqueue can be `O(N)` while dequeue remains `O(1)`, and that search and remove operations in an array-based list have worst-case `O(N)` behavior because items may need to be scanned or shifted (Lysecky & Vahid, 2019). Those same ideas appear in this project's benchmark results. Operations that stay on a favorable end of the underlying structure behave close to linear or constant time, while operations that trigger repeated shifts or traversals become much more expensive as `n` grows.

**Table 1**  
*Theoretical Complexity Comparison of the Data Structures in This Project*

| Structure       | Common Build                                    | Common Drain                                          | Peek / Front          | Search | Key implementation note                                                |
|-----------------|-------------------------------------------------|-------------------------------------------------------|-----------------------|--------|------------------------------------------------------------------------|
| Stack           | `O(n)`                                          | `O(n)`                                                | `O(1)`                | `O(n)` | Uses list-end `append()` / `pop()` for top-only access                 |
| Queue           | `O(n^2)`                                        | `O(n)`                                                | `O(1)`                | `O(n)` | `enqueue` inserts index `0`, every existing item shifts                |
| Deque           | `O(n)` with `addFront`, `O(n^2)` with `addRear` | `O(n)` with `removeFront`, `O(n^2)` with `removeRear` | `O(1)`                | `O(n)` | Both ends are available, but the chosen end changes the cost           |
| LinkedList      | `O(n)` with `insert_rear`                       | `O(n)` with `delete_head`                             | `O(1)` at cached ends | `O(n)` | Cached `head` / `tail` help endpoint work; middle work still traverses |

*Note*: The table reflects the course-aligned implementations used in this project, not every possible implementation of the same ADTs.

Table 1 illustrates the scaling patterns imparted from the Benchmark Lab results stored in the benchmark CSV. It shows that when the dataset size grows from `1,000` to `50,000`, `Stack.push` grows by `48.8x`, `LinkedList.insert_rear` by `53.8x`, and `Deque.addFront_build` by `47.9x`. This is close to a linear growth behavior for a `50x` larger dataset. On the other hand, `Queue.enqueue` grows by `1,765.5x`, `Deque.addRear` by `1,781.9x`, and `Deque.addRear_build` by `1,888.8x`. These larger growth behaviors are what should be expected when a workload has an internal shifting cost, that is, when shifting elements is required for insertion or deletion.

---

## Benchmark Results 

The benchmark lab feature measured runtime for every operation group at sizes `1,000`, `5,000`, `10,000`, and `50,000`. 

### Operation Groups

- Common Build is a bulk insertion process that is used to measure how fast each structure can fill itself up from empty using its normal add operation (`Stack.push`, `Queue.enqueue`, `Deque.addRear`, `LinkedList.insert_rear`).
- Common Drain is bulk removal process that is used to measure how fast each structure can empty itself out using its normal remove operation (`Stack.pop`, `Queue.dequeue`, `Deque.removeFront`, `LinkedList.delete_head`).
- Peek / Front is an operation that reads the next element to be removed without removing it.
- Deque Ends is an operation that inserts or removes elements from both ends of the deque.
- LinkedList Delete / Search / Display is an operation that deletes, searches, or displays elements in the linked list.

**Table 2**  
*Benchmark Results for All Structure Workloads*

| Structure  | Operation             | Group              | Size   | Time (ms) | Big-O  | Correct |
|------------|-----------------------|--------------------|--------|-----------|--------|---------|
| Deque      | addRear               | Common Build       | 1,000  | 0.1969    | O(n^2) | Yes     |
| LinkedList | insert_rear           | Common Build       | 1,000  | 0.2504    | O(n)   | Yes     |
| Queue      | enqueue               | Common Build       | 1,000  | 0.1990    | O(n^2) | Yes     |
| Stack      | push                  | Common Build       | 1,000  | 0.0484    | O(n)   | Yes     |
| Deque      | removeFront           | Common Drain       | 1,000  | 0.1293    | O(n)   | Yes     |
| LinkedList | delete_head           | Common Drain       | 1,000  | 0.2638    | O(n)   | Yes     |
| Queue      | dequeue               | Common Drain       | 1,000  | 0.1133    | O(n)   | Yes     |
| Stack      | pop                   | Common Drain       | 1,000  | 0.1089    | O(n)   | Yes     |
| Deque      | addFront_build        | Deque Ends         | 1,000  | 0.0325    | O(n)   | Yes     |
| Deque      | addRear_build         | Deque Ends         | 1,000  | 0.1824    | O(n^2) | Yes     |
| Deque      | removeFront_drain     | Deque Ends         | 1,000  | 0.0811    | O(n)   | Yes     |
| Deque      | removeRear_drain      | Deque Ends         | 1,000  | 0.1281    | O(n^2) | Yes     |
| LinkedList | delete_head_single    | LinkedList Delete  | 1,000  | 0.0003    | O(1)   | Yes     |
| LinkedList | delete_middle_single  | LinkedList Delete  | 1,000  | 0.0128    | O(n)   | Yes     |
| LinkedList | delete_missing_single | LinkedList Delete  | 1,000  | 0.0244    | O(n)   | Yes     |
| LinkedList | delete_tail_single    | LinkedList Delete  | 1,000  | 0.0251    | O(n)   | Yes     |
| LinkedList | display_forward       | LinkedList Display | 1,000  | 0.0265    | O(n)   | Yes     |
| LinkedList | display_reverse       | LinkedList Display | 1,000  | 0.0268    | O(n)   | Yes     |
| LinkedList | search_middle         | LinkedList Search  | 1,000  | 0.0125    | O(n)   | Yes     |
| LinkedList | search_missing        | LinkedList Search  | 1,000  | 0.0243    | O(n)   | Yes     |
| Deque      | peekFront             | Peek / Front       | 1,000  | 0.0001    | O(1)   | Yes     |
| Deque      | peekRear              | Peek / Front       | 1,000  | 0.0001    | O(1)   | Yes     |
| Queue      | front                 | Peek / Front       | 1,000  | 0.0001    | O(1)   | Yes     |
| Stack      | peek                  | Peek / Front       | 1,000  | 0.0001    | O(1)   | Yes     |
| Deque      | addRear               | Common Build       | 5,000  | 3.7225    | O(n^2) | Yes     |
| LinkedList | insert_rear           | Common Build       | 5,000  | 1.2686    | O(n)   | Yes     |
| Queue      | enqueue               | Common Build       | 5,000  | 3.7020    | O(n^2) | Yes     |
| Stack      | push                  | Common Build       | 5,000  | 0.2410    | O(n)   | Yes     |
| Deque      | removeFront           | Common Drain       | 5,000  | 0.5594    | O(n)   | Yes     |
| LinkedList | delete_head           | Common Drain       | 5,000  | 1.3070    | O(n)   | Yes     |
| Queue      | dequeue               | Common Drain       | 5,000  | 0.5635    | O(n)   | Yes     |
| Stack      | pop                   | Common Drain       | 5,000  | 0.5602    | O(n)   | Yes     |
| Deque      | addFront_build        | Deque Ends         | 5,000  | 0.1540    | O(n)   | Yes     |
| Deque      | addRear_build         | Deque Ends         | 5,000  | 3.7006    | O(n^2) | Yes     |
| Deque      | removeFront_drain     | Deque Ends         | 5,000  | 0.4141    | O(n)   | Yes     |
| Deque      | removeRear_drain      | Deque Ends         | 5,000  | 1.5046    | O(n^2) | Yes     |
| LinkedList | delete_head_single    | LinkedList Delete  | 5,000  | 0.0004    | O(1)   | Yes     |
| LinkedList | delete_middle_single  | LinkedList Delete  | 5,000  | 0.0629    | O(n)   | Yes     |
| LinkedList | delete_missing_single | LinkedList Delete  | 5,000  | 0.1191    | O(n)   | Yes     |
| LinkedList | delete_tail_single    | LinkedList Delete  | 5,000  | 0.1237    | O(n)   | Yes     |
| LinkedList | display_forward       | LinkedList Display | 5,000  | 0.1277    | O(n)   | Yes     |
| LinkedList | display_reverse       | LinkedList Display | 5,000  | 0.1283    | O(n)   | Yes     |
| LinkedList | search_middle         | LinkedList Search  | 5,000  | 0.0616    | O(n)   | Yes     |
| LinkedList | search_missing        | LinkedList Search  | 5,000  | 0.1205    | O(n)   | Yes     |
| Deque      | peekFront             | Peek / Front       | 5,000  | 0.0001    | O(1)   | Yes     |
| Deque      | peekRear              | Peek / Front       | 5,000  | 0.0001    | O(1)   | Yes     |
| Queue      | front                 | Peek / Front       | 5,000  | 0.0001    | O(1)   | Yes     |
| Stack      | peek                  | Peek / Front       | 5,000  | 0.0001    | O(1)   | Yes     |
| Deque      | addRear               | Common Build       | 10,000 | 14.3594   | O(n^2) | Yes     |
| LinkedList | insert_rear           | Common Build       | 10,000 | 2.6037    | O(n)   | Yes     |
| Queue      | enqueue               | Common Build       | 10,000 | 14.2810   | O(n^2) | Yes     |
| Stack      | push                  | Common Build       | 10,000 | 0.4721    | O(n)   | Yes     |
| Deque      | removeFront           | Common Drain       | 10,000 | 1.1057    | O(n)   | Yes     |
| LinkedList | delete_head           | Common Drain       | 10,000 | 2.6531    | O(n)   | Yes     |
| Queue      | dequeue               | Common Drain       | 10,000 | 1.1008    | O(n)   | Yes     |
| Stack      | pop                   | Common Drain       | 10,000 | 1.0898    | O(n)   | Yes     |
| Deque      | addFront_build        | Deque Ends         | 10,000 | 0.3013    | O(n)   | Yes     |
| Deque      | addRear_build         | Deque Ends         | 10,000 | 14.0763   | O(n^2) | Yes     |
| Deque      | removeFront_drain     | Deque Ends         | 10,000 | 0.8363    | O(n)   | Yes     |
| Deque      | removeRear_drain      | Deque Ends         | 10,000 | 5.2333    | O(n^2) | Yes     |
| LinkedList | delete_head_single    | LinkedList Delete  | 10,000 | 0.0003    | O(1)   | Yes     |
| LinkedList | delete_middle_single  | LinkedList Delete  | 10,000 | 0.1217    | O(n)   | Yes     |
| LinkedList | delete_missing_single | LinkedList Delete  | 10,000 | 0.2393    | O(n)   | Yes     |
| LinkedList | delete_tail_single    | LinkedList Delete  | 10,000 | 0.2468    | O(n)   | Yes     |
| LinkedList | display_forward       | LinkedList Display | 10,000 | 0.2504    | O(n)   | Yes     |
| LinkedList | display_reverse       | LinkedList Display | 10,000 | 0.2495    | O(n)   | Yes     |
| LinkedList | search_middle         | LinkedList Search  | 10,000 | 0.1235    | O(n)   | Yes     |
| LinkedList | search_missing        | LinkedList Search  | 10,000 | 0.2385    | O(n)   | Yes     |
| Deque      | peekFront             | Peek / Front       | 10,000 | 0.0001    | O(1)   | Yes     |
| Deque      | peekRear              | Peek / Front       | 10,000 | 0.0001    | O(1)   | Yes     |
| Queue      | front                 | Peek / Front       | 10,000 | 0.0001    | O(1)   | Yes     |
| Stack      | peek                  | Peek / Front       | 10,000 | 0.0001    | O(1)   | Yes     |
| Deque      | addRear               | Common Build       | 50,000 | 350.8099  | O(n^2) | Yes     |
| LinkedList | insert_rear           | Common Build       | 50,000 | 13.4627   | O(n)   | Yes     |
| Queue      | enqueue               | Common Build       | 50,000 | 351.2580  | O(n^2) | Yes     |
| Stack      | push                  | Common Build       | 50,000 | 2.3620    | O(n)   | Yes     |
| Deque      | removeFront           | Common Drain       | 50,000 | 5.5740    | O(n)   | Yes     |
| LinkedList | delete_head           | Common Drain       | 50,000 | 12.6559   | O(n)   | Yes     |
| Queue      | dequeue               | Common Drain       | 50,000 | 5.4459    | O(n)   | Yes     |
| Stack      | pop                   | Common Drain       | 50,000 | 5.6118    | O(n)   | Yes     |
| Deque      | addFront_build        | Deque Ends         | 50,000 | 1.5538    | O(n)   | Yes     |
| Deque      | addRear_build         | Deque Ends         | 50,000 | 344.5407  | O(n^2) | Yes     |
| Deque      | removeFront_drain     | Deque Ends         | 50,000 | 4.2062    | O(n)   | Yes     |
| Deque      | removeRear_drain      | Deque Ends         | 50,000 | 155.3099  | O(n^2) | Yes     |
| LinkedList | delete_head_single    | LinkedList Delete  | 50,000 | 0.0007    | O(1)   | Yes     |
| LinkedList | delete_middle_single  | LinkedList Delete  | 50,000 | 0.6257    | O(n)   | Yes     |
| LinkedList | delete_missing_single | LinkedList Delete  | 50,000 | 1.2009    | O(n)   | Yes     |
| LinkedList | delete_tail_single    | LinkedList Delete  | 50,000 | 1.2615    | O(n)   | Yes     |
| LinkedList | display_forward       | LinkedList Display | 50,000 | 1.2252    | O(n)   | Yes     |
| LinkedList | display_reverse       | LinkedList Display | 50,000 | 1.2238    | O(n)   | Yes     |
| LinkedList | search_middle         | LinkedList Search  | 50,000 | 0.6186    | O(n)   | Yes     |
| LinkedList | search_missing        | LinkedList Search  | 50,000 | 1.2122    | O(n)   | Yes     |
| Deque      | peekFront             | Peek / Front       | 50,000 | 0.0001    | O(1)   | Yes     |
| Deque      | peekRear              | Peek / Front       | 50,000 | 0.0001    | O(1)   | Yes     |
| Queue      | front                 | Peek / Front       | 50,000 | 0.0001    | O(1)   | Yes     |
| Stack      | peek                  | Peek / Front       | 50,000 | 0.0001    | O(1)   | Yes     |

*Note*: The table is generated from `analysis/benchmark_results.csv`, which stores one row per `(structure, operation, size)` workload.

**Table 3**  
*Fastest Structure by Operation Group and Size*

| Operation Group    | Size    | Fastest Structure | Fastest Operation | Time (ms) | Runner-Up                       |
|--------------------|---------|-------------------|-------------------|-----------|---------------------------------|
| Common Build       | 1,000   | Stack             | push              | 0.0484    | Deque.addRear                   |
| Common Drain       | 1,000   | Stack             | pop               | 0.1089    | Queue.dequeue                   |
| Deque Ends         | 1,000   | Deque             | addFront_build    | 0.0325    | Deque.removeFront_drain         |
| LinkedList Delete  | 1,000   | LinkedList        | delete_head_single| 0.0003    | LinkedList.delete_middle_single |
| LinkedList Display | 1,000   | LinkedList        | display_forward   | 0.0265    | LinkedList.display_reverse      |
| LinkedList Search  | 1,000   | LinkedList        | search_middle     | 0.0125    | LinkedList.search_missing       |
| Peek / Front       | 1,000   | Deque             | peekRear          | 0.0001    | Deque.peekFront                 |
| Common Build       | 5,000   | Stack             | push              | 0.2410    | LinkedList.insert_rear          |
| Common Drain       | 5,000   | Deque             | removeFront       | 0.5594    | Stack.pop                       |
| Deque Ends         | 5,000   | Deque             | addFront_build    | 0.1540    | Deque.removeFront_drain         |
| LinkedList Delete  | 5,000   | LinkedList        | delete_head_single| 0.0004    | LinkedList.delete_middle_single |
| LinkedList Display | 5,000   | LinkedList        | display_forward   | 0.1277    | LinkedList.display_reverse      |
| LinkedList Search  | 5,000   | LinkedList        | search_middle     | 0.0616    | LinkedList.search_missing       |
| Peek / Front       | 5,000   | Deque             | peekRear          | 0.0001    | Stack.peek                      |
| Common Build       | 10,000  | Stack             | push              | 0.4721    | LinkedList.insert_rear          |
| Common Drain       | 10,000  | Stack             | pop               | 1.0898    | Queue.dequeue                   |
| Deque Ends         | 10,000  | Deque             | addFront_build    | 0.3013    | Deque.removeFront_drain         |
| LinkedList Delete  | 10,000  | LinkedList        | delete_head_single| 0.0003    | LinkedList.delete_middle_single |
| LinkedList Display | 10,000  | LinkedList        | display_reverse   | 0.2495    | LinkedList.display_forward      |
| LinkedList Search  | 10,000  | LinkedList        | search_middle     | 0.1235    | LinkedList.search_missing       |
| Peek / Front       | 10,000  | Deque             | peekRear          | 0.0001    | Stack.peek                      |
| Common Build       | 50,000  | Stack             | push              | 2.3620    | LinkedList.insert_rear          |
| Common Drain       | 50,000  | Queue             | dequeue           | 5.4459    | Deque.removeFront               |
| Deque Ends         | 50,000  | Deque             | addFront_build    | 1.5538    | Deque.removeFront_drain         |
| LinkedList Delete  | 50,000  | LinkedList        | delete_head_single| 0.0007    | LinkedList.delete_middle_single |
| LinkedList Display | 50,000  | LinkedList        | display_reverse   | 1.2238    | LinkedList.display_forward      |
| LinkedList Search  | 50,000  | LinkedList        | search_middle     | 0.6186    | LinkedList.search_missing       |
| Peek / Front       | 50,000  | Deque             | peekRear          | 0.0001    | Stack.peek                      |

*Note*: The table is generated from `analysis/operation_winners.csv`, which ranks the fastest recorded structure per operation group and dataset size.

**Figure 1**  
*Common operation runtime*

![](Portfolio-Milestone-Module-4/analysis/charts/common_operation_runtime.png)

*Note*: The common build and common drain chart makes the largest scaling gap in the project easy to see. `Stack.push` and `LinkedList.insert_rear` remain far below `Queue.enqueue` and `Deque.addRear` as size increases.

**Figure 2**  
*Structure-specific runtime*

![](Portfolio-Milestone-Module-4/analysis/charts/structure_specific_runtime.png)

*Note*: The structure-specific runtime chart highlights the internal asymmetry within Deque and the traversal-driven cost of LinkedList search, delete, and display workloads.

**Figure 3**  
*Fastest structure by operation group and size*

![](Portfolio-Milestone-Module-4/analysis/charts/operation_winner_heatmap.png)

*Note*: The heatmap confirms that Stack dominates common build, Deque dominates two-ended favorable-end workloads, and LinkedList dominates its own cached-head delete and related traversal scenarios.

**Figure 4**  
*Structure profile comparison*

![](Portfolio-Milestone-Module-4/analysis/charts/structure_profile_comparison.png)

*Note*: This figure summarizes the practical tradeoffs among the four structures and complements Table 1 by presenting the same ideas in a more visual comparison format.

The benchmark results show that Stack is the best general-purpose data structure in the common build group because all work is done on one end of the list. The Queue with its FIFO behavior, makes large build times expensive. Deque, on the other hand, makes operation choice matter, as one end, the front, performs very well, while the other, the rear, becomes much slower. Finally, LinkedList is most effective for endpoint access, avoids shifting all the elements when deleting or inserting, and uses node-based traversal for searching.

The common build results show that at `50,000` items, `Stack.push` finishes in `2.3620 ms`, `LinkedList.insert_rear` in `13.4627 ms`, `Deque.addRear` in `350.8099 ms`, and `Queue.enqueue` in `351.2580 ms`. This means the two shift-heavy builds are roughly `148x` slower than Stack at the largest tested size. That widening gap is exactly what Big-O analysis predicts.

On the other hand, the common drain results show that `Stack.pop`, `Queue.dequeue`, and `Deque.removeFront` have the same time range at `50,000` items, from `5.4459 ms` to `5.6118 ms`, while `LinkedList.delete_head` is slower at `12.6559 ms`. For peek operations, every structure stays constant, as times are clustered around `0.0001 ms`. These means that the structures can reach the needed value without needing to perform a full traversal or a large shifting of elements.

The linked-list-specific cases are especially useful because they separate endpoint, and from having to perform traversal-heavy work when the middle or tail of the list is accessed. `delete_head_single` is effectively constant at every size, but `delete_middle_single`, `delete_tail_single`, `search_middle`, and `search_missing` all grow with list size. This shows that theoretical complexity, Big-O notation analysis, gives expectations, while benchmark data shows explicitly where or when traversal times become significant.

---

## Conclusion

The analysis shows that choosing the best data structure depends on both theory and context, that is, the specific operations that will be performed on the data structure, and the requirements of a specific data application. Stack is the strongest option when access is limited to the most recently inserted item, the front. Queue is best suited for arrival-order processing matters; however, the benchmark results show that this list-backed front insertion approach scales poorly. Deque is highly flexible, but its benchmark results show that this both-end access does not eliminate the cost asymmetry, that is, the front of the deque is much faster to access than the rear. LinkedList is most useful when work happens at cached endpoints or when insertion and deletion matter more than direct indexed access, as it avoids the cost of shifting elements.

In practical terms, the Benchmark Lab results show that if the workload requires a LIFO (Last-In, First-Out) approach, choose Stack. If the workload is FIFO (First-In, First-Out), choose Queue. If both ends matter, Deque can be very effective, but only when the cheaper end, the front (if using a Python list as the underlying structure), is used consistently. If endpoint insertion, deletion, and traversal behavior (for searches) matter more than contiguous storage, LinkedList is a strong choice. Overall, Big-O analysis and benchmark testing work best together as theory explains the pattern, and measurement shows how large the difference becomes in real use.

An important note is that LinkedList can be used singly and doubly as an underlying structure for Queue and Deque Abstract Data Types, and they are often used in that manner in practice, as they are more efficient than using a Python list. 

---

## References

Lysecky, R., & Vahid, F. (2019).  Module 4: Lists, stacks, and queues. *Data structures essentials: Pseudocode with Python examples*. zyBooks

TutorialsPoint. (n.d.-a). *Doubly Linked List Data Structure*. TutorialsPoint. https://www.tutorialspoint.com/data_structures_algorithms/doubly_linked_list_algorithm.htm

TutorialsPoint. (n.d.-b). *Linked List Data Structure*. TutorialsPoint. https://www.tutorialspoint.com/data_structures_algorithms/linked_list_algorithms.htm

TutorialsPoint. (n.d.-c). *Queue Data Structure*. TutorialsPoint. https://www.tutorialspoint.com/data_structures_algorithms/dsa_queue.htm

TutorialsPoint. (n.d.-d). *Stack Data Structure*. TutorialsPoint. https://www.tutorialspoint.com/data_structures_algorithms/stack_algorithm.htm
