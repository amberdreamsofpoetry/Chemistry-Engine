# Molecule.py


from typing import Optional, Iterable, Any
from Particle import Particle
from Atom import Atom


_IN_PROGRESS = object()
class Molecule:
    def __init__(
        self,
        input_Particle: Optional[Particle] = None,
        output_Particle: Optional[Particle] = None,
        name: Optional[str] = None,
    ) -> None:
        self.input_Particle = input_Particle or Atom()
        self.output_Particle = output_Particle or Atom()
        self._name = name if name is not None else str(id(self))

    @property
    def input_source_Particles(self) -> set[Particle]:
        return self.input_Particle.input_source_Particles
    @input_source_Particles.setter
    def input_source_Particles(self, input_source_Particles: Iterable[Particle]) -> None:
        self.input_Particle.input_source_Particles = set(input_source_Particles)

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def emit(
        self,
        cached_emissions: Optional[dict[Particle, Any]] = None
    ) -> Any:
        cached_emissions = cached_emissions or dict()
        if self in cached_emissions:
            if (cached_emission := cached_emissions[self]) is _IN_PROGRESS:
                raise Exception(f"Cycle detected at {self}")
            return cached_emission
        cached_emissions[self] = _IN_PROGRESS
        cached_emissions[self] = self.output_Particle.emit(cached_emissions)
        return cached_emissions[self]
