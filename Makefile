PY ?= .venv/bin/python
PROCS ?= 32

# one BLAS thread per worker: the experiments parallelise over processes, and multithreaded BLAS
# inside each worker oversubscribes the cores (R04 made no progress until this was set)
export OMP_NUM_THREADS = 1
export OPENBLAS_NUM_THREADS = 1
export MKL_NUM_THREADS = 1

.PHONY: test reliability same-information mixed-noise competitors data apipop heterogeneous all

test:
	$(PY) -m pytest -q

# seconds: exact latent reliability at the Gaussian-extremal law, q = 0.8, 0.9, 0.95
reliability:
	$(PY) experiments/r01_reliability_curves.py

# minutes: rules with the same information, bimodal latent law, mixed noise
same-information:
	$(PY) experiments/r02_same_information.py 2000 $(PROCS)

# exact reliability under mixed noise laws at the extremal latent law (minutes, one core per case)
mixed-noise:
	$(PY) experiments/r03_mixed_noise_stress.py

# hours on 32 cores: comparison with existing methods; resumes from its checkpoint if interrupted
competitors:
	$(PY) experiments/r04_competitors.py 300 200 $(PROCS) hetldc

# downloads the pinned CRAN `survey` 4.5 tarball and checks api.rda against its SHA-256
data/apipop.pkl:
	$(PY) experiments/fetch_apipop.py

data: data/apipop.pkl

# school-district application
apipop: data/apipop.pkl
	$(PY) experiments/r05_apipop.py 120 $(PROCS)

# seconds: exact check of the heterogeneous-latent corollary
heterogeneous:
	$(PY) experiments/r06_heterogeneous_latent.py

all: test reliability same-information mixed-noise competitors apipop heterogeneous
