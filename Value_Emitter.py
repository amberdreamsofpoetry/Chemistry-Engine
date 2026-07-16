# Value_Emitter.py


from Atom import Atom
from typing import Any, Optional


class Value_Emitter(Atom):
    def __init__(
        self,
        value: Any,
        properties: Optional[dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            name=str(value),
            value=value,
            process = lambda x, _: x,
            properties=properties
        )