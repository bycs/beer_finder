from unittest.mock import MagicMock
from unittest.mock import patch

from bot.utils.statistics import get_number_unique_users_text
from bot.utils.utils import list_separator


def test_list_separator():
    input_list = [1, 2, 3]
    expected_output = [[1, 2, 3]]
    assert list_separator(input_list, max_len=5) == expected_output

    input_list = [1, 2, 3]
    expected_output = [[1, 2, 3]]
    assert list_separator(input_list, max_len=3) == expected_output

    input_list = [1, 2, 3, 4, 5, 6]
    expected_output = [[1, 2, 3], [4, 5, 6]]
    assert list_separator(input_list, max_len=3) == expected_output

    input_list = []
    expected_output = [[]]
    assert list_separator(input_list) == expected_output


def test_get_number_unique_users_text():
    mock_number_unique_users = MagicMock(return_value=10)

    with patch("bot.utils.statistics.get_number_unique_users", mock_number_unique_users):
        result = get_number_unique_users_text()

    assert result == "Количество уникальных пользователей: 10"
    mock_number_unique_users.assert_called_once()
