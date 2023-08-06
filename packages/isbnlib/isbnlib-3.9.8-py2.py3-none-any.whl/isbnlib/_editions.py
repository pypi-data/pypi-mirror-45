# -*- coding: utf-8 -*-
"""Return editions for a given ISBN."""

import logging

from ._core import EAN13
from .dev import vias
from ._exceptions import NotRecognizedServiceError, NotValidISBNError
from ._openled import query as oed
from ._thinged import query as ted

PROVIDERS = ('any', 'merge', 'openl', 'thingl')
TRUEPROVIDERS = ('openl', 'thingl')  # <-- by priority
LOGGER = logging.getLogger(__name__)


def fake_provider_any(isbn):
    """Fake provider 'any' service."""
    providers = {'openl': oed, 'thingl': ted}
    for provider in TRUEPROVIDERS:
        data = []
        try:
            data = providers[provider](isbn)
            if len(data) > 1:
                return data
            continue  # pragma: no cover
        except Exception:  # pragma: no cover
            continue
    return data  # pragma: no cover


def fake_provider_merge(isbn):
    """Fake provider 'merge' service."""
    try:  # pragma: no cover
        named_tasks = (('openl', oed), ('thingl', ted))
        results = vias.parallel(named_tasks, isbn)
        odata = results.get('openl', [])
        tdata = results.get('thingl', [])
        data = list(set(odata + tdata))
        return data
    except Exception:  # pragma: no cover
        return []


def editions(isbn, service='merge'):
    """Return the list of ISBNs of editions related with this ISBN."""
    isbn = EAN13(isbn)
    if not isbn:
        LOGGER.critical('%s is not a valid ISBN', isbn)
        raise NotValidISBNError(isbn)

    if service not in PROVIDERS:
        LOGGER.critical('%s is not a recognized editions provider', service)
        raise NotRecognizedServiceError(service)

    from .registry import metadata_cache
    cache = metadata_cache
    key = 'ed' + isbn + service
    # some kinds of cache don't implement get!
    # so don't use cache.get(key)
    # BUG #58
    try:
        if cache[key]:
            return cache[key]
        else:  # pragma: no cover
            raise KeyError  # <-- IMPORTANT: "caches don't return error"!
    except KeyError:
        if service == 'merge':
            eds = fake_provider_merge(isbn)
        if service == 'any':
            eds = fake_provider_any(isbn)

        if service == 'openl':
            eds = oed(isbn)
        if service == 'thingl':
            eds = ted(isbn)

        if eds:
            cache[key] = eds
            return eds
    return []
