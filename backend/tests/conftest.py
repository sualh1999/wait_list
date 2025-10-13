import pytest
import os

@pytest.fixture(autouse=True)
def set_test_env_vars(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    monkeypatch.setenv("RESEND_API_KEY", "test_resend_key")
    monkeypatch.setenv("ADMIN_PASSWORD", "test_admin_password")
    monkeypatch.setenv("ALLOWED_ORIGINS", "http://localhost,http://localhost:3000")