from app.tools.diagnostics import run_simulated_diagnostics

def test_vpn_diagnostics_are_simulated():
    result = run_simulated_diagnostics("vpn_network", "VPN failure", "DNS lookup fails")
    assert "vpn_service" in result
    assert all("SIMULATED" in value for value in result.values())

def test_access_diagnostics_do_not_request_secrets():
    result = run_simulated_diagnostics("access_account", "Login issue", "MFA failed")
    assert "Never request passwords" in result["security_note"]
