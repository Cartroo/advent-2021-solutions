#!/usr/bin/env python3.10

from sys import stdin

class Mapper:
    """Work out mapping from segment sets to values.

    This class uses a deductive approach in two passes. In the first pass,
    it simply looks for the digits with unique numbers of segments.

    In the second pass, it looks for intersections with the digits it's
    already determined to differentiate between multiple digits with the
    same number of segments. For example, a combination with 5 segments
    could be 2, 3 or 5. However, only 3 has two segments in common with 1,
    and from the remaining two possibilities only 5 has 3 segments in common
    with 4.
    """

    NUM_SEGMENTS = { 2: 1, 3: 7, 4: 4, 7: 8 }

    def __init__(self, segment_sets):
        self.segments_to_value = {}
        self.value_to_segments = {}
        self.analyse_segment_sets(segment_sets)

    def _store_mapping(self, segment_set, value):
        if value is not None:
            self.segments_to_value[segment_set] = value
            self.value_to_segments[value] = segment_set

    def analyse_segment_sets(self, segment_sets):
        self.simple_analysis(segment_sets)
        self.advanced_analysis(segment_sets)

    def simple_analysis(self, segment_sets):
        for segment_set in (frozenset(i) for i in segment_sets):
            self._store_mapping(segment_set, self.NUM_SEGMENTS.get(len(segment_set)))

    def advanced_analysis(self, segment_sets):
        for segment_set in (frozenset(i) for i in segment_sets):
            if len(segment_set) == 6:
                if len(segment_set & self.value_to_segments[1]) < 2:
                    self._store_mapping(segment_set, 6)
                elif len(segment_set & self.value_to_segments[4]) > 3:
                    self._store_mapping(segment_set, 9)
                else:
                    self._store_mapping(segment_set, 0)
            elif len(segment_set) == 5:
                if len(segment_set & self.value_to_segments[1]) > 1:
                    self._store_mapping(segment_set, 3)
                elif len(segment_set & self.value_to_segments[4]) > 2:
                    self._store_mapping(segment_set, 5)
                else:
                    self._store_mapping(segment_set, 2)

    def get_multidigit_value(self, patterns):
        total = 0
        for pattern in (frozenset(i) for i in patterns):
            total = total * 10 + self.segments_to_value[pattern]
        return total


total = 0
for digits, outputs in ((d_s.split(), o_s.split()) for d_s, o_s in (line.split("|", 1) for line in stdin)):
    mapper = Mapper(digits)
    total += mapper.get_multidigit_value(outputs)

print(f"Total={total}")
