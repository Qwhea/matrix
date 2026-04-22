import asyncio
import re

import aiohttp

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'

async def get_matrix(url: str) -> list[int] | None:
    """Получает матрицу из url и возвращает ее элементы по спирали против часовой стрелки."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            if response.status == 200:
                text = await response.text()
                matrix = []
                for line in text.strip().splitlines():
                    numbers = list(map(int, re.findall(r'-?\d+', line)))
                    if numbers:
                        matrix.append(numbers)

                if not matrix:
                    raise ValueError("Неверный формат входных данных")

                result = []

                if matrix:
                    top, bottom = 0, len(matrix) - 1
                    left, right = 0, len(matrix[0]) - 1

                    while top <= bottom and left <= right:
                        for row in range(top, bottom + 1):
                            result.append(matrix[row][left])
                        left += 1

                        if left <= right:
                            for col in range(left, right + 1):
                                result.append(matrix[bottom][col])
                            bottom -= 1

                        if top <= bottom:
                            for row in range(bottom, top - 1, -1):
                                result.append(matrix[row][right])
                            right -= 1

                        if left <= right:
                            for col in range(right, left - 1, -1):
                                result.append(matrix[top][col])
                            top += 1

                    return result
            return None


if __name__ == '__main__':
    print(asyncio.run(get_matrix(SOURCE_URL)))
