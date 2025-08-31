"""
Tests for CLIck utility functions
"""

import pytest
from datetime import datetime, timedelta
from src.utils import parse_date, validate_priority
from src.models import Priority


def test_parse_date_relative():
    """Test parsing relative dates"""
    today = parse_date("today")
    assert today.date() == datetime.now().date()

    tomorrow = parse_date("tomorrow")
    expected_tomorrow = (datetime.now() + timedelta(days=1)).date()
    assert tomorrow.date() == expected_tomorrow


def test_parse_date_iso_format():
    """Test parsing ISO date format"""
    date = parse_date("2025-01-15")
    assert date.year == 2025
    assert date.month == 1
    assert date.day == 15


def test_parse_date_invalid():
    """Test parsing invalid date returns None"""
    assert parse_date("invalid-date") is None
    assert parse_date("") is None
    assert parse_date(None) is None


def test_validate_priority():
    """Test priority validation"""
    assert validate_priority("high") is True
    assert validate_priority("medium") is True
    assert validate_priority("low") is True
    assert validate_priority("invalid") is False
