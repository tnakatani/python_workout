import time

import pytest

from src.iterators_generators.iterators_generators import (
    Circle,
    CircleInherit,
    MyEnumerate,
    MyRange,
    MyZip,
    all_lines,
    all_lines_mychain, circle,
    elapsed_since,
    file_usage_timing,
    my_generator,
    mychain,
    myrange_generator, parallel_lines,
    yield_filter,
)

####################################################################################################
# e47: MyEnumerate


class TestMyEnumerate:
    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                ["Chocolate", "Vanilla", "Strawberry"],
                [(0, "Chocolate"), (1, "Vanilla"), (2, "Strawberry")],
            ),
            (
                [1, 2, 3],
                [(0, 1), (1, 2), (2, 3)],
            ),
        ],
    )
    def test_myenumerate(self, inputs, expected):
        e = MyEnumerate(inputs)
        e_indexed = [(i, v) for i, v in e]
        assert e_indexed == expected

    def test_myenumerate_enumerating_twice(self):
        e = MyEnumerate("abc")
        e_indexed = [(i, v) for i, v in e]
        f_indexed = [(i, v) for i, v in e]
        assert e_indexed == [(0, "a"), (1, "b"), (2, "c")]
        assert f_indexed == [(0, "a"), (1, "b"), (2, "c")]

    def test_myenumerate_is_iterable(self):
        e = MyEnumerate("abc")
        assert hasattr(e, "__iter__")

    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                ["Chocolate", "Vanilla", "Strawberry"],
                [(0, "Chocolate"), (1, "Vanilla"), (2, "Strawberry")],
            ),
            (
                [1, 2, 3],
                [(0, 1), (1, 2), (2, 3)],
            ),
        ],
    )
    def test_mygenerator(self, inputs, expected):
        g = my_generator(inputs)
        assert [(i, v) for i, v in g] == expected


####################################################################################################
# e48: Circle


class TestCircle:
    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                ["a", "b", "c"],
                ["a", "b", "c", "a", "b", "c"],
            ),
            (
                [1, 2],
                [1, 2, 1, 2, 1, 2],
            ),
        ],
    )
    def test_circle(self, inputs, expected):
        c = Circle(inputs, 6)
        assert [i for i in c] == expected

    def test_circle_inherit(self):
        c = CircleInherit("abc", 6)
        assert [i for i in c] == ["a", "b", "c", "a", "b", "c"]

    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                ["a", "b", "c"],
                ["a", "b", "c", "a", "b", "c"],
            ),
            (
                [1, 2],
                [1, 2, 1, 2, 1, 2],
            ),
        ],
    )
    def test_circle_generator(self, inputs, expected):
        c = circle(inputs, 6)
        assert [i for i in c] == expected

    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                [0, 10, 2],
                [0, 2, 4, 6, 8],
            ),
            (
                [0, 20, 10],
                [0, 10],
            ),
        ],
    )
    def test_myrange(self, inputs, expected):
        r = MyRange(inputs[0], inputs[1], inputs[2])
        assert [i for i in r] == expected

    def test_myrange_with_defaults(self):
        r = MyRange(0, 5)
        s = MyRange(10)
        t = MyRange(0)
        assert [i for i in r] == [0, 1, 2, 3, 4]
        assert [i for i in s] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert [i for i in t] == []


####################################################################################################
# e48: All of the files


@pytest.fixture
def test_dir(tmp_path):
    f = tmp_path / "f1.txt"
    g = tmp_path / "f2.txt"
    h = tmp_path / "f3.txt"
    i = tmp_path / "f4.txt"
    f.write_text("\n".join(["foo", "bar", "baz"]))
    g.write_text("\n".join(["one", "two", "three"]))
    h.write_text(
        """This is the first line of a big file
and this is the second line
and this is, to no one's surprise, the third line
but the biggest word will probably be encyclopedia"""
    )
    i.write_text("")
    return tmp_path


@pytest.fixture
def test_empty_dir(tmp_path):
    return tmp_path


class TestAlloftheFiles:
    def test_all_lines(self, test_dir):
        assert len([i for i in all_lines(test_dir)]) == 10

    def test_all_lines_empty_dir(self, test_empty_dir):
        assert len([i for i in all_lines(test_empty_dir)]) == 0

    def test_parallel_lines(self, test_dir):
        result = [i for i in parallel_lines(test_dir) if i]
        assert len(result) == 10

    def test_parallel_lines_with_filter(self, test_dir):
        result = [i for i in parallel_lines(test_dir, "foo") if i]
        assert len(result) == 1


####################################################################################################
# e49: Elapsed Since
# TODO: Learn how to mock time.perf_counter
class TestElapsedSince:
    def test_elapsed_since(self):
        for index, t in enumerate(elapsed_since("abc")):
            assert isinstance(t, tuple)
            assert isinstance(t[0], float)
            assert isinstance(t[1], str)

            if index == 0:
                assert t[0] == 0
            else:
                assert round(t[0], 1) == 0.1

            time.sleep(0.1)

    def test_elapsed_with_min_elapsed(self):
        time_elapsed = 0.5
        for index, t in enumerate(elapsed_since("abc", min_wait=time_elapsed)):
            assert isinstance(t, tuple)
            assert isinstance(t[0], float)
            assert isinstance(t[1], str)

            if index == 0:
                assert t[0] == time_elapsed
            else:
                assert round(t[0], 1) == time_elapsed

    # BTE 2
    # TODO: Mock os.stat attributes
    # Uses test_dir fixture
    def test_file_usage_timing(self, test_dir):
        for i in file_usage_timing(test_dir):
            assert len(i) == 4

    # BTE 3
    def test_yield_filter(self):
        data = ["foo", "", "bar", "", "baz"]
        assert len([i for i in yield_filter(data)]) == 3


class TestMyChain:
    data = ("abc", [1, 2, 3], {"foo": 1, "bar": 2})

    def test_mychain(self):
        assert [i for i in mychain(*self.data)] == [
            "a",
            "b",
            "c",
            1,
            2,
            3,
            "foo",
            "bar",
        ]

    def test_myzip(self):
        z = MyZip()
        for i, j, k in zip(
            z.zip(*self.data), zip(*self.data), z.python_zip(*self.data)
        ):
            assert i == j == k


class TestAllLinesMyChain:
    def test_all_lines_mychain(self, test_dir):
        assert len([i for i in all_lines_mychain(test_dir)]) == 10


class TestMyRangeGenerator:
    @pytest.mark.parametrize(
        "inputs, expected",
        [
            (
                    [0, 10, 2],
                    [0, 2, 4, 6, 8],
            ),
            (
                    [0, 20, 10],
                    [0, 10],
            ),
        ],
    )
    def test_myrange_generator(self, inputs, expected):
        r = myrange_generator(inputs[0], inputs[1], inputs[2])
        assert [i for i in r] == expected

    def test_myrange_generator_with_defaults(self):
        r = myrange_generator(0, 5)
        s = myrange_generator(10)
        t = myrange_generator(0)
        assert [i for i in r] == [0, 1, 2, 3, 4]
        assert [i for i in s] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        assert [i for i in t] == []
