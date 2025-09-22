"""
Network visibility and monitoring tools for kn-sock.

⚠️  WARNING: This module is intended for use in authorized networks such as schools, 
labs, or controlled IT environments. Monitoring user traffic may be illegal without 
explicit consent. Use responsibly and ethically.
"""

# Import and re-export callables so `from kn_sock.network import mac_lookup`
# yields a function (callable) rather than the submodule.
from .arp import arp_scan  # noqa: F401
from .monitor import monitor_dns  # noqa: F401

# Export a callable mac_lookup that also exposes a 'requests' attribute
from . import mac_lookup as _mac_lookup_module  # noqa: F401
from .mac_lookup import mac_lookup as _mac_lookup_func

# Attach the requests module to the function so patch targets like
# 'kn_sock.network.mac_lookup.requests.get' resolve correctly during tests
try:
    _mac_lookup_func.requests = _mac_lookup_module.requests  # type: ignore[attr-defined]
except Exception:
    pass

mac_lookup = _mac_lookup_func  # re-export

__all__ = ["arp_scan", "mac_lookup", "monitor_dns"]

# Version info
__version__ = "0.3.0a1"
