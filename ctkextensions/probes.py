from chaoslib.exceptions import ActivityFailed
from chaoslib.types import Configuration
import requests

__all__ = ["alert_is_not_firing"]


def alert_is_not_firing(alert_name: str, container_name: str,
                        configuration: Configuration) -> bool:
    """
    Lookup for a specific alert on a given container and see if its status
    is either `pending` or `firing`. If either, it returns `False` so that
    the tolerance will fail.
    """
    base = (configuration or {}).get(
        "prometheus_base_url", "http://localhost:9090")
    url = "{base}/api/v1/alerts".format(base=base)

    r = requests.get(url, headers={"Accept": "application/json"})
    if r.status_code > 399:
        raise ActivityFailed("Prometheus alert failed: {m}".format(m=r.text))

    alerts = r.json()
    alerts = alerts.get("data", {"alerts": []}).get("alerts", [])

    for alert in alerts:
        labels = alert["labels"]
        if labels["alertname"] == alert_name and \
            labels["container"] == container_name and \
            alert["state"] in ("pending", "firing"):
                return False
    return True
