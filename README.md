# 2024_AWS
AWS iQuHACK 2024 In-Person Challenge

For this year's Amazon Braket challenge, we invite you to implement a noise-aware compilation scheme using the Braket SDK which improves the performance of Braket devices. Basically, you're remapping input quantum circuits to make the best use of available qubits, based on which are noisiest. 

## WARNING: IonQ Harmony is currently experiencing an issue and not processing tasks quickly enough for hackers to run their tasks!

As a fallback, we've developed a *facsimile* noise model of a "similar" device. Included below is a *sample script* to apply this noise model to a circuit. This runs on `braket_dm` (a local simulator) in a qBraid notebook (we show how to do this below).
Previously, by running tasks on IonQ Harmony, you would have been able to infer such a noise model. Now, you can use ours (which drifts at each run) to try to develop your compiler approach.

```python
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
        
        bf_prob = bf_mu + bf_sigma * rng.standard_normal()
        bf_prob = 0.0 if bf_prob < 0.0 else bf_prob
        
        one_q_depo_prob = one_q_depo_mu + one_q_depo_sigma * rng.standard_normal()
        one_q_depo_prob = 0.0 if one_q_depo_prob < 0.0 else one_q_depo_prob
        
        m.add_noise(BitFlip(z_bf_prob), ObservableCriteria(observables=Observable.Z, qubits=qi))
        #m.add_noise(BitFlip(bf_prob), ObservableCriteria(qubits=qi))
        
        m.add_noise(Depolarizing(one_q_depo_prob), GateCriteria(qubits=qi))
        for qj in range(11):
            if not qj == qi:
                two_q_depo_prob = two_q_depo_mu + two_q_depo_sigma * rng.standard_normal()
                two_q_depo_prob = 0.0 if two_q_depo_prob < 0.0 else two_q_depo_prob
                
                m.add_noise(TwoQubitDepolarizing(two_q_depo_prob), GateCriteria(gates=[Gate.CNot, Gate.Swap, Gate.CPhaseShift], qubits=[qi, qj]))
    return m

# build my circuit here
c = Circuit()
# SOME GATES GET APPLIED

# examine the noiseless circuit 
print(c)

# apply the noise model to the circuit 
nm = noise_model()
c = nm.apply(c)

# examine the noisy circuit 
print(c)

# run the simulation!
device = LocalSimulator('braket_dm')
result = device.run(c, shots=1000).result()

# now improve the mapping based on the results!
```

## A (relatively) simple example

So for an example, let's say I wanted to generate Bell state, which I define as follows: 
```
from braket.circuits import Circuit
bell = Circuit().h(0).cnot(0, 1)
``` 
![Local Image](standard-Bell.png)

I want to run this circuit on the IonQ Harmony device and make sure I’m using the best qubits for the job. Therefore, I’ll query the two qubit gate fidelities (T2) like this: 
```
from braket.aws import AwsDevice

harmony = AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Harmony")
l_fid = harmony.properties.provider.properties
l_t2 = l_fid['2Q']
print(l_t2)
```
which gives
```
{'mean': 0.9552}
```
In this case, the mean two qubit gate fidelity is 95.5. Since IonQ doesn't break out the individual 2-qubit fidelities, we can try to infer them by running Bell-pair preparations on each pair (can you think of a way to do this in fewer than `N` tasks, where `N` is the number of pairs?). From this information, my noise-aware compiler would implement logic to remap my input circuit to run on those qubits with the best fidelity.

**Hint**: make sure your output circuit uses [verbatim compilation](https://github.com/amazon-braket/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb) so your circuit doesn’t get recompiled again!

## General approach and getting started

For a standard approach to noise-aware compiling in gate-based Noisy Intermediate Scale Quantum (NISQ) devices, you can check out this paper by Murali et al.: https://arxiv.org/abs/1901.11054. For a reference implementation in Qiskit, check out the `NoiseAdaptiveLayout` [method](https://docs.quantum.ibm.com/api/qiskit/qiskit.transpiler.passes.NoiseAdaptiveLayout).

**Hint**: you can access mean 1 and 2-qubit fidelities for the IonQ Harmony device as follows:
```
from braket.aws import AwsDevice

harmony = AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Harmony")
h_fidelities = harmony.properties.provider.fidelity
```
You are also welcome to run a noisy simulation using the local density matrix simulator or the DM1 on-demand simulator (check out this [comprehensive example](https://github.com/amazon-braket/amazon-braket-examples/blob/main/examples/braket_features/Simulating_Noise_On_Amazon_Braket.ipynb) to see how) and apply noise-aware compiling to the simulated circuit. We would recommend referring to the Adding noise to a circuit section of the above example, so that you can properly assign noise rates to different simulated qubits, and therefore get an advantage using noise-aware compiling.

The overall goal of the challenge is to implement a noise-aware scheme which improves the performance for a quantum algorithm of your choice over the default compiler (i.e. if you didn’t include your compiler pass) on your chosen Braket device(s). 


## Working on qBraid
[<img src="https://qbraid-static.s3.amazonaws.com/logos/Launch_on_qBraid_white.png" width="150">](https://account.qbraid.com?gitHubUrl=https://github.com/iQuHACK/2024_AWS.git)

To access the devices such as IonQ's Harmony for the challenge, we will be providing access and credits via qBraid. So, here are some guidelines:
1. To launch these materials on qBraid, first fork this repository and click the above `Launch on qBraid` button. It will take you to your qBraid Lab with the repository cloned.
2. Once cloned, open terminal (first icon in the **Other** column in Launcher) and `cd` into this repo. Set the repo's remote origin using the git clone url you copied in Step 1, and then create a new branch for your team:
```bash
cd  2024_AWS
git remote set-url origin <url>
git branch <team_name>
git checkout <team_name>
```
3. Use the default environment which has the latest version of `amazon_braket_sdk`. 
4. From the **FILES** tab in the left sidebar, double-click on the `2024_AWS` directory, if you are not there already.
6. You are now ready to begin hacking and [submitting jobs](https://docs.qbraid.com/projects/lab/en/latest/lab/quantum_jobs.html)! Work with your team to complete either of the challenges listed above.

For other questions or additional help using qBraid, see [Lab User Guide](https://docs.qbraid.com/en/latest/), or reach out on the qBraid Slack channel.

# Submission Instructions
To submit your solution, *make sure your fork of this repo is public* and upload a PDF or slideshow explaining your project solution (include a brief intro to the problem, your approach, an outline of your implementation, and your results). All in-person participants will have the opportunity to give a 5-10 minute presentation on their challenge solution in the project presentations (10:30-12:30) on Sunday February 4. 
