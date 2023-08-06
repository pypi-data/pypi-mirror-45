"""
Dummy user directory.

Unless explicitly instantiated with `users` (not possible from a config file,
primarily a mechanism for unit tests), this boldly claims that no users exist.

For projects which are not relying on constraints in experiments, this may be
sufficient.
"""

from jacquard.directory.base import Directory


class DummyDirectory(Directory):
    """Dummy user directory."""

    def __init__(self, users=()):
        """
        Initialise.

        If `users` is given it should be an iterable of `UserEntry` instances.
        This is likely only to be useful in tests, given that one cannot
        construct `UserEntry` instances in a config file.
        """
        self.users = {str(x.id): x for x in users}

    def lookup(self, user_id):
        """Look up user by ID."""
        return self.users.get(str(user_id))
