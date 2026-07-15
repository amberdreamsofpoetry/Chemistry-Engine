# Atom.py


from typing import Optional, Any, Iterable, Callable
import logging
logger = logging.getLogger(__name__)
from Registry import Reserved_Property_Names
from Particle import Particle

_IN_PROGRESS = object()

class Atom:
    def __init__(
        self,
        properties: Optional[dict[str, Any]] = None,
        log_dropped_properties: bool = True,
    ) -> None:
        properties = properties or dict()
        self.properties = dict()
        for key, value in properties.items():
            if isinstance(key, str):
                self.properties[key] = value
            elif log_dropped_properties:
                logger.warning(f"Dropped invalid (non-string) key {key}.")

    @property
    def input_source_Particles(self) -> set[Particle]:
        return self.properties.get(Reserved_Property_Names.INPUT_SOURCES) or set()
    @input_source_Particles.setter
    def input_source_Particles(self, input_source_Particles: Iterable[Particle]) -> None:
        self.properties[Reserved_Property_Names.INPUT_SOURCES] = set(input_source_Particles)

    @property
    def value(self) -> Any:
        return self.properties.get(Reserved_Property_Names.VALUE)
    @value.setter
    def value(self, value) -> None:
        self.properties[Reserved_Property_Names.VALUE] = value

    @property
    def process(self) -> Callable[[Any, dict[Particle, Any]], Any]:
        return self.properties.get(Reserved_Property_Names.PROCESS) or (lambda x, y: (x, y))
    @process.setter
    def process(self, process) -> None:
        self.properties[Reserved_Property_Names.PROCESS] = process

    @property
    def name(self) -> str:
        return self.properties.get(Reserved_Property_Names.NAME) or str(id(self))
    @name.setter
    def name(self, name: str) -> None:
        self.properties[Reserved_Property_Names.NAME] = name

    def emit(
        self,
        cached_emissions: Optional[dict[Particle, Any]] = None,
    ) -> Any:
        cached_emissions = cached_emissions or dict()
        if self in cached_emissions:
            if (cached_emission := cached_emissions[self]) is _IN_PROGRESS:
                raise Exception(f"Cycle detected at {self}")
            return cached_emission
        cached_emissions[self] = _IN_PROGRESS
        cached_emissions[self] = self.process(self.value, {input_source_Particle: input_source_Particle.emit(cached_emissions) for input_source_Particle in self.input_source_Particles})
        return cached_emissions[self]
