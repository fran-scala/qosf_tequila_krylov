import tequila as tq
import copy

def make_overlap(U0 = None, U1 = None):
    '''
    Function that calculates the overlap between two quantum states.

    Parameters
    ----------
    U0 : QCircuit tequila object, corresponding to the first state.
         
    U1 : QCircuit tequila object, corresponding to the second state.

    Returns
    -------
    Tequila objective to be simulated or compiled.

    '''
    
    U_a = copy.deepcopy(U0)
    U_b = copy.deepcopy(U1)
    
    U_a.add_controls([0]) #this add the control by modifying the previous circuit
    U_b.add_controls([0]) #NonType object
    
    #bulding the circuit for the overlap evaluation
    circuit = tq.gates.H(target=0)
    circuit += U_a
    circuit += tq.gates.X(target=0)
    circuit += U_b
    
    x = tq.paulis.X(0)
    y = tq.paulis.Y(0)
    Ex = tq.ExpectationValue(H=x, U=circuit)
    Ey = tq.ExpectationValue(H=y, U=circuit)
    
    
    return Ex, Ey


def make_transition(U0=None, U1=None, H=None):# may be V instead of H
    '''
    Function that calculates the transition elements of an Hamiltonian operator
    between two different quantum states.

    Parameters
    ----------
    U0 : QCircuit tequila object, corresponding to the first state.
         
    U1 : QCircuit tequila object, corresponding to the second state.
    
    H : TYPE, optional
        DESCRIPTION. 
        ?????
        tq.gates.Trotterized(generator=tq.paulis.Y(0), angle=1)
        this for gives me the trotterization or is one ofthe m operators I have to compose?

    Returns
    -------
    Tequila objective to be simulated or compiled.

    '''
    
    U0.add_controls([0]) #this add the control by modifying the previous circuit
    U1.add_controls([0]) #NonType object
    H.add_controls([0])
    
    #bulding the circuit for the overlap evaluation
    circuit = tq.gates.H(target=0)
    circuit += U0
    circuit += tq.gates.X(target=0)
    circuit += U1
    circuit += H
    
    
    x = tq.paulis.X(0)
    y = tq.paulis.Y(0)
    Ex = tq.ExpectationValue(H=x, U=circuit)
    Ey = tq.ExpectationValue(H=y, U=circuit)
    
    exp_val = Ex + 1.0j*Ey
    return exp_val 


def test_simple_overlap():
    '''
    Function that tests if make_overlap function is working correctly.
    It creates a simple circuit in order to check that both real and imaginary 
    part are calculated in the right way. 

    Returns
    -------
    None.

    '''
        # two circuits to test
    U0 = tq.gates.Rz(angle=1.0, target=1)#tq.gates.H(target=1) + tq.gates.CNOT (1 ,2)
    U1 = tq.gates.Rz(angle=2, target=1)#tq.gates.X(target=[1,2])#
    
    print(U0)
    print(U1)
    print()
    # we want the overlap of the wavefunctions
    
    # goal would be a function like this
    objective_real, objective_im = make_overlap(U0,U1)
    
    Ex = tq.simulate(objective_real)
    Ey= tq.simulate(objective_im)
    
    exp_val = Ex + 1.0j*Ey
    
    print('Evaluated overlap between the two states: {}'.format(exp_val))
    
    # # to test we can compute it manually
    wfn0 = tq.simulate(U0)
    print(wfn0)
    wfn1 = tq.simulate(U1)
    print(wfn1)    
    test = wfn0.inner(wfn1)#it seems to be wrong
    print(test)
    
    # # assert numpy.isclose(test, evaluated)
    
    return

def test_random_overlap():
    '''
    Function that tests if make_overlap function is working correctly.
    It creates circuits with random number of qubits, random rotations and 
    random angles.

    Returns
    -------
    None.

    '''
    
    
    return


#-----------------------------------------------
# MAIN function
#-----------------------------------------------
if __name__ == "__main__":

    
    test_simple_overlap()

    # # same thing with operators
    # # to test <psi0|H|psi1>
    # # with function that we want:
    # # sandwhich = make_transition(U0,U1,H)
    
    # # test with:
    # H = tq.paulis.X(0)
    # tmp = H(wfn1)
    # test_sandwhich = wfn0.inner(tmp)
    
    # # potentially useful
    
    # cu0 = U0.add_controls([1]) 
