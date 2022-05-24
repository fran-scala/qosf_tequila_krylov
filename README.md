# qosf Mentroship Program

<p>
  <a href="" target="_blank"><img src="https://github.com/fran-scala/qosf-c5-task2/blob/7be030043a89a70ba63dfeae95a818950bac6975/qosf_logo.png?raw=True" width="30%"/> </a>
</p>

## Tequila implementation of Krylov method

This repository contains all the material written and created during the QOSF mentorship program by Francesco Scala and Jakob Kottmann. The goal is the implementation of Krylov method ([arXiv:1911.05163v1](https://arxiv.org/abs/1911.05163), [published paper](https://pubs.acs.org/doi/10.1021/acs.jctc.9b01125)) inside the [tequila](https://github.com/tequilahub/tequila) package. Full contributions can be seen in the [main pull request](https://github.com/tequilahub/tequila/pull/227) I did.

### Random generatos

`random_generators.py` contains two functions:
- `make_random_circuit`: creates a circuit with random rotations or random control rotations.
- `make_random_hamiltonian`: creates a random Hamiltonian, given the list of Pauli operators to use and the number of Pauli strings.

These two functions will be useful in the testing framework.

### Braket module

The braket module inside `braket.py` contains the `braket` function that allows one to calculate the overlap between two states, the expectation value of one operator with respect to a given state or the transition element of one operator with respect to two given states. Checkout `Braket_tutorial.ipynb` to have a complete overview of the possible applications of this function as well as a detailed explenation of the underlying theoretical framework.

`test_braket.py` contains the testing of the braket function and of all its components.

The `test_functions.py` file contains some initial versions of this module.

### Krylov method
