"""
Pytest tests for the src/ptth/api.py file
"""
import pytest

from src.ptth.api import (
    get_forte_name,
    get_intervals,
    get_most_packed_to_the_left,
    get_set_class_members,
    invert,
    is_inversionally_related,
    is_transpositionally_related,
    make_chord_from_intervals,
    mod_12,
    normal_form,
    normalize,
    prime_form,
    rotate_pitches,
    transpose,
    _tuple_to_string
)
from test.data_api import (
    test_get_forte_name,
    test_get_intervals,
    test_get_most_packed_to_the_left,
    test_get_set_class_members,
    test_init_happy_path,
    test_init_str_input_with_wrong_chars,
    test_invert,
    test_is_inversionally_related,
    test_is_transpositionally_related,
    test_make_chord_from_intervals,
    test_mod_12,
    test_normal_form,
    test_prime_form,
    test_rotate_pitches,
    test_transpose,
    test_tuple_to_string
)

class TestTheApi(object):

    @pytest.mark.parametrize("pitches, expected_pcs, expected_pcs2", test_init_happy_path)
    def test_init_happy_path(self, pitches, expected_pcs, expected_pcs2):
        pcs = normalize(pitches)
        assert pcs == expected_pcs
        tup = normalize(pitches, de_dup=False, sort=False)
        assert tup == expected_pcs2


    def test_init_non_str_input_raises_correct_error(self):
        test_input = 456738
        with pytest.raises(TypeError) as err:
            pcs = normalize(test_input)
        assert 'must enter a string, such as "05T38"' == str(err.value)


    @pytest.mark.parametrize("pitches", test_init_str_input_with_wrong_chars)
    def test_init_str_input_with_wrong_chars_raises_correct_error(self, pitches):
        with pytest.raises(ValueError) as err:
            pcs = normalize(pitches)
        assert 'pitch class string must contain only the numbers 0-9 and/or the '\
            'letters "T" or "t" and "E" or "e"' == str(err.value)


    @pytest.mark.parametrize("input, expected", test_tuple_to_string)
    def test_tuple_to_string(self, input, expected):
        assert _tuple_to_string(input) == expected


    @pytest.mark.parametrize("input, expected", test_mod_12)
    def test_mod_12(self, input, expected):
        assert mod_12(input) == expected


    @pytest.mark.parametrize("chord1, chord2, expected", test_get_most_packed_to_the_left)
    def test_get_most_packed_to_the_left_happy_path(self, chord1, chord2, expected):
        result = get_most_packed_to_the_left(chord1, chord2)
        assert result == expected


    def test_get_most_packed_to_the_left_uneven_chords(self):
        chord1 = (1, 2, 3, 4)
        chord2 = (5, 6)
        with pytest.raises(ValueError) as err:
            result = get_most_packed_to_the_left(chord1, chord2)
        assert 'the chords must have the same number of notes' == str(err.value)


    @pytest.mark.parametrize("chord, n, expected", test_rotate_pitches)
    def test_rotate_pitches(self, chord, n, expected):
        result = rotate_pitches(chord, n)
        assert result == expected


    def test_rotate_pitches_empty_chord(self):
        chord = tuple()
        with pytest.raises(ValueError) as err:
            result = rotate_pitches(chord)
        assert 'must provide a chord' == str(err.value)


    @pytest.mark.parametrize("pitches, expected", test_normal_form)
    def test_normal_form(self, pitches, expected):
        assert normal_form(pitches) == expected


    @pytest.mark.parametrize("chord, expected", test_get_intervals)
    def test_get_intervals(self, chord, expected):
        result = get_intervals(chord)
        assert result == expected
        assert len(result[0]) == len(result[1])
        assert len(result[0]) == len(chord) - 1


    @pytest.mark.parametrize("intervals, starting_pitch, expected",
                             test_make_chord_from_intervals)
    def test_make_chord_from_intervals(self,
                                       intervals,
                                       starting_pitch,
                                       expected):
        result = make_chord_from_intervals(intervals,
                                           starting_pitch=starting_pitch)
        assert result == expected

    
    @pytest.mark.parametrize("pitches, interval, expected", test_transpose)
    def test_transpose(self, pitches, interval, expected):
        assert transpose(pitches, interval) == expected


    @pytest.mark.parametrize("pitches, transpose, expected", test_invert)
    def test_invert(self, pitches, transpose, expected):
        assert invert(pitches, transpose) == expected


    @pytest.mark.parametrize("set1, set2, expected",
                             test_is_transpositionally_related)
    def test_is_transpositionally_related(self,
                                          set1,
                                          set2,
                                          expected):
        assert is_transpositionally_related(set1, set2) == expected


    @pytest.mark.parametrize("set1, set2, expected",
                             test_is_inversionally_related)
    def test_is_inversionally_related(self,
                                      set1,
                                      set2,
                                      expected):
        assert is_inversionally_related(set1, set2) == expected


    @pytest.mark.parametrize("pitches, expected",
                             test_get_set_class_members)
    def test_get_set_class_members(self, pitches, expected):
        assert get_set_class_members(pitches).sort() == expected.sort()


    @pytest.mark.parametrize("pitches, expected",
                             test_prime_form)
    def test_prime_form(self, pitches, expected):
        assert prime_form(pitches) == expected


    @pytest.mark.parametrize("pitches, expected",
                             test_get_forte_name)
    def test_get_forte_name(self, pitches, expected):
        assert get_forte_name(pitches) == expected
