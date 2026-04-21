# -------------------------------------------------------------------------
# File: hash_table.py
# Author: Alexander Ricciardi
# Date: 2026-04-14
# -------------------------------------------------------------------------
# Course: CSC506 – Design and Analysis of Algorithms
# Professor: Dr. Jonathan Vanover
# Spring A (26SA) – 2026
# -------------------------------------------------------------------------

# --- Module Functionality ---
# HashTable class using a simple position-weighted hash function and
# separate chaining for collision resolution.  Supports insert, search,
# delete, update-on-duplicate, automatic resizing, and statistics.
# -------------------------------------------------------------------------

# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Hash table implementation with separate chaining.

The hash function uses a position-weighted approach (multiply by 31,
add ``ord(ch)``) and compresses via modulo to the current capacity.
Collisions are resolved by chaining entries in per-bucket lists.
"""

# ______________________________________________________________________________
#
# ==============================================================================
# IMPORTS
# ==============================================================================

from __future__ import annotations

from models.hash_entry import HashEntry
from models.hash_table_stats import HashTableStats

# ______________________________________________________________________________
# Global Constants / Variables
# ==============================================================================
# HASH FUNCTION DESIGN
# ==============================================================================
#
# The hash function uses a position-weighted polynomial:
#     h(s) = ord(s[0])·31^(n-1) + ord(s[1])·31^(n-2) + ... + ord(s[n-1])
#
# A multiplier of 31 is the textbook choice (also used by Java String.hashCode):
#   - prime → reduces clustering after modulo compression
#   - odd   → preserves the low bit during multiplication
#   - 31 = 2^5 - 1 → multiplication can be optimized to a shift-subtract
#
# COMPRESSION:
#   The raw hash code is reduced into the bucket range with `h % capacity`.
#   capacity is kept prime (see _next_prime) to spread keys more uniformly.
#
# COLLISION POLICY:
#   Separate chaining — each bucket is a Python list of HashEntry instances.
#   Chains stay short while load factor < max_load_factor (default 0.75),
#   at which point _resize_and_rehash() doubles capacity to the next prime.
# ------------------------------------------------------------------------------

# Constraint: shared multiplier used by every position-weighted hash computation.
# Rationale: changing this value would change every stored bucket index and
# invalidate any persisted hash-table state.
_HASH_MULTIPLIER: int = 31
"""Multiplier constant for the position-weighted string hash."""

# ______________________________________________________________________________
# Function definitions
# ==============================================================================
# PRIME HELPERS
# ==============================================================================
# Capacity is kept prime so the modulo compression spreads keys evenly even
# when the keyspace has structural patterns (e.g., sequential ids, repeated
# prefixes). Both helpers are pure, deterministic, and side-effect free.
#
# - Function: _is_prime()    - Trial-division primality test
# - Function: _next_prime()  - Smallest prime >= n (used during resize)
# ------------------------------------------------------------------------------

# -------------------------------------------------------------------------------- _is_prime()
def _is_prime(n: int) -> bool:
    """Return True if *n* is a prime number.

    Logic:
        This helper is a small trial-division primality test for capacity sizing.
        1. Reject inputs below 2 (not prime by definition).
        2. Accept 2 and 3 directly; reject any multiple of 2 or 3.
        3. Test remaining candidates with the 6k±1 wheel up to sqrt(n).
        4. Return True only if no divisor is found.
    """
    # VALIDATION: anything below 2 is not prime
    if n < 2:
        return False
    # Step 1: small-number fast path (2 and 3 are prime)
    if n < 4:
        return True
    # Step 2: eliminate any multiple of 2 or 3 in O(1)
    if n % 2 == 0 or n % 3 == 0:
        return False
    # Step 3: test 6k±1 candidates up to sqrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
# --------------------------------------------------------------------------------


# -------------------------------------------------------------------------------- _next_prime()
def _next_prime(n: int) -> int:
    """Return the smallest prime >= *n*.

    Logic:
        This helper is used to round capacity choices up to a prime.
        1. Start the search from n itself, bumping to n+1 when n is even.
        2. Walk forward by 2 (only odd candidates) until _is_prime succeeds.
        3. Return the first prime found.
    """
    # Step 1: skip even seeds so the +=2 walk only visits odd candidates
    candidate = n if n % 2 != 0 else n + 1
    # MAIN ITERATION LOOP: walk odd candidates until one is prime
    while not _is_prime(candidate):
        candidate += 2
    return candidate
# --------------------------------------------------------------------------------

# ______________________________________________________________________________
# Class Definitions - Regular Classes
# ==============================================================================
# CLASS DEFINITIONS
# ==============================================================================
# Regular (non-dataclass) implementation of an open-keyed hash table that
# manages a bucket array and a collision counter. Chosen as a regular class
# because __init__ runs non-trivial setup (prime sizing, bucket allocation)
# and the type owns mutable internal state across many operations.
#
# - Class: HashTable - Position-weighted hash with separate chaining
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------- class HashTable
class HashTable:
    """Hash table with separate chaining collision resolution.

    Logic:
        This class is a regular class (not a dataclass) because __init__ allocates
        bucket lists, normalizes capacity to a prime, and tracks cumulative state
        across many later operations.
        1. Allocate `_buckets` as a list of empty chains sized to a prime capacity.
        2. Track size and cumulative collision count to expose health via get_stats().
        3. Trigger _resize_and_rehash() automatically when load factor exceeds threshold.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(
        self,
        initial_capacity: int = 53,
        max_load_factor: float = 0.75,
    ) -> None:
        """Initialize the hash table with a prime-sized bucket array.

        Logic:
            This initializer prepares the bucket structure and collision counters.
            1. Round the requested initial capacity up to the nearest prime (>= 1).
            2. Allocate one empty list per bucket to back separate chaining.
            3. Initialize size and cumulative collision counters to zero.
        """
        self._capacity: int = _next_prime(max(initial_capacity, 1))
        self._max_load_factor: float = max_load_factor
        self._buckets: list[list[HashEntry]] = [[] for _ in range(self._capacity)]
        self._size: int = 0
        self._total_collisions: int = 0
    # ---------------------------------------------------------------

    # ________________________________________________
    #  Utilities
    #
    # --------------------------------------------------------------- _hash_code()
    def _hash_code(self, key: str) -> int:
        """Compute a position-weighted hash code for *key*.

        Logic:
            This helper computes the polynomial hash described in the file header.
            1. Start with an accumulator of 0.
            2. For each character, multiply running value by 31 and add ord(ch).
            3. Return the final non-negative integer hash code.
        """
        h: int = 0
        # MAIN ITERATION LOOP: accumulate position-weighted contribution per character
        for ch in key:
            h = h * _HASH_MULTIPLIER + ord(ch)
        return h
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _compress()
    def _compress(self, hash_code: int) -> int:
        """Compress *hash_code* into the current bucket range.

        Logic:
            This helper maps a raw hash code to a valid bucket index.
            1. Apply modulo against current capacity (kept prime for spread).
            2. Return the resulting index in [0, capacity).
        """
        return hash_code % self._capacity
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _bucket_index()
    def _bucket_index(self, key: str) -> int:
        """Return the bucket index for *key*.

        Logic:
            This helper composes hashing and compression for callers.
            1. Compute the raw hash code via _hash_code().
            2. Compress the code via _compress() to produce a bucket index.
            3. Return the final index used by insert/search/delete paths.
        """
        return self._compress(self._hash_code(key))
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _should_resize()
    def _should_resize(self) -> bool:
        """Return True if the load factor exceeds the threshold.

        Logic:
            This predicate decides when to trigger an automatic resize.
            1. SAFETY CHECK: if max_load_factor <= 0.0, auto-resize is disabled.
            2. Compare current load factor (size / capacity) against the threshold.
            3. Return True only when the threshold is exceeded.
        """
        # SAFETY CHECK: zero/negative threshold disables automatic resizing
        if self._max_load_factor <= 0.0:
            return False
        return (self._size / self._capacity) > self._max_load_factor
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _resize_and_rehash()
    def _resize_and_rehash(self) -> None:
        """Grow the bucket array and reinsert all existing entries.

        Logic:
            This routine doubles capacity and migrates every entry to a fresh table.
            1. Round 2 * capacity up to the next prime to preserve modulo spread.
            2. Allocate a new bucket array and reset size (collisions stay cumulative).
            3. Re-insert every existing entry via the low-level insert path.
        """
        # Step 1: pick a new prime capacity at least double the current size
        new_capacity = _next_prime(self._capacity * 2)
        old_buckets = self._buckets
        # Step 2: install the empty new bucket array and reset size counter
        self._capacity = new_capacity
        self._buckets = [[] for _ in range(new_capacity)]
        self._size = 0
        # NOTE: do not reset _total_collisions — they are cumulative
        # MAIN ITERATION LOOP: rehash every entry from the old bucket array
        for bucket in old_buckets:
            for entry in bucket:
                self._insert_entry(entry.key, entry.value, track_collision=False)
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- _insert_entry()
    def _insert_entry(
        self,
        key: str,
        value: object,
        *,
        track_collision: bool = True,
    ) -> None:
        """Low-level insert used by both public insert and rehash.

        Logic:
            This helper performs the actual chain-update logic for one (key, value).
            1. Locate the destination bucket via _bucket_index().
            2. UPDATE: if the key already exists, overwrite the value in place and exit.
            3. COLLISION: if the bucket is non-empty (and tracking enabled), increment counter.
            4. APPEND: add a new HashEntry to the chain and bump size.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]

        # UPDATE: if key already exists, overwrite value
        for entry in bucket:
            if entry.key == key:
                entry.value = value
                return

        # COLLISION: bucket already has entries
        if track_collision and len(bucket) > 0:
            self._total_collisions += 1

        # APPEND: new entry to chain
        bucket.append(HashEntry(key, value))
        self._size += 1
    # ---------------------------------------------------------------

    # ________________________________________________
    # Setters
    #
    # --------------------------------------------------------------- insert()
    def insert(self, key: str, value: object) -> None:
        """Insert or update a key-value pair.

        If *key* already exists the value is updated in place.
        Raises ``ValueError`` for empty-string keys.

        Logic:
            This public entry point performs validation, insertion, and resize.
            1. VALIDATION: reject empty-string keys with ValueError.
            2. Delegate to _insert_entry() to perform the chain update.
            3. SAFETY CHECK: trigger _resize_and_rehash() if load factor exceeded.
        """
        # VALIDATION: keys must be non-empty strings
        if not key:
            raise ValueError("Key must be a non-empty string.")
        self._insert_entry(key, value)
        # SAFETY CHECK: keep load factor below threshold for O(1) average behavior
        if self._should_resize():
            self._resize_and_rehash()
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- delete()
    def delete(self, key: str) -> object | None:
        """Remove *key* and return its value, or ``None`` if not found.

        Logic:
            This method removes the entry at the resolved bucket, if present.
            1. Locate the bucket index for the key.
            2. Scan the chain for a matching key.
            3. Pop the entry, decrement size, and return its value on hit.
            4. Return None when no chain element matches.
        """
        idx = self._bucket_index(key)
        bucket = self._buckets[idx]
        # MAIN ITERATION LOOP: scan the chain for the target key
        for i, entry in enumerate(bucket):
            if entry.key == key:
                bucket.pop(i)
                self._size -= 1
                return entry.value
        return None
    # ---------------------------------------------------------------

    # ________________________________________________
    # Getters
    #
    # --------------------------------------------------------------- search()
    def search(self, key: str) -> object | None:
        """Return the value for *key*, or ``None`` if not found.

        Logic:
            This lookup is the hash table's headline O(1) average-case operation.
            1. Compute the destination bucket index.
            2. Scan that bucket's short chain for the matching key.
            3. Return the matching value, or None if the chain holds no match.
        """
        idx = self._bucket_index(key)
        # MAIN ITERATION LOOP: walk the (typically short) chain at this bucket
        for entry in self._buckets[idx]:
            if entry.key == key:
                return entry.value
        return None
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- contains()
    def contains(self, key: str) -> bool:
        """Return True if *key* exists in the hash table.

        Logic:
            This convenience wrapper layers a presence check over search().
            1. Delegate to search() to find the stored value.
            2. Return True when the result is not None.
        """
        return self.search(key) is not None
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- items()
    def items(self) -> list[tuple[str, object]]:
        """Return all stored key-value pairs.

        Logic:
            This method exposes a flat snapshot of (key, value) pairs.
            1. Walk every bucket in the bucket array.
            2. Walk every entry in each bucket's chain.
            3. Append (key, value) tuples to the result list and return it.
        """
        result: list[tuple[str, object]] = []
        # MAIN ITERATION LOOP: visit every bucket and every chain entry
        for bucket in self._buckets:
            for entry in bucket:
                result.append((entry.key, entry.value))
        return result
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- get_stats()
    def get_stats(self) -> HashTableStats:
        """Compute and return a snapshot of current hash table statistics.

        Logic:
            This method aggregates per-bucket counts into a HashTableStats record.
            1. Walk every bucket and tally used / collision / longest counts.
            2. Compute the load factor (size / capacity) with a 4-digit round.
            3. Return a fully populated HashTableStats snapshot for the UI/report.
        """
        used = 0
        collision_buckets = 0
        longest = 0
        # MAIN ITERATION LOOP: aggregate per-bucket counts
        for bucket in self._buckets:
            length = len(bucket)
            # Step 1: bucket is "used" if it has any entries
            if length > 0:
                used += 1
            # Step 2: bucket contributes to collision count when chain length > 1
            if length > 1:
                collision_buckets += 1
            # Step 3: track the longest observed chain length
            if length > longest:
                longest = length
        return HashTableStats(
            size=self._size,
            capacity=self._capacity,
            load_factor=round(self._size / self._capacity, 4) if self._capacity else 0.0,
            used_buckets=used,
            empty_buckets=self._capacity - used,
            collision_buckets=collision_buckets,
            longest_bucket_length=longest,
            total_collisions=self._total_collisions,
        )
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- get_buckets()
    def get_buckets(self) -> list[list[HashEntry]]:
        """Expose the internal bucket structure for UI display.

        Logic:
            This accessor returns the live bucket array for read-only display.
            1. Return the internal list-of-lists reference (no copy).
            2. Callers must treat the result as read-only.
        """
        return self._buckets
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of stored entries.

        Logic:
            This dunder mirrors len() over the size counter.
            1. Return the cached size attribute.
        """
        return self._size
    # ---------------------------------------------------------------

    # --------------------------------------------------------------- __repr__()
    def __repr__(self) -> str:
        """Return a compact summary string.

        Logic:
            This dunder produces a one-line UI/log-friendly summary.
            1. Format size and capacity into a HashTable(...) string.
            2. Return the formatted result.
        """
        return f"HashTable(size={self._size}, capacity={self._capacity})"
    # ---------------------------------------------------------------

# ------------------------------------------------------------------------- end class HashTable

# ==============================================================================
# End of File
# ==============================================================================
