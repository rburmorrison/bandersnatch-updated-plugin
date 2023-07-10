"""Defines the UpdatedFilter plugin for filtering out old packages."""

import logging

from datetime import datetime, timezone
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
from configparser import SectionProxy
from bandersnatch.filter import FilterMetadataPlugin, Filter


logger = logging.getLogger("bandersnatch")


class UpdatedFilter(FilterMetadataPlugin, Filter):
    """Plugin to only download packages with a recent release."""

    name = "updated"
    minimum_date: datetime

    def initialize_plugin(self: "UpdatedFilter") -> None:
        """Load settings from the config file."""
        try:
            config: SectionProxy = self.configuration[self.name]
        except KeyError:
            return

        maximum_years = int(config["maximum_years"])
        self.minimum_date = datetime.now(timezone.utc) - relativedelta(
            years=maximum_years
        )

        logger.info(f"Initialized updated plugin with maximum_years={maximum_years}")

        self.initialized = True

    def filter(self: "UpdatedFilter", metadata: dict) -> bool:
        """Filter packages that don't match the configured filters."""
        upload_time = metadata["release_file"]["upload_time_iso_8601"]
        release_time = parse(upload_time)
        new_enough = release_time >= self.minimum_date
        return new_enough
