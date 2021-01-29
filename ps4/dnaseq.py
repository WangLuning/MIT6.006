#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.my_dict = {}

    # Associates the value v with the key k.
    def put(self, k, v):
        if k not in self.my_dict.keys():
            self.my_dict[k] = set()
        self.my_dict[k].add(v)

    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, k):
        if k in self.my_dict.keys():
            ordered_list = list(self.my_dict[k])
            if isinstance(ordered_list[0], str):
                ordered_list.sort()
            return ordered_list
        return list()

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
def subsequenceHashes(seq, k):
    cur = ""
    idx = 0

    for i in range(k):
        cur += next(seq)

    hash_value = RollingHash(cur)
    prev = cur[0]
    yield cur, 0, hash_value

    while True:
        try:
            idx += 1
            next_char = next(seq)
            cur = cur[1:] + next_char
            val = hash_value.slide(prev, next_char)
            prev = cur[0]
            yield cur, idx, val
        except StopIteration:
            break

# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    cur = ""
    idx = 0

    for i in range(k):
        cur += next(seq)

    hash_value = RollingHash(cur)
    prev = cur[0]

    for i in range(m - 1):
        next(seq)
    yield cur, 0, hash_value

    while True:
        try:
            for i in range(m - 1):
                next(seq)
            idx += 1
            next_char = next(seq)
            cur = cur[1:] + next_char
            val = hash_value.slide(prev, next_char)
            prev = cur[0]

            for i in range(m - 1):
                next(seq)

            yield cur, idx, val
        except StopIteration:
            break

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    matching_points = list()
    record_it = b
    dict_a = Multidict()
    for it in intervalSubsequenceHashes(a, k, m):
        dict_a.put(it[2], (it[0], it[1]))
    print("putting seq a into dict")

    for b_sub in subsequenceHashes(record_it, k):
        if dict_a.get(b_sub[2]) != list():
            for each_dict_item in dict_a.get(b_sub[2]):
                matching_points.append((each_dict_item[1], b_sub[1]))
    print("reading two sequence finished")
    return matching_points

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0]))
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
