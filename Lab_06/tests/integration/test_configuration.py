from application.config import get_config


def test_configuration_loading(monkeypatch):
    monkeypatch.setenv("LOW_STOCK_THRESHOLD", "15")
    monkeypatch.setenv("APP_ENV", "testing")

    config = get_config()
    assert config.low_stock_threshold == 15
    assert config.environment == "testing"