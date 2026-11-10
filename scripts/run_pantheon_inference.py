"""Starter script for PHYS690 Project 2.

Complete the TODOs so this file independently reproduces the analysis in the
notebook. Run it from the repository root. Do not depend on notebook state.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.request import urlretrieve

import matplotlib.pyplot as plt
import emcee
import numpy as np
import pandas as pd
from scipy.constants import c
from scipy.linalg import cholesky, solve_triangular
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
FIGURE_DIR = ROOT / "figures"
OUTPUT_DIR = ROOT / "outputs"
DATA_URL = "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES.dat"
COV_URL = "https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/Pantheon%2BSH0ES_STAT%2BSYS.cov"
H0 = 70.0  # km s^-1 Mpc^-1; its degeneracy with M_B is absorbed by M_B.
C_KM_S = c / 1000.0
PARAMETER_NAMES = ["Omega_m", "w0", "wa", "M_B"]
BOUNDS = np.array([[0.05, 0.60], [-2.5, -0.3], [-5.0, 5.0], [-20.0, -18.0]])


def load_data():
    """Download the public files and return selected data and covariance."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data_path = DATA_DIR / "Pantheon+SH0ES.dat"
    cov_path = DATA_DIR / "Pantheon+SH0ES_STAT+SYS.cov"
    if not data_path.exists():
        urlretrieve(DATA_URL, data_path)
    if not cov_path.exists():
        urlretrieve(COV_URL, cov_path)
    table = pd.read_csv(data_path, sep=r"\s+")
    raw = np.fromstring(cov_path.read_text(), sep=" ")
    n_cov = int(raw[0])
    covariance = raw[1:].reshape(n_cov, n_cov)
    if n_cov != len(table):
        raise ValueError(f"Covariance dimension {n_cov} != table rows {len(table)}")
    # TODO: Select IS_CALIBRATOR == 0 and zHD > 0.01; apply the same row index
    # to the table and both covariance dimensions. Explain this supernova-only
    # selection in the notebook and final report.
    raise NotImplementedError("Apply the documented row selection")


def e_of_z(z, omega_m, w0, wa):
    """Dimensionless expansion rate for flat w0waCDM."""
    # TODO: Implement the equation in the notebook. Return sqrt(E_squared).
    raise NotImplementedError


def apparent_magnitude_model(z, parameters, n_quad=32):
    """Return m_b,corr prediction for [Omega_m, w0, wa, M_B]."""
    # TODO: Use Gauss-Legendre quadrature for the comoving-distance integral,
    # then compute distance modulus + M_B. H0 is held fixed at module scope.
    raise NotImplementedError


def whitened_residual(parameters, z, magnitude, covariance_cholesky):
    # TODO: residual = observed - model; solve L y = residual.
    raise NotImplementedError


def chi_square(parameters, z, magnitude, covariance_cholesky):
    # TODO: Return y @ y for the whitened residual vector.
    raise NotImplementedError


def log_prior(parameters):
    # TODO: Uniform prior inside BOUNDS, zero probability outside.
    raise NotImplementedError


def log_posterior(parameters, z, magnitude, covariance_cholesky):
    # TODO: Return log_prior - chi_square/2, or -inf outside the prior.
    raise NotImplementedError


def run_emcee_ensemble(log_target, initial_positions, z, magnitude,
                       covariance_cholesky, n_burnin, n_production, seed):
    """Run burn-in, reset stored burn-in draws, then run production with emcee."""
    # TODO: Follow Lecture 18:
    # 1. Set the reproducible emcee random seed.
    # 2. Construct emcee.EnsembleSampler(n_walkers, n_parameters, log_target,
    #    args=(z, magnitude, covariance_cholesky)).
    # 3. Run burn-in from initial_positions and keep the returned State.
    # 4. Call sampler.reset() to clear stored burn-in draws, not the State.
    # 5. Run production from that State and return the sampler.
    raise NotImplementedError


def run(args):
    # TODO: Complete the full pipeline:
    # 1. Load selected data and Cholesky-factor the full covariance submatrix.
    # 2. Fit LambdaCDM [Omega_m, M_B] and w0waCDM [Omega_m,w0,wa,M_B]
    #    with bounded scipy.optimize.least_squares on whitened residuals.
    # 3. Run four independent emcee ensembles, each with >= 48 walkers for
    #    this four-dimensional problem. Use burn-in then reset before production.
    # 4. Inspect acceptance fractions and traces. Use sampler.get_autocorr_time()
    #    for integrated autocorrelation time; estimate ESS and split-Rhat across
    #    independent ensemble runs, not by treating coupled walkers as chains.
    # 5. Compare the broad wa prior with a narrower -2 < wa < 2 prior by
    #    rejection-filtering broad-prior draws if those chains sample that range.
    # 6. Save Hubble, covariance, MCMC diagnostic, posterior, and predictive
    #    plots; save posterior draws plus summary, diagnostic, and sensitivity CSVs.
    raise NotImplementedError("Complete the reproducible analysis workflow")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", type=int, default=2000,
                        help="production steps per walker, per ensemble")
    parser.add_argument("--warmup", type=int, default=500,
                        help="burn-in steps per walker, per ensemble")
    parser.add_argument("--seed", type=int, default=2202)
    run(parser.parse_args())
