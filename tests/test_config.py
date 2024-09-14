from src.config import config


def test_config():
    assert len(config(filename="database_test.ini", section="postgresql")) == 3
