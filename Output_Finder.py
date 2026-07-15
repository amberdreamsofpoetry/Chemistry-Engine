# Output_Finder.py


from Particle import Particle
from typing import Iterable
from Atom import Atom
from typing import Any


class Output_Finder(Atom):
    @staticmethod
    def find_outputs_of_Particle(
        source_Particles: Iterable[Particle],
        potential_output_Particles: Iterable[Particle]
    ) -> dict[Particle, set[Particle]]:
        return {source_Particle: {output_Particle for output_Particle in potential_output_Particles if source_Particle in output_Particle.input_source_Particles} for source_Particle in source_Particles}

    # TODO: make helper arguments for value and inputs
    def __init__(self, properties: dict[str, Any] | None = None) -> None:
        super().__init__(properties)
        self.process = self.find_outputs_of_Particle
    