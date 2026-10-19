from app.ml.classifier import TicketClassifier

def test_classifier_returns_probability_distribution():
    result = TicketClassifier().predict("VPN login failure", "Cannot connect to VPN after password reset")
    assert result["category"] in {"vpn_network", "access_account", "application", "hardware", "software"}
    assert 0 <= result["confidence"] <= 1
    assert abs(sum(result["probabilities"].values()) - 1) < 1e-5
