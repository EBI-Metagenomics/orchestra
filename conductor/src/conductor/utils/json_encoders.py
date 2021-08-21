"""JSON Encoders."""

import json
from typing import Any
from uuid import UUID


class UUIDEncoder(json.JSONEncoder):
    """UUID Json encoder."""

    def default(self: "UUIDEncoder", obj: Any) -> Any:
        """Convert UUID to str.

        Args:
            obj (Any): Object

        Returns:
            Any: [description]
        """
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
