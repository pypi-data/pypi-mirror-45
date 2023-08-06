# -*- coding: utf-8 -*-
# flake8: noqa
# pylint: skip-file

try:
    from time import process_time
except:
    pass

from nose.tools import assert_equals, raises

from .._exceptions import NotRecognizedServiceError, NotValidISBNError
from .._ext import editions

# nose tests



def test_editions_openl():
    """Test the 'openl editions' service."""
    assert_equals(len(editions('9780099536017', service='openl')) > 4, True)


def test_editions_thingl():
    """Test the 'thingl editions' service."""
    assert_equals(len(editions('9780151446476', service='thingl')) > 19, True)


def test_editions_any():
    """Test the 'any editions' service."""
    assert_equals(len(editions('9780151446476', service='any')) > 19, True)


def test_editions_merge():
    """Test the 'merge editions' service."""
    assert_equals(len(editions('9780151446476', service='merge')) > 19, True)


@raises(NotValidISBNError)
def test_editions_NotValidISBNError():
    """Test the 'editions' service error detection (NotValidISBNError)."""
    editions('978')


@raises(NotRecognizedServiceError)
def test_editions_NotRecognizedServiceError():
    """Test the 'editions' service error detection (NotRecognizedServiceError)."""
    editions('9780156001311', service='xxx')

def test_cache():
    """Test the 'editions' cache."""
    try:
        t = process_time()
        assert_equals(len(editions('9780151446476', service='merge')) > 19, True)
        elapsed_time = process_time() - t
        millis = int(elapsed_time * 1000)
        assert millis < 100
    except:
        pass
