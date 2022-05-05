# qosf Mentroship Program
## Tequila implementation of Krylov methods
This repository contains all the material written and created during the QOSF mentorship program by Francesco Scala and Jakob Kottmann. The goal is the implementation of Krylov methods inside the tequila package. Full contributions can be seen in the frorked repository of tequila.

### Random generatos
`random_generators.py` contains two functions:
- `make_random_circuit`: creates a circuit with random rotations or random control rotations.
- `make_random_hamiltonian`: creates a random Hamiltonian, given the list of Pauli operators to use and the number of Pauli strings.

These two functions will be useful in the testing framework.

### Braket module
The braket module inside `braket.py` contains the `braket` function that allows one to calculate the overlap between two states, the expectation value of one operator with respect to a given state or the transition element of one operator with respect to two given states.

`test_braket.py` contains the testing of the braket function and of all its components.

The `test_functions.py` file contains some initial versions of this module.
