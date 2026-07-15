# Particle.py


from typing import Protocol, Iterable, Any, Optional


class Particle(Protocol):
    @property
    def input_source_Particles(self) -> set['Particle']:
        ...
    @input_source_Particles.setter
    def input_source_Particles(self, input_source_Particles: Iterable['Particle']):
        ...
    
    def emit(self, cached_emissions: Optional[dict['Particle', Any]] = None) -> Any:
        ...