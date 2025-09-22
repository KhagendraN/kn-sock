"""
Tests for the network module functionality.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock

from kn_sock.network.arp import (
    arp_scan,
    arp_scan_simple,
    get_local_network_info,
    _normalize_mac,
    _get_oui_from_mac
)
from kn_sock.network.mac_lookup import (
    mac_lookup,
    mac_lookup_offline,
    validate_mac,
    _normalize_mac as mac_normalize
)
from kn_sock.network.monitor import (
    monitor_dns,
    analyze_dns_logs,
    get_network_interfaces,
    _check_scapy_available,
    _check_privileges
)


class TestARPScanning(unittest.TestCase):
    """Test ARP scanning functionality."""

    def test_normalize_mac(self):
        """Test MAC address normalization."""
        # Test various MAC formats
        test_cases = [
            ("00:1A:2B:3C:4D:5E", "00:1A:2B:3C:4D:5E"),
            ("00-1A-2B-3C-4D-5E", "00:1A:2B:3C:4D:5E"),
            ("001A2B3C4D5E", "00:1A:2B:3C:4D:5E"),
            ("00:1a:2b:3c:4d:5e", "00:1A:2B:3C:4D:5E"),
        ]
        
        for input_mac, expected in test_cases:
            with self.subTest(mac=input_mac):
                result = _normalize_mac(input_mac)
                self.assertEqual(result, expected)

    def test_normalize_mac_invalid(self):
        """Test MAC address normalization with invalid input."""
        invalid_macs = [
            "00:1A:2B:3C:4D",  # Too short
            "00:1A:2B:3C:4D:5E:6F",  # Too long
            "00:1A:2B:3C:4G:5E",  # Invalid character
            "not-a-mac",  # Not hex
        ]
        
        for invalid_mac in invalid_macs:
            with self.subTest(mac=invalid_mac):
                with self.assertRaises(ValueError):
                    _normalize_mac(invalid_mac)

    def test_get_oui_from_mac(self):
        """Test OUI extraction from MAC address."""
        mac = "00:1A:2B:3C:4D:5E"
        expected_oui = "00:1A:2B"
        result = _get_oui_from_mac(mac)
        self.assertEqual(result, expected_oui)

    @patch('kn_sock.network.arp._check_scapy_available')
    def test_arp_scan_no_scapy(self, mock_check):
        """Test ARP scan when scapy is not available."""
        mock_check.return_value = False
        
        with self.assertRaises(ImportError):
            arp_scan("192.168.1.0/24")

    @patch('kn_sock.network.arp._check_scapy_available')
    @patch('kn_sock.network.arp.scapy')
    def test_arp_scan_success(self, mock_scapy, mock_check):
        """Test successful ARP scan."""
        mock_check.return_value = True
        
        # Mock scapy response
        recv_pkt = MagicMock()
        recv_pkt.psrc = "192.168.1.1"
        recv_pkt.hwsrc = "00:1A:2B:3C:4D:5E"
        pair = MagicMock()
        pair.__getitem__.return_value = recv_pkt
        mock_scapy.srp.return_value = ([pair], [])
        
        result = arp_scan("192.168.1.0/24")
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["ip"], "192.168.1.1")
        self.assertEqual(result[0]["mac"], "00:1A:2B:3C:4D:5E")

    def test_arp_scan_simple(self):
        """Test simple ARP scan."""
        with patch('kn_sock.network.arp.arp_scan') as mock_arp_scan:
            mock_arp_scan.return_value = [
                {"ip": "192.168.1.1", "mac": "00:1A:2B:3C:4D:5E"},
                {"ip": "192.168.1.2", "mac": "00:1A:2B:3C:4D:5F"}
            ]
            
            result = arp_scan_simple("192.168.1.0/24")
            
            expected = [
                ("192.168.1.1", "00:1A:2B:3C:4D:5E"),
                ("192.168.1.2", "00:1A:2B:3C:4D:5F")
            ]
            self.assertEqual(result, expected)

    @patch('kn_sock.network.arp.psutil')
    def test_get_local_network_info(self, mock_psutil):
        """Test getting local network information."""
        # Mock psutil network interfaces
        mock_interface = Mock()
        mock_interface.family = 2  # AF_INET
        mock_interface.address = "192.168.1.100"
        mock_psutil.net_if_addrs.return_value = {
            "eth0": [mock_interface]
        }
        
        # Mock subprocess for gateway detection
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.stdout = "default via 192.168.1.1 dev eth0"
            mock_run.return_value.returncode = 0
            
            result = get_local_network_info()
            
            self.assertEqual(result["local_ip"], "192.168.1.100")
            self.assertEqual(result["interface"], "eth0")
            self.assertEqual(result["gateway"], "192.168.1.1")


class TestMACLookup(unittest.TestCase):
    """Test MAC address lookup functionality."""

    def test_validate_mac(self):
        """Test MAC address validation."""
        valid_macs = [
            "00:1A:2B:3C:4D:5E",
            "00-1A-2B-3C-4D-5E",
            "001A2B3C4D5E",
            "00:1a:2b:3c:4d:5e"
        ]
        
        for mac in valid_macs:
            with self.subTest(mac=mac):
                self.assertTrue(validate_mac(mac))

    def test_validate_mac_invalid(self):
        """Test MAC address validation with invalid input."""
        invalid_macs = [
            "00:1A:2B:3C:4D",
            "00:1A:2B:3C:4D:5E:6F",
            "00:1A:2B:3C:4G:5E",
            "not-a-mac"
        ]
        
        for mac in invalid_macs:
            with self.subTest(mac=mac):
                self.assertFalse(validate_mac(mac))

    def test_mac_lookup_offline(self):
        """Test offline MAC lookup."""
        result = mac_lookup_offline("00:50:56:00:00:08")
        
        self.assertEqual(result["mac"], "00:50:56:00:00:08")
        self.assertEqual(result["oui"], "00:50:56")
        self.assertIn("VMware", result["vendor"])
        self.assertEqual(result["source"], "local database")

    def test_mac_lookup_offline_unknown(self):
        """Test offline MAC lookup with unknown MAC."""
        result = mac_lookup_offline("FF:FF:FF:00:00:00")
        
        self.assertEqual(result["mac"], "FF:FF:FF:00:00:00")
        self.assertEqual(result["oui"], "FF:FF:FF")
        self.assertIn("Unknown", result["vendor"])
        self.assertEqual(result["source"], "local database")

    @patch('kn_sock.network.mac_lookup.requests.get')
    def test_mac_lookup_api_success(self, mock_get):
        """Test successful API MAC lookup."""
        mock_response = Mock()
        mock_response.text = "VMware, Inc."
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = mac_lookup("00:50:56:00:00:08", use_api=True)
        
        self.assertEqual(result["vendor"], "VMware, Inc.")
        self.assertEqual(result["source"], "macvendors.co API")

    @patch('kn_sock.network.mac_lookup.requests.get')
    def test_mac_lookup_api_fallback(self, mock_get):
        """Test API MAC lookup with fallback to offline."""
        mock_get.side_effect = Exception("API Error")
        
        result = mac_lookup("00:50:56:00:00:08", use_api=True)
        
        # Should fallback to offline lookup
        self.assertIn("VMware", result["vendor"])
        self.assertEqual(result["source"], "local database")


class TestDNSMonitoring(unittest.TestCase):
    """Test DNS monitoring functionality."""

    def test_check_scapy_available(self):
        """Test scapy availability check."""
        # This test depends on whether scapy is actually installed
        result = _check_scapy_available()
        self.assertIsInstance(result, bool)

    def test_check_privileges(self):
        """Test privilege check."""
        result = _check_privileges()
        self.assertIsInstance(result, bool)

    @patch('kn_sock.network.monitor._check_scapy_available')
    @patch('kn_sock.network.monitor._check_privileges')
    def test_monitor_dns_no_scapy(self, mock_priv, mock_scapy):
        """Test DNS monitoring when scapy is not available."""
        mock_scapy.return_value = False
        mock_priv.return_value = True
        
        with self.assertRaises(ImportError):
            monitor_dns(duration=1)

    @patch('kn_sock.network.monitor._check_scapy_available')
    @patch('kn_sock.network.monitor._check_privileges')
    def test_monitor_dns_no_privileges(self, mock_priv, mock_scapy):
        """Test DNS monitoring when insufficient privileges."""
        mock_scapy.return_value = True
        mock_priv.return_value = False
        
        with self.assertRaises(PermissionError):
            monitor_dns(duration=1)

    def test_analyze_dns_logs(self):
        """Test DNS log analysis."""
        # Create temporary log file
        test_data = [
            {
                "timestamp": "2023-01-01T00:00:00",
                "source_ip": "192.168.1.100",
                "domain": "example.com",
                "query_type": "A"
            },
            {
                "timestamp": "2023-01-01T00:00:01",
                "source_ip": "192.168.1.100",
                "domain": "google.com",
                "query_type": "A"
            },
            {
                "timestamp": "2023-01-01T00:00:02",
                "source_ip": "192.168.1.101",
                "domain": "example.com",
                "query_type": "A"
            }
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f)
            log_file = f.name
        
        try:
            result = analyze_dns_logs(log_file)
            
            self.assertEqual(result["total_requests"], 3)
            self.assertEqual(result["unique_domains"], 2)
            self.assertEqual(result["unique_sources"], 2)
            self.assertEqual(len(result["top_domains"]), 2)
            self.assertEqual(result["top_domains"][0][0], "example.com")
            self.assertEqual(result["top_domains"][0][1], 2)
        finally:
            os.unlink(log_file)

    def test_analyze_dns_logs_file_not_found(self):
        """Test DNS log analysis with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            analyze_dns_logs("nonexistent.json")

    def test_analyze_dns_logs_invalid_json(self):
        """Test DNS log analysis with invalid JSON."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("invalid json content")
            log_file = f.name
        
        try:
            with self.assertRaises(ValueError):
                analyze_dns_logs(log_file)
        finally:
            os.unlink(log_file)

    def test_analyze_dns_logs_empty(self):
        """Test DNS log analysis with empty file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            log_file = f.name
        
        try:
            result = analyze_dns_logs(log_file)
            self.assertEqual(result["total_requests"], 0)
            self.assertIn("message", result)
        finally:
            os.unlink(log_file)

    @patch('kn_sock.network.monitor.psutil')
    def test_get_network_interfaces(self, mock_psutil):
        """Test getting network interfaces."""
        # Mock psutil network interfaces
        mock_interface = Mock()
        mock_interface.family = 2  # AF_INET
        mock_interface.address = "192.168.1.100"
        mock_interface.netmask = "255.255.255.0"
        mock_psutil.net_if_addrs.return_value = {
            "eth0": [mock_interface]
        }
        
        result = get_network_interfaces()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "eth0")
        self.assertEqual(result[0]["ip"], "192.168.1.100")
        self.assertEqual(result[0]["netmask"], "255.255.255.0")

    @patch('kn_sock.network.monitor.psutil')
    def test_get_network_interfaces_no_psutil(self, mock_psutil):
        """Test getting network interfaces when psutil is not available."""
        mock_psutil.side_effect = ImportError()
        
        result = get_network_interfaces()
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "unknown")
        self.assertEqual(result[0]["ip"], "unknown")
        self.assertEqual(result[0]["netmask"], "unknown")


class TestNetworkModuleIntegration(unittest.TestCase):
    """Integration tests for the network module."""

    def test_network_module_imports(self):
        """Test that network module can be imported."""
        from kn_sock.network import arp_scan, mac_lookup, monitor_dns
        
        # Just test that the functions are importable
        self.assertTrue(callable(arp_scan))
        self.assertTrue(callable(mac_lookup))
        self.assertTrue(callable(monitor_dns))

    def test_network_module_all_exports(self):
        """Test that __all__ exports are correct."""
        from kn_sock.network import __all__
        
        expected_exports = ["arp_scan", "mac_lookup", "monitor_dns"]
        self.assertEqual(__all__, expected_exports)


if __name__ == "__main__":
    unittest.main()
