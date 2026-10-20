

https://github.com/user-attachments/assets/4a75ac49-8e74-4829-af12-d3e2b0fdab8f



# 3D Brownian Motion Simulation (Langevin Equation)

A Python simulation of a Brownian particle in a fluid, numerically
integrating the Langevin equation in three dimensions:

    M · dv/dt = −γ·v + F(t)

where −γ·v is the viscous drag and F(t) is Gaussian white noise whose
amplitude is set by the fluctuation-dissipation theorem
(⟨F²⟩ ∝ 2·γ·k_B·T).

The project generates many trajectories in parallel for different
diffusion coefficients `D = k_B·T / γ`, stores them, visualizes them, and
compares the results with theory.

## Features

- **Euler-Maruyama** integration in 3D (position and velocity).
- Two formulations of the dynamics:
  - **Equation 1:** dimensional Langevin equation (short time step).
  - **Equation 2:** non-dimensionalized equation using the characteristic time `M/γ` (long time step).
- **Parallel** simulation generation (`multiprocessing`) with a progress bar.
- Each simulation is saved as `.npz`, with a unique ID and its parameters in the file name.
- 2D (XY plane) visualization of trajectories, colored by `D`.
- Animation export to **transparent-background video** (`.mov`, via FFmpeg).
- Statistical study over many simulations:
  - Experimental ⟨V²⟩ vs. its theoretical evolution towards the equipartition value `3·k_B·T/M`.
  - Experimental ⟨|V|⟩ vs. the Maxwell-Boltzmann limit `√(8·k_B·T / (π·M))`.

## Project structure

| File | Description |
|---|---|
| `main.py` | Entry point. Menu to create new simulations or load and plot saved ones. |
| `dinamica.py` | Integrates the particle dynamics (equations 1 and 2). |
| `fuerzaestocastica.py` | Generates Gaussian noise with the correct amplitude for Euler-Maruyama. |
| `guardarsimulacion.py` | Saves trajectory, times and parameters to `simulaciones/*.npz`. |
| `leerdatos.py` | Reads an `.npz` file and returns its contents as a dictionary. |
| `representardatos.py` | Plots and animates trajectories; exports the transparent video. |
| `estudioprobabilistico.py` | Statistical analysis of several simulations against theory. |

## Installation

```bash
git clone https://github.com/YOUR_USER/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
pip install -r requirements.txt
```

Exporting videos requires [FFmpeg](https://ffmpeg.org/). Set its path at the
top of `representardatos.py`:

```python
plt.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'
```

## Usage

```bash
python main.py
```

- **`1` (Create):** runs the simulations defined in `main.py` and saves them to `simulaciones/`.
- **`0` (Read):** lists the saved simulations, lets you plot one or all of them, and optionally animate them and save the video.

### Default parameters

Edit them directly in `main.py`:

| Parameter | Value | Meaning |
|---|---|---|
| `T` | 298.15 K | Temperature |
| `M` | 1e-12 kg | Particle mass |
| `D_targets` | 1e-19, 1e-20, 1e-21 m²/s | Diffusion coefficients (γ = k_B·T / D) |
| `particulas_por_D` | 10 | Trajectories per coefficient |
| `cond` | `[0, 1e-15, 2e-10, 1]` | Initial time, time step `dt`, final time, equation number |
| `v_ini` | zeros | Initial position and velocity |

### Statistical study

```python
from estudioprobabilistico import estudioprobabilistico

estudioprobabilistico(["datos_xxxxxx_....npz", ...])
# or, to load every simulation of the same version:
estudioprobabilistico(["datos_xxxxxx_....npz"], lectura=True)
```

## Results

<img width="1400" height="600" alt="convergencia155simulaciones" src="https://github.com/user-attachments/assets/94a09098-05da-4b38-b4a5-7fa9e84177d6" />



https://github.com/user-attachments/assets/c34f2608-5cfc-42ce-a5a3-41c4ac4707f2



<img width="800" height="800" alt="119particulasbrownianas" src="https://github.com/user-attachments/assets/82f10550-6c8a-44ac-a89b-3fba7b2cd6fa" />


## Requirements

- Python 3.9 or higher
- numpy, scipy, matplotlib, tqdm
- FFmpeg (optional, only for video export)
