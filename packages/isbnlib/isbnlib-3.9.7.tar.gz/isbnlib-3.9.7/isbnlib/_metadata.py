# -*- coding: utf-8 -*-
"""Query providers for metadata."""

from ._core import EAN13
from ._exceptions import NotRecognizedServiceError, NotValidISBNError


def query(isbn, service='default', cache='default'):
    """Query services like Google Books (JSON API), ... for metadata."""
    # validate inputs
    ean = EAN13(isbn)
    if not ean:
        raise NotValidISBNError(isbn)
    isbn = ean
    # only import when needed (code splitting)
    from .registry import services
    if service != 'default' and service not in services:  # pragma: no cover
        raise NotRecognizedServiceError(service)
    # set cache and get metadata
    if cache is None:  # pragma: no cover
        return services[service](isbn)
    if cache == 'default':
        from .registry import metadata_cache
        cache = metadata_cache
    key = isbn + service
    try:
        if cache[key]:
            return cache[key]
        else:  # pragma: no cover
            raise KeyError  # <-- IMPORTANT: "caches don't return error"!
    except KeyError:
        meta = services[service](isbn)
        if meta:
            cache[key] = meta
        return meta if meta else None
