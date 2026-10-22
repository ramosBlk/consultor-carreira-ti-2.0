import collections
import collections.abc


if not hasattr(collections, "Mapping"):
    setattr(collections, "Mapping", collections.abc.Mapping)