"""Prove the suite never opens real sockets when isolation is enabled."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.usefixtures("_dummy_api_env")


def test_socket_disabled_blocks_outbound():
    pytest.importorskip("pytest_socket")
    import socket

    with pytest.raises((RuntimeError, OSError, socket.error)):
        socket.create_connection(("1.1.1.1", 80), timeout=0.2)
