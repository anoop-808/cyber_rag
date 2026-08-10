"""Tests for fetch_nvd_feed script."""

import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
from scripts.fetch_nvd_feed import fetch_feed

@patch("scripts.fetch_nvd_feed.urllib.request.urlopen")
def test_fetch_feed_success(mock_urlopen, tmp_path):
    mock_response = MagicMock()
    mock_response.read.return_value = b"fake gzip data"
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response
    
    dest_dir = tmp_path / "raw"
    dest_dir.mkdir()
    
    fetch_feed(2021, dest_dir)
    
    dest_file = dest_dir / "nvdcve-2.0-2021.json.gz"
    assert dest_file.exists()
    assert dest_file.read_bytes() == b"fake gzip data"

def test_fetch_feed_skips_existing(tmp_path):
    dest_dir = tmp_path / "raw"
    dest_dir.mkdir()
    dest_file = dest_dir / "nvdcve-2.0-2021.json.gz"
    dest_file.write_bytes(b"existing data")
    
    with patch("scripts.fetch_nvd_feed.urllib.request.urlopen") as mock_urlopen:
        fetch_feed(2021, dest_dir)
        mock_urlopen.assert_not_called()
        assert dest_file.read_bytes() == b"existing data"
        
        # Test force
        mock_response = MagicMock()
        mock_response.read.return_value = b"new data"
        mock_response.__enter__.return_value = mock_response
        mock_urlopen.return_value = mock_response
        
        fetch_feed(2021, dest_dir, force=True)
        mock_urlopen.assert_called_once()
        assert dest_file.read_bytes() == b"new data"
