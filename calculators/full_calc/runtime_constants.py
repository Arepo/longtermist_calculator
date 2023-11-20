# pylint: skip-file

# These constants determine runtime, which is something like
# O(MAX_CIVILISATIONS*MAX_PROGRESS_YEARS^2) or O(MAX_CIVILISATIONS*MAX_PLANETS^2) if the
# latter is bigger. So setting them higher substantially increases runtime, but will also increase
# the fidelity of the final output.

# Some example runtimes on my 2019 Macbook Pro:
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 4000, runtime = 997 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 2000, runtime = 180 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 20, MAX_PROGRESS_YEARS = 1000, runtime = 98 seconds
# MAX_PLANETS = 20, MAX_CIVILISATIONS = 10, MAX_PROGRESS_YEARS = 2000, runtime = 196 seconds
# MAX_PLANETS = 10, MAX_CIVILISATIONS = 20, MAX_PROGRESS_YEARS = 2000, runtime = 399 seconds


MAX_PLANETS = 10
MAX_CIVILISATIONS = 20

MAX_PROGRESS_YEARS = 2000
if MAX_PROGRESS_YEARS < 2:
    raise 'Need at least two possible progress years'

MAX_PROGRESS_YEAR_REGRESSION_STEPS = 50
if MAX_PROGRESS_YEAR_REGRESSION_STEPS < 1:
    raise 'Need at least one possible regression'
