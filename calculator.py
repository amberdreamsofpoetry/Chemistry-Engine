# we want to model (3+2)*5.

from Atom import Atom
from Registry import Reserved_Property_Names
import math
from Visualizer import Visualizer


three = Atom()
three.value = 3
three.process = lambda x, _: x
three.name = '3'
two = Atom()
two.value = 2
two.process = lambda x, _: x
two.name = '2'
five = Atom()
five.value = 5
five.process = lambda x, _: x
five.name = '5'

sumOperator = Atom()
sumOperator.process = lambda _, x: sum(dict(x).values())
sumOperator.name = 'sum'
productOperator = Atom()
productOperator.process = lambda _, x: math.prod(dict(x).values())
productOperator.name = 'product'

output = Atom()
output.process = lambda _, x: next(iter(dict(x).values()))

sumOperator.properties[Reserved_Property_Names.INPUT_SOURCES] = {three, two}
productOperator.properties[Reserved_Property_Names.INPUT_SOURCES] = {sumOperator, five}

output.properties[Reserved_Property_Names.INPUT_SOURCES] = {productOperator}
output.name = str(output.emit())

Visualizer(properties={Reserved_Property_Names.INPUT_SOURCES: {three, two, five, sumOperator, productOperator, output}}).emit()
