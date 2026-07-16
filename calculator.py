# calculator.py
# a demo of the Chemistry engine



from Atom import Atom
from Value_Emitter import Value_Emitter
from Registry import Reserved_Property_Names
import math
from Visualizer import Visualizer



# we want to model (3+2)*5.

three = Value_Emitter(3)
two = Value_Emitter(2)
five = Value_Emitter(5)

sumOperator = Atom(
    process=lambda _, x: sum(x.values()),
    name="sum"
)
productOperator = Atom(
    process=lambda _, x: math.prod(x.values()),
    name="product"
)

output = Atom(
    process = lambda _, x: next(iter(dict(x).values()))
)

sumOperator.input_source_Particles = {three, two}
productOperator.input_source_Particles = {sumOperator, five}

output.input_source_Particles = {productOperator}
output.name = str(output.emit())

Visualizer(properties={Reserved_Property_Names.INPUT_SOURCE_PARTICLES: {three, two, five, sumOperator, productOperator, output}}).emit()

print(output.emit())
