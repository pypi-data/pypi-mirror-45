# viznet - a network visualization toolbox
![](docs/images/viznetlogo.jpg)
viznet is designed for visualizing networks composed of nodes and edges, e.g. tensor networks, neural networks and quantum circuits. 

It is based on and compatible with matplotlib. The theme brush (for both node and edge) makes the design itself interesting, getting you free from fine tuning the node and wire parameters for hours.

## To Install
```bash
    $ pip install viznet
```

or for the latest version
```bash
    $ git clone https://github.com/GiggleLiu/viznet.git
    $ cd viznet
    $ pip install -r requirements.txt
    $ python setup.py install
```

## To Run Examples
```bash
    $ cd viznet
    $ python apps/nn/bm.py      # example on neural network
    $ python apps/tn/tebd.py    # example on tensor network
    $ python apps/qc/ghz.py     # example on quantum circuit
```
you will get something like

Boltzmann Machine       | TEBD                      
----------------------- | -------------------------
![](docs/images/bm.png) | ![](docs/images/tebd.png)

 Quantum Circuit           |  Graph Theory
 --------------------------| -------------------------------
 ![](docs/images/ghz4.png) | ![](docs/images/contract.gif)

The theme for neural network follows from [Neural Network Zoo Page](http://www.asimovinstitute.org/neural-network-zoo/),

The theme for quantum circuits follows from [ProjectQ](https://github.com/ProjectQ-Framework/ProjectQ.git).

## Author

The first release of viznet (v0.1) was developed by [Jin-Guo Liu](https://giggleliu.github.io/)  in the group of Lei Wang at IOP China.

## Documentation
* Go through notebook `docs/viznet_basic.ipynb` ([online](https://drive.google.com/file/d/1mP9DOoTR4JEhd-ILVXfggpBJOyGatiws/view?usp=sharing)) as a quick introduction
* Click [here](http://viznet.readthedocs.io/en/latest/) to read the docs!


