import tequila as tq
#from tequila 
import numpy as np
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
    
    objective_real, objective_im = make_overlap(U0,U1)
    
    Ex = tq.simulate(objective_real)
    Ey= tq.simulate(objective_im)
    
    exp_val = Ex + 1.0j*Ey
    
    #print('Evaluated overlap between the two states: {}\n'.format(exp_val))
    
    # we want the overlap of the wavefunctions
    # # to test we can compute it manually
    wfn0 = tq.simulate(U0)
    
    wfn1 = tq.simulate(U1)
   
    test = wfn0.inner(wfn1)
    #print('Correct overlap between the two states: {}'.format(test))
    
    #print('The two result are approximately the same?',np.isclose(test, exp_val, atol=1.e-4))
    
    assert np.isclose(test, exp_val, atol=1.e-4)
    
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
    rotation_gates = ['rx', 'ry', 'rz']
    
    #np.random.seed(111)
    n_qubits = np.random.randint(1, high=5)
    
    U = {}
    for j in range(2):
        n_rotations = np.random.randint(n_qubits, high=n_qubits*3)
        gates_list = [np.random.choice(rotation_gates) for i in range(n_rotations)]
        
        angles = 2*np.pi * np.random.rand(n_rotations)
        
        circ = tq.QCircuit()
        for i, angle in enumerate(angles):
            qb = i%n_qubits+1
            
            if gates_list[i]=='rx':
                circ += tq.gates.Rx(angle=angle, target=qb)
            
            elif gates_list[i]=='ry':
                circ += tq.gates.Ry(angle=angle, target=qb)
                
            elif gates_list[i]=='rz':
                circ += tq.gates.Rz(angle=angle, target=qb)
        U[j] = circ
    
    objective_real, objective_im = make_overlap(U[0],U[1])
    
    Ex = tq.simulate(objective_real)
    Ey= tq.simulate(objective_im)
    
    exp_val = Ex + 1.0j*Ey
    
    # we want the overlap of the wavefunctions
    # # to test we can compute it manually
    wfn0 = tq.simulate(U[0])
    wfn1 = tq.simulate(U[1])
    
    test = wfn0.inner(wfn1)
    
    #print(test, '\n', exp_val)
    
    assert np.isclose(test, exp_val, atol=1.e-4)
    
    return 


def p2g(ps, first_qubit = 0):
        '''
        Functions that converts a Pauli string into the corresponding quantum 
        circuit.
        
        Parameters
        ----------
        ps : Pauli string.

        Raises
        ------
        Exception: Not a Pauli Operator.

        Returns
        -------
        U : QCircuit tequila object corresponding to the Pauli string.

        '''
        
        U = tq.QCircuit()
        for k,v in ps.items():
            if v.lower() == "x":
                U+=tq.gates.X(target=k+first_qubit)
            elif v.lower() == "y":
                U+=tq.gates.Y(target=k+first_qubit)
            elif v.lower() == "z":
                U+=tq.gates.Z(target=k+first_qubit)
            else:
                raise Exception("{}???".format(v))
        return U


def make_transition(U0=None, U1=None, H=None):# may be V instead of H
    '''
    Function that calculates the transition elements of an Hamiltonian operator
    between two different quantum states.

    Parameters
    ----------
    U0 : QCircuit tequila object, corresponding to the first state.
         
    U1 : QCircuit tequila object, corresponding to the second state.
    
    H : QubitHamiltonian tequila object
        
    Returns
    -------
    The value of the transition element as a complex number.

    '''
    
    # want to measure: <U1|H|U0> -> \sum_k c_k <U1|U_k|U0>
    
    transition_element = 0.0 + 0.0j
    
    for ps in H.paulistrings:
        #print('string',ps)
        c_k = ps.coeff
        #print('coeff', c_k)
        U_k = p2g(ps,first_qubit=1)
        objective_real, objective_im = make_overlap(U0=U0, U1=U1+U_k)
        
        tmp_r = tq.simulate(objective_real)
        tmp_im = tq.simulate(objective_im)
        
        tmp = tmp_r + 1.0j*tmp_im
        #print('contribution',c_k*tmp)
        #print()
        transition_element += c_k*tmp
        
    
    return transition_element


def test_simple_transition():
    '''
    Function that tests if make_transition function is working correctly.
    It creates a simple circuit in order to check that both real and imaginary 
    part are calculated in the right way. 

    Returns
    -------
    None.

    '''
    # two circuits to test
    U0 = tq.gates.H(target=1) + tq.gates.CNOT (1 ,2)#tq.gates.Rx(angle=1.0, target=1)#
    U1 = tq.gates.X(target=[1,2])+tq.gates.Ry(angle=2, target=1)#
    
    # defining the hamiltonian
    H = tq.QubitHamiltonian("1.0*Y(0)X(1)+0.5*Y(1)Z(0)")
    #print('Hamiltonian',H,'\n')
    
    # calculating the transition element
    trans_el = make_transition(U0=U0, U1=U1, H=H)
    
    
    #print('Evaluated transition element between the two states: {}'.format( trans_el))
    
    # # to test we can compute it manually
    #print()
    correct_trans_el = 0.0 + 0.0j
    
    wfn0 = tq.simulate(U0)
    
    for ps in H.paulistrings:
        
        c_k = ps.coeff
       
        U_k = p2g(ps,first_qubit=1)
        wfn1 = tq.simulate(U1+U_k)
        
        tmp = wfn0.inner(wfn1)
        #print('contribution',c_k*tmp)
        correct_trans_el += c_k*tmp
    
    
    #print('Correct transition element value: {}'.format(correct_trans_el))
    
    #print('The two result are approximately the same?',np.isclose(correct_trans_el, trans_el, atol=1.e-4))
    
    assert np.isclose(correct_trans_el, trans_el, atol=1.e-4)
    
    return

#-----------------------------------------------
# MAIN function
#-----------------------------------------------
if __name__ == "__main__":
  
    #test_simple_overlap()
    
    #test_simple_transition()
    
    test_random_overlap()
    #tq.draw(dic[0], backend='qiskit')
