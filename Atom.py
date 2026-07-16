# Atom.py

from typing import Optional, Any, Iterable, Callable
import logging
from Registry import Reserved_Property_Names
from Particle import Particle

logger = logging.getLogger(__name__)
_IN_PROGRESS = object()
_VALUE_SENTINEL = object()



class Atom:
    def __init__(
        self,
        name: Optional[str] = None,
        value: Optional[Any] = _VALUE_SENTINEL,
        input_source_Particles: Optional[Iterable[Particle]] = None,
        process: Optional[Callable[[Any, dict[Particle, Any]], Any]] = None,
        properties: Optional[dict[str, Any]] = None,
    ) -> None:
        self._properties = dict()
        self._set_reserved_properties(
            name,
            value,
            input_source_Particles,
            process,
        )
        self.set_properties(
            properties or dict(),
            overwrite_existing=False,
            overwrite_all=False,
        )
        self.set_defaults(overwrite=False)


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


    def get_property(
        self,
        property_name: str,
        default_value: Any = None,
    ) -> Any:
        return self.get(property_name, default_value)

    def get(
        self,
        property_name: str,
        default_value: Any = None,
    ) -> Any:
        return self.properties.get(property_name, default_value)
    
    def __getitem__(
        self,
        key: str
    ) -> Any:
        return self.properties[key] # unsafe! use `Atom.get()` if you don't know that the key exists

    def __setitem__(
        self,
        key: str,
        value: Any
    ) -> None:
        if isinstance(key, str):
            self.properties[key] = value
        else:
            raise TypeError(f"Failed to assign invalid (non-string) key {key} in Atom {self.name}.")
        
    def set_property(
        self,
        property_name: str,
        property_value: Any,
        warn_on_reserved: bool = True,
        warn_on_overwrite: bool = False,
    ) -> None:
        if warn_on_reserved and property_name in [reserved_property_name.value for reserved_property_name in Reserved_Property_Names]:
            logger.warning(f"Writing to reserved property {property_name} in Atom {self.name}.")
        if warn_on_overwrite and property_value is not self.get(property_name):
            logger.warning(f"Overwriting property {property_name} in Atom {self.name}.")
        self[property_name] = property_value

    def set_properties(
        self,
        properties: dict[str, Any],
        overwrite_existing: bool = True,
        warn_on_overwrite_existing: bool = False,
        overwrite_all: bool = False,
        warn_on_overwrite_all: bool = True,
    ) -> None:
        if overwrite_all:
            if warn_on_overwrite_all:
                logger.warning(f"Erasing all properties on Atom {self.name}!")
            self.properties = dict() # automatically resets reserved properties to their defaults
        for property_name, property_value in properties.items():
            if overwrite_all or overwrite_existing:
                if property_name in self.properties and warn_on_overwrite_existing:
                    logger.warning(f"Overwriting property {property_name} on Atom {self.name}.")
                self.set_property(property_name, property_value)
            else:
                self.set_default(property_name, property_value)

    def _set_reserved_properties(
        self,
        name: Optional[str],
        value: Any,
        input_source_Particles: Optional[Iterable[Particle]],
        process: Optional[Callable[[Any, dict[Particle, Any]], Any]],
    ) -> None:
        if name is not None:
            self.set_property(
                Reserved_Property_Names.NAME,
                name,
                warn_on_reserved=False,
                warn_on_overwrite=False,
            )
        if value is not _VALUE_SENTINEL:
            self.set_property(
                Reserved_Property_Names.VALUE,
                value,
                warn_on_reserved=False,
                warn_on_overwrite=False,
            )
        if input_source_Particles is not None:
            self.set_property(
                Reserved_Property_Names.INPUT_SOURCE_PARTICLES,
                input_source_Particles,
                warn_on_reserved=False,
                warn_on_overwrite=False,
            )
        if process is not None:
            self.set_property(
                Reserved_Property_Names.PROCESS,
                process,
                warn_on_reserved=False,
                warn_on_overwrite=False,
            )

    def set_default(
        self,
        property_name: str,
        default_value: Any,
    ) -> Any:
        if property_name not in self.properties:
            self[property_name] = default_value
        return self[property_name]
    
    def set_defaults(
        self,
        overwrite: bool,
    ) -> None:
        if overwrite:
            self.set_property(Reserved_Property_Names.NAME, str(id(self)))
            self.set_property(Reserved_Property_Names.VALUE, None)
            self.set_property(Reserved_Property_Names.INPUT_SOURCE_PARTICLES, set())
            self.set_property(Reserved_Property_Names.PROCESS, lambda x, y: (x, y))
        else:
            self.set_default(Reserved_Property_Names.NAME, str(id(self)))
            self.set_default(Reserved_Property_Names.VALUE, None)
            self.set_default(Reserved_Property_Names.INPUT_SOURCE_PARTICLES, set())
            self.set_default(Reserved_Property_Names.PROCESS, lambda x, y: (x, y))


    @property
    def properties(
        self
    ) -> dict[str, Any]:
        return self._properties
    @properties.setter
    def properties(
        self,
        properties: dict[str, Any],
    ) -> None:
        self._properties = properties
        self.set_defaults(overwrite = False)

    @property
    def name(self) -> str | None:
        return self.get(Reserved_Property_Names.NAME)
    @name.setter
    def name(self, name: str) -> None:
        self.properties[Reserved_Property_Names.NAME] = name

    @property
    def value(self) -> Any:
        return self.get(Reserved_Property_Names.VALUE)
    @value.setter
    def value(self, value) -> None:
        self[Reserved_Property_Names.VALUE] = value

    @property
    def input_source_Particles(self) -> set[Particle]:
        return self.get(Reserved_Property_Names.INPUT_SOURCE_PARTICLES)
    @input_source_Particles.setter
    def input_source_Particles(self, input_source_Particles: Iterable[Particle]) -> None:
        self[Reserved_Property_Names.INPUT_SOURCE_PARTICLES] = input_source_Particles

    @property
    def process(self) -> Callable[[Any, dict[Particle, Any]], Any]:
        return self.get(Reserved_Property_Names.PROCESS)
    @process.setter
    def process(self, process: Callable[[Any, dict[Particle, Any]], Any]) -> None:
        self[Reserved_Property_Names.PROCESS] = process