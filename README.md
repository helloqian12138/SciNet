[![License](https://img.shields.io/badge/License-BSD%203--Clause-red.svg)](https://github.com/imperial-qore/SciNet/blob/master/LICENSE)
![Python 3.7, 3.8](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue.svg)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fimperial-qore%2FSciNet%2F&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

# SciNet

<a href="https://gitpod.io/#https://github.com/shreshthtuli/SciNet/">
    <img src="https://gitpod.io/button/open-in-gitpod.svg" alt="Open in gitpod">
  </a>

The rise of distributed cloud computing technologies has been pivotal for the large-scale adoption of Artificial Intelligence (AI) based applications for high fidelity and scalable service delivery. Systematic resource management is central in maintaining optimal Quality of Service (QoS) in cloud platforms and is divided into three fundamental types: resource provisioning, AI model deployment and workload placement. To exploit the synergy among these decision types, it becomes imperative to concurrently design (co-design) the provisioning, deployment and placement decisions for optimal QoS. As users and cloud service providers shift to non-stationary AI-based workloads, frequent decision making imposes severe time constraints on the resource management models. Existing AI-based solutions often optimize decision types independently and tend to ignore the dependencies across various system performance aspects such as energy consumption and CPU utilization, making them perform poorly in large-scale cloud systems. To address this, we propose a novel method, called SciNet, that leverages a co-simulated digital-twin of the infrastructure to capture inter-metric dependencies and accurately estimate QoS scores. To avoid expensive simulation overheads at test time, SciNet trains a neural network based imitation learner that aims to mimic an oracle, which takes optimal decisions based on co-simulated QoS estimates. Offline model training and online decision making based on the imitation learner, enables SciNet to take optimal decisions while being time-efficient. Experiments with real-life AI-based benchmark applications on a public cloud testbed show that SciNet gives up to 48\% lower execution cost, 79\% higher inference accuracy, 71\% lower energy consumption and 56\% lower response times compared to the current state-of-the-art methods. 

## Quick Start Guide

### Installation.

```console
# install prerequisites
sudo apt -y update && sudo apt install -y rsync python3-pip
pip3 install --upgrade pip
pip3 install matplotlib scikit-learn
pip3 install -r requirements.txt
export PATH=$PATH:~/.local/bin
sudo chmod 400 keys/id_rsa

# install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

Or use pre-installed gitpod.

### Quick test.

```console
# deploy a single VM and print VM IP
python3 debug/deployazure.py

# test function
http http://<public_ip>:7071/api/onnx @debug/babyyoda.jpg > output.jpg
```

### Running the SciNet model
```console
python3 main.py
```


## Cite this work
Our work is published in IEEE Transactions on Computers. Cite using the following bibtex entry.
```bibtex
@article{tuli2023scinet,
  author={Tuli, Shreshth and Casale, Giuliano and Jennings, Nicholas R.},
  journal={IEEE Transactions on Computers}, 
  title={{SciNet: Co-Design of Resource Management in Cloud Computing Environments}}, 
  year={2023}
}
```


## License

BSD-3-Clause. 
Copyright (c) 2022, Shreshth Tuli.
All rights reserved.

See License file for more details.
