from braket.circuits.noise_model import (
    GateCriteria,
    NoiseModel,
    ObservableCriteria,
)
from braket.circuits import Circuit, Observable, Gate
from braket.circuits.noises import (
    BitFlip,
    Depolarizing,
    TwoQubitDepolarizing,
)
from braket.devices import LocalSimulator
import numpy as np
import math


def noise_model():
    rng = np.random.default_rng()
    m = NoiseModel()

    two_q_depo_mu = 1 - 0.9311
    two_q_depo_sigma = 0.005
    bf_mu = 1 - 0.99752
    bf_sigma = 0.0015
    one_q_depo_mu = 1 - 0.9981
    one_q_depo_sigma = 0.00017
    for qi in range(11):
        z_bf_prob = bf_mu + bf_sigma * rng.standard_normal()
        z_bf_prob = 0.0 if z_bf_prob < 0.0 else z_bf_prob

        # bf_prob = bf_mu + bf_sigma * rng.standard_normal()
        # bf_prob = 0.0 if bf_prob < 0.0 else bf_prob

        one_q_depo_prob = one_q_depo_mu + one_q_depo_sigma * rng.standard_normal()
        one_q_depo_prob = 0.0 if one_q_depo_prob < 0.0 else one_q_depo_prob

        m.add_noise(BitFlip(z_bf_prob), ObservableCriteria(observables=Observable.Z, qubits=qi))
        # m.add_noise(BitFlip(bf_prob), ObservableCriteria(qubits=qi))

        m.add_noise(Depolarizing(one_q_depo_prob), GateCriteria(qubits=qi))
        for qj in range(11):
            if not qj == qi:
                two_q_depo_prob = two_q_depo_mu + two_q_depo_sigma * rng.standard_normal()
                two_q_depo_prob = 0.0 if two_q_depo_prob < 0.0 else two_q_depo_prob

                m.add_noise(TwoQubitDepolarizing(two_q_depo_prob),
                            GateCriteria(gates=[Gate.CNot, Gate.Swap, Gate.CPhaseShift], qubits=[qi, qj]))
    return m