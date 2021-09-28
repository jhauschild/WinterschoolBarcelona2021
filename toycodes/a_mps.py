"""Toy code implementing a matrix product state."""
# Copyright 2018-2021 TeNPy Developers, GNU GPLv3

import numpy as np
from scipy.linalg import svd
# if you get an error message "LinAlgError: SVD did not converge",
# uncomment the following line. (This requires TeNPy to be installed.)
#  from tenpy.linalg.svd_robust import svd  # (works like scipy.linalg.svd)

import warnings


class SimpleMPS:
    """Simple class for a matrix product state.

    We index sites with `i` from 0 to L-1; bond `i` is left of site `i`.
    We *assume* that the state is in right-canonical form.

    Parameters
    ----------
    Bs, Ss, bc:
        Same as attributes.

    Attributes
    ----------
    Bs : list of np.Array[ndim=3]
        The 'matrices', in right-canonical form, one for each physical site
        (within the unit-cell for an infinite MPS).
        Each `B[i]` has legs (virtual left, physical, virtual right), in short ``vL i vR``.
    Ss : list of np.Array[ndim=1]
        The Schmidt values at each of the bonds, ``Ss[i]`` is left of ``Bs[i]``.
    bc : 'infinite', 'finite'
        Boundary conditions.
    L : int
        Number of sites (in the unit-cell for an infinite MPS).
    nbonds : int
        Number of (non-trivial) bonds: L-1 for 'finite' boundary conditions, L for 'infinite'.
    """
    def __init__(self, Bs, Ss, bc='finite'):
        assert bc in ['finite', 'infinite']
        self.Bs = Bs
        self.Ss = Ss
        self.bc = bc
        self.L = len(Bs)
        self.nbonds = self.L - 1 if self.bc == 'finite' else self.L

    def copy(self):
        return SimpleMPS([B.copy() for B in self.Bs], [S.copy() for S in self.Ss], self.bc)

    def get_theta1(self, i):
        """Calculate effective single-site wave function on sites i in mixed canonical form.

        The returned array has legs ``vL, i, vR`` (as one of the Bs).
        """
        return np.tensordot(np.diag(self.Ss[i]), self.Bs[i], (1, 0))  # vL [vL'], [vL] i vR

    def get_theta2(self, i):
        """Calculate effective two-site wave function on sites i,j=(i+1) in mixed canonical form.

        The returned array has legs ``vL, i, j, vR``.
        """
        j = (i + 1) % self.L
        return np.tensordot(self.get_theta1(i), self.Bs[j], (2, 0))  # vL i [vR], [vL] j vR

    def get_chi(self):
        """Return bond dimensions."""
        return [self.Bs[i].shape[2] for i in range(self.nbonds)]

    def site_expectation_value(self, op):
        """Calculate expectation values of a local operator at each site."""
        result = []
        for i in range(self.L):
            theta = self.get_theta1(i)  # vL i vR
            op_theta = np.tensordot(op, theta, axes=(1, 1))  # i [i*], vL [i] vR
            result.append(np.tensordot(theta.conj(), op_theta, ([0, 1, 2], [1, 0, 2])))
            # [vL*] [i*] [vR*], [i] [vL] [vR]
        return np.real_if_close(result)

    def bond_expectation_value(self, op):
        """Calculate expectation values of a local operator at each bond."""
        result = []
        for i in range(self.nbonds):
            theta = self.get_theta2(i)  # vL i j vR
            op_theta = np.tensordot(op[i], theta, axes=([2, 3], [1, 2]))
            # i j [i*] [j*], vL [i] [j] vR
            result.append(np.tensordot(theta.conj(), op_theta, ([0, 1, 2, 3], [2, 0, 1, 3])))
            # [vL*] [i*] [j*] [vR*], [i] [j] [vL] [vR]
        return np.real_if_close(result)

    def entanglement_entropy(self):
        """Return the (von-Neumann) entanglement entropy for a bipartition at any of the bonds."""
        bonds = range(1, self.L) if self.bc == 'finite' else range(0, self.L)
        result = []
        for i in bonds:
            S = self.Ss[i].copy()
            S[S < 1.e-20] = 0.  # 0*log(0) should give 0; avoid warning or NaN.
            S2 = S * S
            assert abs(np.linalg.norm(S) - 1.) < 1.e-13
            result.append(-np.sum(S2 * np.log(S2)))
        return np.array(result)

    def correlation_length(self):
        """Diagonalize transfer matrix to obtain the correlation length."""
        import scipy.sparse.linalg.eigen.arpack as arp
        if self.get_chi()[0] > 100:
            warnings.warn("Skip calculating correlation_length() for large chi: could take long")
            return -1.
        assert self.bc == 'infinite'  # works only in the infinite case
        B = self.Bs[0]  # vL i vR
        chi = B.shape[0]
        T = np.tensordot(B, np.conj(B), axes=(1, 1))  # vL [i] vR, vL* [i*] vR*
        T = np.transpose(T, [0, 2, 1, 3])  # vL vL* vR vR*
        for i in range(1, self.L):
            B = self.Bs[i]
            T = np.tensordot(T, B, axes=(2, 0))  # vL vL* [vR] vR*, [vL] i vR
            T = np.tensordot(T, np.conj(B), axes=([2, 3], [0, 1]))
            # vL vL* [vR*] [i] vR, [vL*] [i*] vR*
        T = np.reshape(T, (chi**2, chi**2))
        # Obtain the 2nd largest eigenvalue
        eta = arp.eigs(T, k=2, which='LM', return_eigenvectors=False, ncv=20)
        xi =  -self.L / np.log(np.min(np.abs(eta)))
        if xi > 1000.:
            return np.inf
        return xi

    def correlation_function(self, op_i, i, op_j, j):
        """Correlation function between two distant operators on sites i < j.

        Note: calling this function in a loop over `j` is inefficient for large j >> i.
        The optimization is left as an exercise to the user.
        Hint: Re-use the partial contractions up to but excluding site `j`.
        """
        assert i < j
        theta = self.get_theta1(i) # vL i vR
        C = np.tensordot(op_i, theta, axes=(1, 1)) # i [i*], vL [i] vR
        C = np.tensordot(theta.conj(), C, axes=([0, 1], [1, 0]))  # [vL*] [i*] vR*, [i] [vL] vR
        for k in range(i + 1, j):
            k = k % self.L
            B = self.Bs[k]  # vL k vR
            C = np.tensordot(C, B, axes=(1, 0)) # vR* [vR], [vL] k vR
            C = np.tensordot(B.conj(), C, axes=([0, 1], [0, 1])) # [vL*] [k*] vR*, [vR*] [k] vR
        j = j % self.L
        B = self.Bs[j]  # vL k vR
        C = np.tensordot(C, B, axes=(1, 0)) # vR* [vR], [vL] j vR
        C = np.tensordot(op_j, C, axes=(1, 1))  # j [j*], vR* [j] vR
        C = np.tensordot(B.conj(), C, axes=([0, 1, 2], [1, 0, 2])) # [vL*] [j*] [vR*], [j] [vR*] [vR]
        return C


def init_FM_MPS(L, d, bc='finite'):
    """Return a ferromagnetic MPS (= product state with all spins up)"""
    B = np.zeros([1, d, 1], dtype=float)
    B[0, 0, 0] = 1.
    S = np.ones([1], dtype=float)
    Bs = [B.copy() for i in range(L)]
    Ss = [S.copy() for i in range(L)]
    return SimpleMPS(Bs, Ss, bc=bc)


def init_Neel_MPS(L, d, bc='finite'):
    """Return a ferromagnetic MPS (= product state with all spins up)"""
    S = np.ones([1], dtype=float)
    Bs = []
    for i in range(L):
        B = np.zeros([1, d, 1], dtype=float)
        if i % 2 == 0:
            B[0, 0, 0] = 1.
        else:
            B[0, -1, 0] = 1.
        Bs.append(B)
    Ss = [S.copy() for i in range(L)]
    return SimpleMPS(Bs, Ss, bc=bc)


def split_truncate_theta(theta, chi_max, eps):
    """Split and truncate a two-site wave function in mixed canonical form.

    Split a two-site wave function as follows::
          vL --(theta)-- vR     =>    vL --(A)--diag(S)--(B)-- vR
                |   |                       |             |
                i   j                       i             j

    Afterwards, truncate in the new leg (labeled ``vC``).

    Parameters
    ----------
    theta : np.Array[ndim=4]
        Two-site wave function in mixed canonical form, with legs ``vL, i, j, vR``.
    chi_max : int
        Maximum number of singular values to keep
    eps : float
        Discard any singular values smaller than that.

    Returns
    -------
    A : np.Array[ndim=3]
        Left-canonical matrix on site i, with legs ``vL, i, vC``
    S : np.Array[ndim=1]
        Singular/Schmidt values.
    B : np.Array[ndim=3]
        Right-canonical matrix on site j, with legs ``vC, j, vR``
    """
    chivL, dL, dR, chivR = theta.shape
    theta = np.reshape(theta, [chivL * dL, dR * chivR])
    X, Y, Z = svd(theta, full_matrices=False)
    # truncate
    chivC = min(chi_max, np.sum(Y > eps))
    assert chivC >= 1
    piv = np.argsort(Y)[::-1][:chivC]  # keep the largest `chivC` singular values
    X, Y, Z = X[:, piv], Y[piv], Z[piv, :]
    # renormalize
    S = Y / np.linalg.norm(Y)  # == Y/sqrt(sum(Y**2))
    # split legs of X and Z
    A = np.reshape(X, [chivL, dL, chivC])
    B = np.reshape(Z, [chivC, dR, chivR])
    return A, S, B
