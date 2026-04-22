"""StoredFact and related memory types."""

from sonzai._generated.models import StoredFact as _GenStoredFact


class StoredFact(_GenStoredFact):
    """Stored fact returned by fact recall endpoints."""
