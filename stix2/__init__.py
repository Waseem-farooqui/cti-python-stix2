import collections
from datetime import datetime
import json
import uuid

import pytz


def format_datetime(dt):
    # TODO: how to handle naive datetime

    # 1. Convert to UTC
    # 2. Format in isoformat
    # 3. Strip off "+00:00"
    # 4. Add "Z"

    # TODO: how to handle timestamps with subsecond 0's
    return dt.astimezone(pytz.utc).isoformat()[:-6] + "Z"


class _STIXBase(collections.Mapping):
    """Base class for STIX object types"""

    def __getitem__(self, key):
        return self._inner[key]

    def __iter__(self):
        return iter(self._inner)

    def __len__(self):
        return len(self._inner)

    # Handle attribute access just like key access
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        if name != '_inner':
            raise ValueError("Cannot modify properties after creation.")
        super(_STIXBase, self).__setattr__(name, value)

    def __str__(self):
        # TODO: put keys in specific order. Probably need custom JSON encoder.
        return json.dumps(self._dict(), indent=4, sort_keys=True,
                          separators=(",", ": "))  # Don't include spaces after commas.


class Indicator(_STIXBase):

    _properties = [
        'type',
        'id',
        'created',
        'modified',
        'labels',
        'pattern',
        'valid_from',
    ]

    def __init__(self, **kwargs):
        # TODO:
        # - created_by_ref
        # - revoked
        # - external_references
        # - object_marking_refs
        # - granular_markings

        # - name
        # - description
        # - valid_until
        # - kill_chain_phases

        # TODO: do we care about the performance penalty of creating this
        # if we won't need it?
        now = datetime.now(tz=pytz.UTC)

        if not kwargs.get('type'):
            kwargs['type'] = 'indicator'
        if kwargs['type'] != 'indicator':
            raise ValueError("Indicator must have type='indicator'.")

        if not kwargs.get('id'):
            kwargs['id'] = 'indicator--' + str(uuid.uuid4())
        if not kwargs['id'].startswith('indicator--'):
            raise ValueError("Indicator id values must begin with 'indicator--'.")

        if not kwargs.get('labels'):
            raise ValueError("Missing required field for Indicator: 'labels'.")

        if not kwargs.get('pattern'):
            raise ValueError("Missing required field for Indicator: 'pattern'.")

        extra_kwargs = list(set(kwargs.keys()) - set(self._properties))
        if extra_kwargs:
            raise TypeError("unexpected keyword arguments: " + str(extra_kwargs))

        self._inner = {
            'type': kwargs['type'],
            'id': kwargs['id'],
            'created': kwargs.get('created', now),
            'modified': kwargs.get('modified', now),
            'labels': kwargs['labels'],
            'pattern': kwargs['pattern'],
            'valid_from': kwargs.get('valid_from', now),
        }

    def _dict(self):
        return {
            'type': self['type'],
            'id': self['id'],
            'created': format_datetime(self['created']),
            'modified': format_datetime(self['modified']),
            'labels': self['labels'],
            'pattern': self['pattern'],
            'valid_from': format_datetime(self['valid_from']),
        }


class Malware(_STIXBase):

    _properties = [
        'type',
        'id',
        'created',
        'modified',
        'labels',
        'name',
    ]

    def __init__(self, **kwargs):
        # TODO:
        # - created_by_ref
        # - revoked
        # - external_references
        # - object_marking_refs
        # - granular_markings

        # - description
        # - kill_chain_phases

        # TODO: do we care about the performance penalty of creating this
        # if we won't need it?
        now = datetime.now(tz=pytz.UTC)

        if not kwargs.get('type'):
            kwargs['type'] = 'malware'
        if kwargs['type'] != 'malware':
            raise ValueError("Malware must have type='malware'.")

        if not kwargs.get('id'):
            kwargs['id'] = 'malware--' + str(uuid.uuid4())
        if not kwargs['id'].startswith('malware--'):
            raise ValueError("Malware id values must begin with 'malware--'.")

        if not kwargs.get('labels'):
            raise ValueError("Missing required field for Malware: 'labels'.")

        if not kwargs.get('name'):
            raise ValueError("Missing required field for Malware: 'name'.")

        extra_kwargs = list(set(kwargs.keys()) - set(self._properties))
        if extra_kwargs:
            raise TypeError("unexpected keyword arguments: " + str(extra_kwargs))

        self._inner = {
            'type': kwargs['type'],
            'id': kwargs['id'],
            'created': kwargs.get('created', now),
            'modified': kwargs.get('modified', now),
            'labels': kwargs['labels'],
            'name': kwargs['name'],
        }

    def _dict(self):
        return {
            'type': self['type'],
            'id': self['id'],
            'created': format_datetime(self['created']),
            'modified': format_datetime(self['modified']),
            'labels': self['labels'],
            'name': self['name'],
        }
