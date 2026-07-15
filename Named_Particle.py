# Named_Particle.py


from Particle import Particle
from typing import Protocol

class Named_Particle(Particle, Protocol):
    @property
    def name(self) -> str:
        ...
    @name.setter
    def name(self, name: str) -> None:
        ...
