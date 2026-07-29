"""
Reusable helpers not tied to any single page — data generation, waits, etc.
"""
from faker import Faker

fake = Faker()


def random_email() -> str:
    return fake.email()


def random_username() -> str:
    return fake.user_name()


def random_password(length: int = 12) -> str:
    return fake.password(length=length)


def random_full_name() -> str:
    return fake.name()


def random_first_name() -> str:
    return fake.first_name()


def random_last_name() -> str:
    return fake.last_name()


def random_zip_code() -> str:
    return fake.postcode()
