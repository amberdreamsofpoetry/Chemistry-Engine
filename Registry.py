# Registry.py



from enum import Enum



class Reserved_Property_Names(str, Enum):
    VALUE = "value"

    INPUT_SOURCE_PARTICLES = "input_source_Particles"
    PROCESS = "process"

    NAME = "name"
