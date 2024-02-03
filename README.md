# 2024_AWS
AWS iQuHACK 2024 In-Person Challenge

For this year's Amazon Braket challenge, we invite you to implement a noise-aware compilation scheme using the Braket SDK which improves the performance of Braket devices. Basically, you're remapping input quantum circuits to make the best use of available qubits, based on which are noisiest. 

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
l_t2 = l_fid['two_qubit']
print(l_t2)
```
which gives
```
 'two_qubit': {'0-1': {'coupling': {'control_qubit': 0.0, 'target_qubit': 1.0},
   'fCX': 0.9107046823673131},
  '0-7': {'coupling': {'control_qubit': 0.0, 'target_qubit': 7.0},
   'fCX': 0.9926670620929618},
  '1-2': {'coupling': {'control_qubit': 1.0, 'target_qubit': 2.0},
   'fCX': 0.9336247576925645},
  '2-3': {'coupling': {'control_qubit': 2.0, 'target_qubit': 3.0},
   'fCX': 0.9305393721231507},
  '4-3': {'coupling': {'control_qubit': 4.0, 'target_qubit': 3.0},
   'fCX': 0.9631366580296402},
  '4-5': {'coupling': {'control_qubit': 4.0, 'target_qubit': 5.0},
   'fCX': 0.9699989023360711},
  '6-5': {'coupling': {'control_qubit': 6.0, 'target_qubit': 5.0},
   'fCX': 0.9632392875032397},
  '7-6': {'coupling': {'control_qubit': 7.0, 'target_qubit': 6.0},
   'fCX': 0.7673442630631202}}}
```
In this case, the two qubit gate fidelity is highest on the qubit pair ‘0-7’ , where 0 is the target and 7 is the control. So my noise-aware compiler would implement logic to remap my input circuit to run on those qubits. Doing this manually, we would have the following output circuit: <br>
![Local Image](verbatim-remapped-bell.png)

**Hint**: make sure your output circuit uses [verbatim compilation](https://github.com/amazon-braket/amazon-braket-examples/blob/main/examples/braket_features/Verbatim_Compilation.ipynb) so your circuit doesn’t get recompiled again!

## General approach and getting started

For a standard approach to noise-aware compiling in gate-based Noisy Intermediate Scale Quantum (NISQ) devices, you can check out this paper by Murali et al.: https://arxiv.org/abs/1901.11054. For a reference implementation in Qiskit, check out the `NoiseAdaptiveLayout` [method](https://docs.quantum.ibm.com/api/qiskit/qiskit.transpiler.passes.NoiseAdaptiveLayout).

**Hint**: you can access individual 1 and 2-qubit fidelities for the IonQ Harmony device as follows:
```
from braket.aws import AwsDevice

harmony = AwsDevice("arn:aws:braket:us-east-1::device/qpu/ionq/Harmony")
h_fidelities = harmony.properties.provider.fidelity
```
You are also welcome to run a noisy simulation using the DM1 on-demand simulator (check out this [comprehensive example](https://github.com/amazon-braket/amazon-braket-examples/blob/main/examples/braket_features/Simulating_Noise_On_Amazon_Braket.ipynb) to see how) and apply noise-aware compiling to the simulated circuit. We would recommend referring to the Adding noise to a circuit section of the above example, so that you can properly assign noise rates to different simulated qubits, and therefore get an advantage using noise-aware compiling.

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
