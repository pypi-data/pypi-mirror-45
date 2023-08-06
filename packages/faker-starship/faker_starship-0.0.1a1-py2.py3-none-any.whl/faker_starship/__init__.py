"""A provider of multi-universe starship data for use with Faker."""

from faker.providers import BaseProvider

from . import library


class Provider(BaseProvider):
    """
    A Faker Provider for starship-related test data.

    >>> from faker import Faker
    >>> from faker_starship import Provider as StarshipProvider
    >>> f = Faker()
    >>> f.add_provider(StarshipProvider)
    """

    def _get(self, category, source_name):
        source = getattr(library, source_name) if source_name else library
        try:
            elements = getattr(source, category)
            return self.random_element(elements)
        except AttributeError:
            raise NotImplementedError(
                "source '{source_name}' does not exist".format(source_name=source_name)
            )

    def starship_name(self, source_name=None):
        """Provide a randomly-selected starship name."""
        return self._get("names", source_name)

    def starship_class(self, source_name=None):
        """Provide a randomly-selected starship class."""
        return self._get("classes", source_name)

    def starship_registry(self, source_name=None):
        """Provide a randomly-selected starship registry."""
        return self._get("registries", source_name)
