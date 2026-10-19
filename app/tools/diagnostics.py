def run_simulated_diagnostics(category: str, title: str, description: str) -> dict[str, str]:
    """Return mock diagnostic observations; never contacts real systems."""
    text = f"{title} {description}".lower()
    if category == "vpn_network":
        result = {"internet_connectivity": "SIMULATED: no real network check performed",
                  "vpn_service": "SIMULATED: service status unknown; check approved status page"}
        if "dns" in text or "resolve" in text:
            result["dns"] = "SIMULATED: DNS lookup not performed; collect hostname and error"
        return result
    if category == "application":
        return {"application_health": "SIMULATED: no live endpoint queried", "http_status": "SIMULATED: capture timestamp and request ID"}
    if category == "access_account":
        return {"identity_status": "SIMULATED: account status not queried; use approved identity workflow",
                "security_note": "Never request passwords or MFA codes"}
    if category == "hardware":
        return {"device_check": "SIMULATED: physical inspection not performed"}
    return {"software_check": "SIMULATED: no device changes or commands were run"}
