import json
from pathlib import Path
import pytest
from rich import print as rich_print
from hypothesis import given, strategies as st
from faker import Faker
from src.testdata.user import User


fake = Faker()


@pytest.mark.user
def test_user():
    """
    use the fake method
    """
    Path("target").mkdir(parents=True, exist_ok=True)
    file_path = Path("target/users.json")
    users = [json.loads(User.fake().json()) for _ in range(20)]
    with open(file_path, "w") as json_file:
        json.dump(users, json_file)

    from_file = None
    with open(file_path, "r") as json_file:
        from_file = [User(**user) for user in json.load(json_file)]
    rich_print(from_file)


@pytest.mark.user
@given(st.builds(User))
def test_many_users(instance):
    """
    hypothesis create many Users
    """
    rich_print(instance)
