# Recommendation Guide: Choosing the Right Hashing Approach

## Overview

Choosing the right lookup approach depends on several factors, not on speed only. When choosing between perfect hashing, non-perfect hashing, a hash table, and linear search, it is important to consider whether the key set is fixed, whether new items will be added later, how collisions will be handled, and the cost as the dataset becomes larger. The CTA-5 Benchmark Lab compared `Hash Table` search against `Linear Search`, and the Hash Table Lab also makes collision behavior visible through normal and forced-collision demos. The dataset sizes ranged from `100` to `10,000`. Based on those benchmark results and the Hash Table Lab feature, this guide recommends when or in which instance each approach is best suited.

---

## When to Use Perfect Hashing

Perfect hashing is the better choice when:

1. If the workload uses a fixed key set that is fully known in advance. Perfect hashing is the best choice for this purpose because every valid key can be assigned to its own unique bucket.

2. If collision-free lookup is more important than flexibility. Perfect hashing is well suited for this purpose because it is designed so that the chosen keys do not collide.

3. If the problem fits cases such as **reserved keywords**, **fixed command names**, **small static ID ranges**, and other read-mostly lookup tables. Perfect hashing is useful for these kinds of problems because the data does not change often.

4. If construction cost can be paid once and reused many times later. Perfect hashing is useful in this kind of case because the mapping can be built ahead of time and then reused without change.

It is important to note that perfect hashing is not the best choice when new keys must be added later. If the key set changes, the original perfect hash function may no longer work and may need to be rebuilt.

Example: Suppose the only valid student IDs are `{101, 102, 103, 104, 105}`. A simple perfect hash function can be `h(id) = id - 101`. This maps `101` to bucket `0`, `102` to bucket `1`, `103` to bucket `2`, `104` to bucket `3`, and `105` to bucket `4`. This is useful because each key gets its own bucket and no collisions occur.

---

## When to Use Non-Perfect Hashing

Non-perfect hashing is the better choice when:

1. If the workload must handle dynamic data where keys are inserted, updated, and deleted over time. Non-perfect hashing is the best choice for this purpose because it remains flexible.

2. If the key set is not fully known ahead of time. General-purpose systems are better suited for non-perfect hashing because they need to accept new keys without rebuilding the entire lookup method.

3. If the problem fits cases such as **inventory systems**, **user records**, **customer accounts**, **caches**, and **general key-value storage**. These problems are better suited for non-perfect hashing because the data changes over time.

4. If collisions can be handled with a clear strategy. In CTA-5, separate chaining is the best choice for this purpose because colliding keys remain together in one bucket chain instead of replacing one another.

It is important to note that non-perfect hashing does not mean weak hashing. It only means that collisions are possible. A good non-perfect hash function can still give very strong average-case performance when the keys are distributed well.

Example: Consider the simple function `h(key) = sum(ord(ch) for ch in key) % 10`. The keys `"cat"` and `"act"` both produce the same sum, so both map to the same bucket. This is a collision. CTA-5 uses a position-weighted string hash to reduce that kind of collision, but the function is still non-perfect because different keys can still map to the same bucket.

---

## When to Use a Hash Table Instead of Linear Search

A hash table is the better choice than linear search when:

1. If the workload performs repeated lookups on the same dataset. A hash table is the best choice for this purpose because it avoids scanning every element one by one.

2. If the dataset becomes moderately large. In the Benchmark Lab, the performance gap widened quickly as size increased from `100` to `10,000`.

3. If misses are common. A hash table is the best choice for this purpose because a miss usually checks only one bucket chain, while linear search may inspect the entire dataset before failing.

4. If key-based access is the main operation. The CTA-5 hash table is well suited for this purpose because it is built specifically for key-value lookup.

It is important to note that the Benchmark Lab strongly supports this recommendation. At `100` items, hash-table search was already faster, with speedups from about `1.90x` to `2.11x`. At `10,000` items, the gap became much larger. Hash-table search was `139.35x` faster for hits, `198.79x` faster for misses, and `174.54x` faster for mixed queries.

Example: In customer-support software, a hash table is the better choice when an agent needs to find a ticket by ticket ID many times during the day. This is useful because the search can go directly to the relevant bucket instead of scanning the full ticket list one record at a time.

---

## When Linear Search Is Still Acceptable

Linear search is still acceptable when:

1. If the dataset is very small. At `100` items, both approaches were still fast in absolute time even though the hash table was already ahead.

2. If only one or two searches will ever be performed. In that case, building and maintaining a separate hash-based structure may not be necessary.

3. If the data is already stored as a plain list and simplicity matters more than speed. Linear search is still useful for this purpose because it is easy to understand and easy to implement.

4. If the search condition is not based on one direct key and instead requires checking each item one by one anyway.

It is important to note that acceptable does not mean best. CTA-5 benchmark results show that linear search becomes much weaker as the dataset grows. At `10,000` items, linear search required `36.4574 ms` for hits, `70.2530 ms` for misses, and `54.5457 ms` for mixed queries, which is much slower than the hash table in every mode.

Example: In customer-support software, linear search may still be acceptable for a very small temporary list of recently opened tickets. This is useful when the list only contains a few entries and a simple one-time scan is enough.

---

## Search Comparison Snapshot

The following table summarizes the search comparison shown in the CTA-5 Benchmark Lab.

{{SPEEDUP_SUMMARY_TABLE}}

It is important to note that the speedup results become much larger as the dataset grows. The misses case shows the widest gap because linear search must scan the entire dataset before reporting failure, while the hash table usually only checks the target bucket and its chain.

---

## Search Comparison Figures

The following figures summarize the hash-table-versus-linear-search comparison from the Benchmark Lab.

**Figure 1**  
*Hash table vs. linear search runtime*

![Hash Table vs. Linear Search](charts/hash_vs_linear_search.png)

*Note*: The chart shows that hash-table search stays almost flat while linear search grows sharply as the dataset becomes larger.

**Figure 2**  
*Search speedup summary*

![Search Speedup](charts/search_speedup.png)

*Note*: The speedup chart shows that the practical advantage of hash-table lookup widens steadily as the dataset grows.

---

## Practical Summary

| Criterion | Perfect Hashing | Non-Perfect Hashing | Hash Table | Linear Search |
|-----------|-----------------|---------------------|------------|---------------|
| Best use case | Fixed key set | Dynamic key set | Repeated key lookup | Small or one-time scans |
| Best-case runtime pattern | No collisions for the chosen keys | Strong average-case lookup | Fast average key search | Simple direct scan |
| Average weakness | Must know keys in advance | Needs collision handling | Can degrade under heavy collisions | Grows directly with dataset size |
| Flexibility | Low | High | High | High |
| CTA-5 role | Conceptual comparison | Actual hashing model | Main lookup structure | Baseline comparison tool |
| Strong benchmark result | Collision-free idea | Supports flexible storage | Faster than linear search at every tested size | Only acceptable at very small scale |

---

## Key Takeaway

In practice, there is no single best hashing approach for every situation. If the key set is fixed and known in advance, perfect hashing is the best choice because it can avoid collisions entirely. If the key set changes over time, non-perfect hashing is the best choice because it remains flexible and practical. Within this project, the most practical recommendation is to use the hash table instead of linear search when repeated key lookup matters, especially as the dataset becomes larger.

Based on Benchmark Lab results and the Hash Table Lab feature, the most practical recommendation is to use perfect hashing only for fixed known key sets, use non-perfect hashing with collision handling for dynamic key-value storage, use the CTA-5 hash table when repeated key lookup matters, and finally, use linear search only when the dataset is very small or the search is simple and one-time.
