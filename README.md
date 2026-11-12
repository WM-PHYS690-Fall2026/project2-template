# Project 2: Bayesian Constraints on Dark Energy with Pantheon+

Starter repository for PHYS690 Project 2. Use Type Ia supernova distances to compare a flat $\Lambda\mathrm{CDM}$ expansion history with a flat time-varying dark-energy model, then use Bayesian inference to quantify the joint and marginalized uncertainty in the cosmological parameters.

This project continues the supernova Hubble-diagram work from Assignment 2. The new analysis uses the public Pantheon+ distance data and its full statistical-plus-systematic covariance matrix. A central goal is to understand why a nonlinear multi-parameter model can have correlated, non-Gaussian parameter constraints, and what MCMC adds beyond a best fit and local covariance matrix.

## Repository layout

```text
.
├── README.md
├── requirements.txt
├── data/raw/                 # downloaded public data; do not commit
├── figures/                  # final student figures
├── notebooks/
│   └── project2_pantheon_bayesian_cosmology.ipynb
├── outputs/                  # chain and result files
├── scripts/
│   └── run_pantheon_inference.py
└── _instructor_only/         # solution notebook, script, figures, outputs
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows Git Bash use `source .venv/Scripts/activate`. Select the `.venv` kernel in VS Code.

## Scientific question

Do the Pantheon+ Type Ia supernova distances constrain a constant dark-energy equation of state as well as a time-varying one? Compare a flat $\Lambda\mathrm{CDM}$ model ($w=-1$) and a flat $w_0w_a\mathrm{CDM}$ model,

$$w(a)=w_0+w_a(1-a),$$

where $a=(1+z)^{-1}$. Infer the matter density $\Omega_m$, dark-energy parameters $w_0$ and $w_a$, and a magnitude intercept $M_B$ from the standardized apparent magnitudes. Hold $H_0$ fixed because supernova apparent magnitudes alone do not independently determine both $H_0$ and the absolute-magnitude calibration; the fitted intercept absorbs that degeneracy.

Pantheon+ provides 1701 supernova and Cepheid-host distance entries. The official release warns that the diagonal uncertainties are for plotting only: cosmological fits must use the full covariance matrix. For this project, use the published covariance submatrix corresponding to the selected rows, not just the quoted point-by-point errors. Exclude Cepheid calibrator rows and the very-low-redshift sample from the supernova-only fit, then state the exact selection used.

## Bayesian roadmap

For parameters $\boldsymbol{\theta}$ and observed data $D_{\mathrm{obs}}$,

$$p(\boldsymbol{\theta}\mid D_{\mathrm{obs}})=\frac{p(D_{\mathrm{obs}}\mid\boldsymbol{\theta})p(\boldsymbol{\theta})}{p(D_{\mathrm{obs}})}.$$

The likelihood is a function of model parameters for the fixed observed data. The prior expresses parameter ranges or information adopted before this dataset. The evidence in the denominator normalizes the posterior and is constant as the parameters vary within one model, so MCMC can target

$$\log p(\boldsymbol{\theta}\mid D_{\mathrm{obs}})=\log p(D_{\mathrm{obs}}\mid\boldsymbol{\theta})+\log p(\boldsymbol{\theta})+\mathrm{constant}.$$

For a Gaussian distance-modulus likelihood with residual vector $\mathbf r=\mathbf m_{\rm obs}-\mathbf m_{\rm model}$ and covariance $C$,

$$-2\log L=\mathbf r^{\mathsf T}C^{-1}\mathbf r+\log|C|+N\log(2\pi).$$

Here $C$ is fixed, so the determinant and normalization terms do not change the parameter location; retain the quadratic form and use a numerically stable Cholesky factorization rather than explicitly inverting $C$. The production sampler is `emcee` 3.1.6, the ensemble sampler used in Lecture 18. `emcee` explores the same posterior defined by the likelihood and prior; it does not change the target distribution.

## Data and provenance

The script downloads the official Pantheon+ distance vector and full covariance matrix from the [PantheonPlusSH0ES DataRelease repository](https://github.com/PantheonPlusSH0ES/DataRelease). The relevant files are `Pantheon+SH0ES.dat` and `Pantheon+SH0ES_STAT+SYS.cov` in `Pantheon+_Data/4_DISTANCES_AND_COVAR/`. The source repository documents the covariance file layout and distance-vector columns.

The principal reference is Brout et al., [“The Pantheon+ Analysis: Cosmological Constraints”](https://arxiv.org/abs/2202.04077). Pantheon+ contains 1701 light curves of 1550 Type Ia supernovae; repeated observations and Cepheid-host information mean the delivered distance vector is not simply a list of independent point errors.

Data are downloaded automatically to `data/raw/` when absent. Do not commit downloaded files, chain files, or generated figures unless your instructor requests them. Record the data source and any filtering in your final report.

## Required analysis

- Inspect columns, redshift coverage, magnitude range, missing values, and covariance matrix; explain why diagonal error bars alone are not the fitting uncertainty.
- Plot the Hubble diagram and a useful view of the covariance (for example, its correlation matrix).
- Implement the luminosity-distance prediction for flat $w_0w_a\mathrm{CDM}$ and document numerical integration choices.
- Fit a baseline flat $\Lambda\mathrm{CDM}$ model and a flat $w_0w_a\mathrm{CDM}$ model. State parameter bounds and priors before interpreting posterior results.
- Construct a Gaussian likelihood using the full covariance and compare the maximum-likelihood or maximum-a-posteriori point with the posterior distribution.
- Use `emcee.EnsembleSampler` with at least 48 walkers for the four-parameter posterior. Run burn-in, reset the stored burn-in samples while retaining the final walker state, then run production steps as in Lecture 18.
- Run at least four independently seeded ensembles. Inspect walker traces, per-walker acceptance fractions, integrated autocorrelation time, effective sample size, and split $\widehat R$ across independent ensembles before reporting intervals. Walkers within one ensemble interact and should not be presented as independent chains.
- Display joint posterior contours and marginalized distributions. Report central 68% and 95% posterior intervals for $\Omega_m$, $w_0$, and $w_a$; explain asymmetry or strong correlation.
- Assess prior sensitivity in the weakly constrained $w_a$ direction by comparing the broad uniform prior with a narrower uniform range. State how many broad-prior draws lie in the narrower range and interpret the conditional posterior carefully.
- Compare the time-varying model constraints with the nested $\Lambda\mathrm{CDM}$ result. Explain what the comparison establishes and what it does not: a broader posterior for extra parameters is not itself evidence that the model is better, and this project does not compute a Bayes factor.
- Perform a posterior predictive check in distance-modulus space and state which model failures it can and cannot reveal.
- Discuss limitations, including the fixed-$H_0$/intercept degeneracy, supernova standardization, covariance assumptions, and the fact that this is not a complete reproduction of the Pantheon+ collaboration analysis.

## Reproducible script requirement

Complete `scripts/run_pantheon_inference.py` as an independent workflow. It must download/load the data, run fitting and `emcee` without relying on notebook variables, and save final figures and machine-readable summaries. The `--steps` argument is the number of production steps per walker; `--warmup` is the number of burn-in steps. A command-line run should look like:

```bash
python scripts/run_pantheon_inference.py --steps 2000 --warmup 500 --seed 2202
```

The script should save at least:

```text
figures/pantheon_hubble_diagram.png
figures/pantheon_covariance.png
figures/pantheon_posterior.png
figures/pantheon_mcmc_diagnostics.png
figures/pantheon_posterior_predictive.png
outputs/pantheon_posterior_samples.npz
outputs/pantheon_parameter_summary.csv
outputs/pantheon_chain_diagnostics.csv
outputs/pantheon_prior_sensitivity.csv
```

The notebook is the guided analysis. The script is a separate reproducibility deliverable and must run from a clean Python process.

## References and course connections

- Pantheon+ public data: https://github.com/PantheonPlusSH0ES/DataRelease
- Brout et al. (2022), Pantheon+ cosmological constraints: https://arxiv.org/abs/2202.04077
- Scolnic et al. (2022), Pantheon+ full dataset: https://arxiv.org/abs/2112.03863
- Course lectures: https://github.com/jrstevenjlab/gradcompphys/tree/main/lectures
- Lecture 17, Bayesian inference: https://github.com/jrstevenjlab/gradcompphys/blob/main/lectures/lecture17_11_5_26_bayesian_inference.ipynb
- Lecture 18, `emcee` production sampling: https://github.com/jrstevenjlab/gradcompphys/blob/main/lectures/lecture18_11_10_26_mcmc.ipynb
- Lecture 19, model checking: https://github.com/jrstevenjlab/gradcompphys/blob/main/lectures/lecture19_11_12_26_model_checking_flows.ipynb

## Submission

Keep the repository private in the course organization. Make meaningful commits and submit a pull request from `submission` into `main`.
