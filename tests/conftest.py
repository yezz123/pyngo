import asyncio
from typing import Generator

import pytest


@pytest.fixture
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Fixture for the event loop.
    Yields:
        asyncio.AbstractEventLoop: The event loop.
    """
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


def test_event_loop(event_loop: asyncio.AbstractEventLoop) -> None:
    """
    Test the event loop fixture.
    Args:
        event_loop (asyncio.AbstractEventLoop): The event loop.
    Returns:
        None
    """
    assert event_loop.is_running()
