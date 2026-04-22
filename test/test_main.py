import asyncio
from logging import exception

import pytest
import aioresponses

from src.main import get_matrix

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]

TRAVERSAL_6x4 = [
    10, 70, 130, 190,
    200, 210, 220, 230, 240,
    180, 120, 60,
    50, 40, 30, 20,
    80, 140,
    150, 160, 170,
    110, 100, 90
]

class TestMatrix:

    def test_get_matrix(self):
        assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL

    def test_get_matrix_bigger_size(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, body="""
                                            +-----+-----+-----+-----+-----+-----+
                                            |  10 |  20 |  30 |  40 |  50 |  60 |
                                            +-----+-----+-----+-----+-----+-----+
                                            |  70 |  80 |  90 | 100 | 110 | 120 |
                                            +-----+-----+-----+-----+-----+-----+
                                            | 130 | 140 | 150 | 160 | 170 | 180 |
                                            +-----+-----+-----+-----+-----+-----+
                                            | 190 | 200 | 210 | 220 | 230 | 240 |
                                            +-----+-----+-----+-----+-----+-----+""",
                                        status=200)

            assert asyncio.run(get_matrix(SOURCE_URL)) == TRAVERSAL_6x4

    def test_matrix_raises_exception_on_invalid_url(self):
        with pytest.raises(Exception):
            asyncio.run(get_matrix("https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt111"))


    def test_matrix_empty_file(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, body="", status=200)
            with pytest.raises(ValueError):
                asyncio.run(get_matrix(SOURCE_URL))


    def test_wrong_file(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, body="qwe\nrwe\nqwe")
            with pytest.raises(ValueError):
                asyncio.run(get_matrix(SOURCE_URL))

    def test_not_square_and_wrong_matrix(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, body="1 2 3 4 \n"
                                          "5 6 7 8 \n"
                                          "9 a s d"
                         )
            with pytest.raises(IndexError):
                asyncio.run(get_matrix(SOURCE_URL))

    def test_not_full_matrix(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, body="1 2 3 4 \n"
                                          "5 6 7 8 \n"
                                          "9"
                         )
            with pytest.raises(IndexError):
                asyncio.run(get_matrix(SOURCE_URL))

    def test_network_timeout(self):
        with aioresponses.aioresponses() as response:
            response.get(SOURCE_URL, exception=asyncio.TimeoutError)
            with pytest.raises(TimeoutError):
                asyncio.run(get_matrix(SOURCE_URL))
