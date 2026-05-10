# File: course_set.py 
#
# Author: Alexander Ricciardi
# Date: 2026-05-10
# Course: CSC506
# Professor: Dr. Jonathan Vanover
# Term: Spring A 2026
# -------------------------------------------------------------------------
#
# --- Module Functionality ---
# - Provide a small hash-backed Set ADT for classroom demonstrations.
# - Support dynamic mutation operations and static two-set operations.
# - Preserve insertion order for stable, readable Streamlit output.
# -------------------------------------------------------------------------
#
# --- Module Contents Overview ---
# TYPE VARIABLES:
#   - Type: T - hashable value type stored by CourseSet
#
# REGULAR CLASSES:
#   - Class: CourseSet - set abstraction backed by dictionary keys
# -------------------------------------------------------------------------
#
# --- Dependencies / Imports ---
# - Standard Library: collections.abc, typing
# --- Requirements ---
# - Python 3.12+
# -------------------------------------------------------------------------
#
# --- Usage / Integration ---
# Imported by the Bubble Quickselect Sets Streamlit page and CourseSet tests.
# -------------------------------------------------------------------------
#
# --- Apache-2.0 ---
# Copyright 2026 Alexander Samuel Ricciardi - All rights reserved.
# License: Apache-2.0 | Code
# -------------------------------------------------------------------------

"""Course-focused Set ADT for the Bubble Quickselect Sets module.

The ``CourseSet`` class stores unique hashable values and provides both
dynamic mutation operations and static set operations that return new sets.
"""

# __________________________________________________________________________
#
# ========================================================================
# IMPORTS
# ========================================================================

from __future__ import annotations

from collections.abc import Hashable, Iterable, Iterator
from typing import Generic, TypeVar


# __________________________________________________________________________
# Global Constants / Variables
# ========================================================================
# TYPE VARIABLES
# ========================================================================

T = TypeVar("T", bound=Hashable)
"""Hashable value type stored by ``CourseSet``."""


# __________________________________________________________________________
# Class Definitions - Regular Classes
# ========================================================================
# COURSE SET
# ========================================================================
# Contains the regular Set ADT implementation used by the Module 8 Set lab.
#
# CLASS CONTENTS:
#   - Class: CourseSet - hash-backed set with dynamic and static operations
# -------------------------------------------------------------------------
# Constraint: Backing keys must be hashable so membership can use dictionary lookup.
# Rationale: This mirrors set behavior while keeping insertion order visible.

# ------------------------------------------------------------------------- class CourseSet
class CourseSet(Generic[T]):
    """Store unique hashable values with classroom set operations.

    Args:
        values: Optional iterable of initial values. Duplicate values are
            ignored while first-seen order is preserved for display.

    Logic:
        This class remains a regular class because initialization normalizes an
        iterable into hash-backed internal state.
        1. Store unique values as dictionary keys for membership behavior.
        2. Preserve insertion order so demos render predictably.
        3. Expose dynamic mutation, static set operations, and display helpers.
    """

    # --------------------------------------------------------------- __init__()
    def __init__(self, values: Iterable[T] | None = None) -> None:
        """Initialize a set from optional values.

        Args:
            values: Optional iterable of hashable values.

        Returns:
            None.

        Logic:
            This initializer prepares the CourseSet for hash-backed operations.
            1. Create the internal dictionary used for uniqueness and membership.
            2. Insert optional values in first-seen order.
            3. Let duplicate values collapse naturally into one dictionary key.
        """
        self._items: dict[T, None] = {}
        # VALIDATION: optional construction accepts any iterable of hashable values.
        if values is not None:
            # MAIN ITERATION LOOP: duplicate values overwrite the same dictionary key.
            for value in values:
                self._items[value] = None
    # --------------------------------------------------------------- end __init__()

    # ________________________________________________
    # Setters
    #
    # --------------------------------------------------------------- add()
    def add(self, value: T) -> bool:
        """Add a value to this set.

        Args:
            value: Hashable value to add.

        Returns:
            ``True`` when the value was new; otherwise ``False``.

        Logic:
            This setter mutates the set only when the value is new.
            1. Check whether the hashable value already exists.
            2. Return ``False`` without mutation for duplicates.
            3. Store new values and return ``True``.
        """
        # VALIDATION: existing values are left unchanged to preserve set semantics.
        if value in self._items:
            return False
        self._items[value] = None
        return True
    # --------------------------------------------------------------- end add()

    # --------------------------------------------------------------- remove()
    def remove(self, value: T) -> bool:
        """Remove a value from this set when present.

        Args:
            value: Hashable value to remove.

        Returns:
            ``True`` when the value was removed; otherwise ``False``.

        Logic:
            This setter mutates the set only when the value exists.
            1. Check whether the hashable value is currently stored.
            2. Return ``False`` without mutation for absent values.
            3. Delete present values and return ``True``.
        """
        # VALIDATION: absent values cannot be removed and do not mutate the set.
        if value not in self._items:
            return False
        del self._items[value]
        return True
    # --------------------------------------------------------------- end remove()

    # ________________________________________________
    # Getters
    #
    # --------------------------------------------------------------- contains()
    def contains(self, value: T) -> bool:
        """Return whether the set contains a value.

        Args:
            value: Hashable value to check.

        Returns:
            ``True`` when the value is present.

        Logic:
            This getter performs a hash-backed membership lookup.
            1. Query the internal dictionary keys.
            2. Return whether the value is present.
        """
        return value in self._items
    # --------------------------------------------------------------- end contains()

    # ________________________________________________
    # Set Operations
    #
    # --------------------------------------------------------------- union()
    def union(self, other: CourseSet[T]) -> CourseSet[T]:
        """Return values that appear in either set.

        Args:
            other: Second set operand.

        Returns:
            New set containing values from this set followed by new values from
            ``other``.

        Logic:
            This static set operation returns a new union result.
            1. Seed the result with this set's values.
            2. Add values from ``other`` while preserving uniqueness.
            3. Return the derived set without mutating either operand.
        """
        result = CourseSet(self)
        # MAIN ITERATION LOOP: append only values that are new to the result set.
        for value in other:
            result.add(value)
        return result
    # --------------------------------------------------------------- end union()

    # --------------------------------------------------------------- intersection()
    def intersection(self, other: CourseSet[T]) -> CourseSet[T]:
        """Return values that appear in both sets.

        Args:
            other: Second set operand.

        Returns:
            New set containing shared values in this set's display order.

        Logic:
            This static set operation returns values shared by both operands.
            1. Iterate over this set in display order.
            2. Keep only values that also appear in ``other``.
            3. Return the derived set without mutating either operand.
        """
        return CourseSet(value for value in self if value in other)
    # --------------------------------------------------------------- end intersection()

    # --------------------------------------------------------------- difference()
    def difference(self, other: CourseSet[T]) -> CourseSet[T]:
        """Return values from this set that are absent from another set.

        Args:
            other: Second set operand.

        Returns:
            New set containing values unique to this set.

        Logic:
            This static set operation returns target-only values.
            1. Iterate over this set in display order.
            2. Keep only values that do not appear in ``other``.
            3. Return the derived set without mutating either operand.
        """
        return CourseSet(value for value in self if value not in other)
    # --------------------------------------------------------------- end difference()

    # --------------------------------------------------------------- symmetric_difference()
    def symmetric_difference(self, other: CourseSet[T]) -> CourseSet[T]:
        """Return values that appear in exactly one operand.

        Args:
            other: Second set operand.

        Returns:
            New set containing values unique to either set.

        Logic:
            This static set operation returns values that appear in exactly one set.
            1. Seed the result with values unique to this set.
            2. Add values unique to ``other``.
            3. Return the derived set without mutating either operand.
        """
        result = CourseSet(value for value in self if value not in other)
        # MAIN ITERATION LOOP: add values that are unique to the second operand.
        for value in other:
            # VALIDATION: shared values are excluded from symmetric difference.
            if value not in self:
                result.add(value)
        return result
    # --------------------------------------------------------------- end symmetric_difference()

    # ________________________________________________
    # Utilities
    #
    # --------------------------------------------------------------- to_list()
    def to_list(self) -> list[T]:
        """Return set values as a display list.

        Returns:
            Values in first-seen insertion order.

        Logic:
            This utility exposes stored values for UI tables and tests.
            1. Read the ordered dictionary keys.
            2. Return them as a list.
        """
        return list(self._items)
    # --------------------------------------------------------------- end to_list()

    # --------------------------------------------------------------- __contains__()
    def __contains__(self, value: object) -> bool:
        """Return whether a value is present.

        Args:
            value: Value to check.

        Returns:
            ``True`` when the value is present.

        Logic:
            This special method supports ``value in course_set`` syntax.
            1. Query the internal dictionary keys.
            2. Return whether the value is present.
        """
        return value in self._items
    # --------------------------------------------------------------- end __contains__()

    # --------------------------------------------------------------- __iter__()
    def __iter__(self) -> Iterator[T]:
        """Iterate over values in insertion order.

        Returns:
            Iterator over stored values.

        Logic:
            This special method supports iteration over stored values.
            1. Read the internal dictionary key iterator.
            2. Return that iterator to the caller.
        """
        return iter(self._items)
    # --------------------------------------------------------------- end __iter__()

    # --------------------------------------------------------------- __len__()
    def __len__(self) -> int:
        """Return the number of unique values.

        Returns:
            Unique value count.

        Logic:
            This special method supports ``len(course_set)``.
            1. Read the internal dictionary size.
            2. Return the unique value count.
        """
        return len(self._items)
    # --------------------------------------------------------------- end __len__()

    # --------------------------------------------------------------- __repr__()
    def __repr__(self) -> str:
        """Return a developer-facing representation.

        Returns:
            ``CourseSet([...])`` representation.

        Logic:
            This special method provides a concise debugging representation.
            1. Convert stored values into display-list form.
            2. Return a ``CourseSet([...])`` string.
        """
        return f"CourseSet({self.to_list()!r})"
    # --------------------------------------------------------------- end __repr__()

# ------------------------------------------------------------------------- end class CourseSet

# __________________________________________________________________________
#
# ========================================================================
# End of File
# ========================================================================
