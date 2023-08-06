"""User constraints predicates."""

import warnings
import collections

import dateutil.tz
import dateutil.parser

from jacquard.utils import check_keys

ConstraintContext = collections.namedtuple("ConstraintContext", ("era_start_date",))


ConstraintContext.__doc__ = """Context for evaluating constraints."""

ConstraintContext.era_start_date.__doc__ = """
Considered "start date" of the era of this experiment.

Used in the `era` key. Generally experiment launch date.
"""


class Constraints(object):
    """
    Constraints definition.

    This can filter by:

    era
      The era, 'old' or 'new' relative to the experiment start date, for users
      included in these constraints.

    required_tags
      A sequence of tags, all of which are required for a user to be in these
      constraints.

    excluded_tags
      A sequence of tags, any of which will exclude a user from this test.
    """

    def __init__(
        self,
        era=None,
        required_tags=(),
        excluded_tags=(),
        joined_before=None,
        joined_after=None,
    ):
        """
        Manual constructor.

        Can be called with no arguments for the "universal constraints" - the
        constraints which are equivalent to unconditionally matching users.

        Generally prefer `.from_json`.
        """
        self.era = era

        if era not in (None, "old", "new"):
            raise ValueError("Invalid era: {era}".format(era=era))

        self.required_tags = tuple(required_tags)
        self.excluded_tags = tuple(excluded_tags)

        self.joined_before = joined_before
        self.joined_after = joined_after

    def __bool__(self):
        """Whether these constraints are non-universal."""
        if (
            self.era
            or self.required_tags
            or self.excluded_tags
            or self.joined_after
            or self.joined_before
        ):
            return True

        return False

    @classmethod
    def from_json(cls, description):
        """Generate constraints from a JSON description."""
        check_keys(
            description.keys(),
            (
                "anonymous",
                "named",
                "era",
                "required_tags",
                "excluded_tags",
                "joined_before",
                "joined_after",
            ),
        )

        if "anonymous" in description:
            warnings.warn("The `anonymous` flag no longer has any effect.")

        if "named" in description:
            warnings.warn("The `named` flag no longer has any effect.")

        def get_maybe_date(key):
            try:
                string_date = description[key]
            except KeyError:
                return None

            parsed_date = dateutil.parser.parse(string_date)

            if parsed_date.tzinfo is None:
                raise ValueError("Constraint dates must explicitly include timezones.")

            return parsed_date

        return cls(
            era=description.get("era"),
            required_tags=description.get("required_tags", ()),
            excluded_tags=description.get("excluded_tags", ()),
            joined_before=get_maybe_date("joined_before"),
            joined_after=get_maybe_date("joined_after"),
        )

    def to_json(self):
        """
        Produce a JSON description.

        A pseudo-inverse of `.from_json`.
        """
        description = {}

        if self.era is not None:
            description["era"] = self.era

        if self.required_tags:
            description["required_tags"] = self.required_tags

        if self.excluded_tags:
            description["excluded_tags"] = self.excluded_tags

        if self.joined_after:
            description["joined_after"] = str(self.joined_after)

        if self.joined_before:
            description["joined_before"] = str(self.joined_before)

        return description

    def specialise(self, context):
        """A copy, specialised for a given context."""
        joined_before_dates = []
        joined_after_dates = []

        if self.joined_before:
            joined_before_dates.append(self.joined_before)

        if self.joined_after:
            joined_after_dates.append(self.joined_after)

        if self.era == "new":
            joined_after_dates.append(context.era_start_date)

        if self.era == "old":
            joined_before_dates.append(context.era_start_date)

        if joined_before_dates:
            joined_before = min(joined_before_dates)
        else:
            joined_before = None

        if joined_after_dates:
            joined_after = max(joined_after_dates)
        else:
            joined_after = None

        return type(self)(
            joined_before=joined_before,
            joined_after=joined_after,
            required_tags=self.required_tags,
            excluded_tags=self.excluded_tags,
        )

    def matches_user(self, user, context=None):
        """Test matching a user, potentially in a given context."""
        if context is not None:
            return self.specialise(context).matches_user(user)

        if user is None:
            # Anonymous users unconditionally fail constraints
            return False

        if self.joined_before and user.join_date > self.joined_before:
            return False

        if self.joined_after and user.join_date < self.joined_after:
            return False

        if any(x not in user.tags for x in self.required_tags):
            return False

        if any(x in user.tags for x in self.excluded_tags):
            return False

        return True

    def is_provably_disjoint_from_constraints(self, other_constraints):
        """Test whether constraints are provably disjoint."""
        if (
            set(self.required_tags) & set(other_constraints.excluded_tags)
            or set(self.excluded_tags) & set(other_constraints.required_tags)
        ):
            return True

        if (
            self.joined_after is not None
            and other_constraints.joined_before is not None
            and self.joined_after >= other_constraints.joined_before
        ):
            return True

        if (
            self.joined_before is not None
            and other_constraints.joined_after is not None
            and self.joined_before < other_constraints.joined_after
        ):
            return True

        return False
