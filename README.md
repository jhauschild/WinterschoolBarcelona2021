# Tutorials for DMRG and TDVP

This is a set of tutorials for the winter school of the European Tensor Network held Sept. 28, 2021 in Barcelona.

The tutorials are split into two sessions.

In the first session, we will use very small "toy codes" that require only [Python](https://python.org) with [numpy](https://numpy.org) + [scipy](https://scipy.org) and should give you a good idea how the algorithms work.
All files for this are in the folder `1_toycodes`

In the second session, we will use the [TeNPy](https://github.com/tenpy/tenpy) library to setup more advanced calculations in the folder `2_tenpy`.

## Setup

**Running locally**: If you have a working Python installation, feel free to solve all the exercises locally on your own computer.
For the second part, you need to install TeNPy, which is often just a `conda install physics-tenpy` or `pip install physics-tenpy`, depending on your setup.

**Jupyter notebooks**: We recommend solving the exercises interactively with [jupyter notebooks](https//jupyter.org). You can get it with ``conda install jupyterlab`` and then run``jupyter-lab``, which opens a coding session in your web browser.

**Running notebooks on Google colab**: You can also use [Google's colab cloud service](https://colab.research.google.com) to run the jupyter notebooks **without any local installation**. Use this option if you have any trouble with your local installation.

## License

All codes are released under GPL (v3) given in the file `LICENSE`, which means you can freely copy, share and distribute the code, provided you keep the copyright notice.
They toycodes in the folder `1_toycodes` are based on the toycodes distributed with TeNPy (also under the GPL).
