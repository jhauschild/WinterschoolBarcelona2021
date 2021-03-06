# Tutorials for DMRG and TDVP

This is a set of tutorials for the [winter school of the European Tensor Network held in September 2021 in Barcelona](https://indico.icc.ub.edu/event/116/overview).

The tutorials are split into two sessions.

In the first session, we will use very small "toy codes" that require only [Python](https://python.org) with [numpy](https://numpy.org) + [scipy](https://scipy.org) and should give you a good idea how the algorithms work.
All files for this are in the folder `toycodes`, and you need to look into them during the tutorials to see how they work. (It should not be necessary to modify them.)

In the second session, we will use the [TeNPy](https://github.com/tenpy/tenpy) library to setup more advanced calculations in the folder `tenpy`.

## Lecture notes

The `IntroDMRG.pdf` and `IntroTDVP.pdf` are the notes written down in the lecture itself.
I've also added the prepared lecture notes with a slightly cleaner hand writing (and an extra page in the end of DMRG, that I skipped during the lecture due to time constraints).

The references are:

- (White, PRL 69, 2863 (1992))[https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.69.2863], the original!
- (JH, Pollmann arXiv:1805.0055)[https://arxiv.org/abs/1805.0055], followed in the DMRG lecture
- (Schollwoeck arXiv:1008.3477)[https://arxiv.org/abs/1008.3477], a classic review
- (Haegeman et al arXiv:1103.0936)[https://arxiv.org/abs/1103.0936], the original application of TDVP to MPS
- (Haegeman et al arXiv:1408.5056)[https://arxiv.org/abs/1408.5056], discussed in the TDVP lecture
- (Vanderstraeten et al arXiv:1810.07006)[https://arxiv.org/abs/1810.07006], a good review of the tangent space for infinite MPS
- (Paeckel et al arXiv:1901.05824)[https://arxiv.org/abs/1901.05824], a nice review comparing various MPS time evolution methods


## Setup

**Running locally**: If you have a working Python installation, feel free to solve all the exercises locally on your own computer.
For the second part, you need to [install TeNPy](https://tenpy.readthedocs.io/en/latest/INSTALL.html), which is often just a `conda install physics-tenpy` or `pip install physics-tenpy`, depending on your setup.

**Jupyter notebooks**: We recommend solving the exercises interactively with [jupyter notebooks](https//jupyter.org). You can get it with ``conda install jupyterlab`` and then run``jupyter-lab``, which opens an interactive coding session in your web browser.

**Running notebooks on Google colab**: You can also use [Google's colab cloud service](https://colab.research.google.com) to run the jupyter notebooks **without any local installation**. Use this option if you have any trouble with your local installation.
In this case, you need to ``pip install git+git://github.com/jhauschild/WinterschoolBarcelona2021`` to allow the notebooks to find the toy codes.
(It's already as a comment at the top of the notebooks.)

## License

All codes are released under GPL (v3) given in the file `LICENSE`, which means you can freely copy, share and distribute the code.
They toycodes in the folder `toycodes` are based on the toycodes distributed with TeNPy (also under the GPL).
