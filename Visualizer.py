# Visualizer.py


from typing import Any, Iterable
from graphviz import Digraph
from Atom import Atom
from Particle import Particle
from Registry import Reserved_Property_Names
from Output_Finder import Output_Finder


class Visualizer(Atom):
    @staticmethod
    def render(_, input_sources: Iterable[Particle]) -> str:
        graph = Digraph()
        input_output_mappings: dict[Particle, set[Particle]] = Output_Finder({Reserved_Property_Names.VALUE: input_sources, Reserved_Property_Names.INPUT_SOURCES: input_sources}).emit()
        for input_Particle in input_output_mappings.keys():
            graph.node(
                name=(input_Particle_node_name := str(id(input_Particle))),
                label=getattr(input_Particle, 'name', str(input_Particle.emit()))
            )
            for output_destination in input_output_mappings[input_Particle]:
                graph.edge(
                    input_Particle_node_name,
                    str(id(output_destination))
                )
        return graph.render("graph", format="png", cleanup=True)
    
    def __init__(self, properties: dict[str, Any] | None = None) -> None:
        super().__init__(properties=properties)
        self.process = self.render
