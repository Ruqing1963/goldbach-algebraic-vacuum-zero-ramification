# The Algebraic Vacuum: Zero-Ramification Conductor Model for the Goldbach Conjecture at N = 2^k

**Author:** Ruqing Chen, GUT Geoservice Inc., Montréal, QC, Canada

## Paper

> R. Chen, *The Algebraic Vacuum: Zero-Ramification Conductor Model for the Goldbach Conjecture at N = 2^k*, 2026.

This is Paper #9 in the conductor rigidity series:

| # | Paper | Link |
|---|-------|------|
| 7 | The Goldbach Mirror | [Zenodo 10.5281/zenodo.18684892](https://zenodo.org/records/18684892) |
| 8 | The Goldbach Mirror II: Geometric Foundations | [Zenodo 10.5281/zenodo.18719056](https://zenodo.org/records/18719056) |
| **9** | **The Algebraic Vacuum** (this paper) | *forthcoming* |

## Abstract

When N = 2^k, the static conduit factor rad_odd(N/2) = 1, so the conductor of the Goldbach–Frey Jacobian is governed entirely by the boundary summands p and q. This **algebraic vacuum** isolates the pure effect of radical rigidity on the conductor distribution. Scanning N = 2^k for k = 7, …, 14, we establish three structural phenomena:

1. **Ground state locking**: ρ_min → 2 from above, locked by rad(p) = p for primes (proved unconditionally)
2. **Bandwidth rigidity**: the composite-to-Goldbach bandwidth ratio is consistently ≥ 2.3 across all tested k
3. **Conductor floor**: Goldbach pairs satisfy ρ > 2, while composites can reach ρ = 0

## Key Results

| Result | Location | Status |
|--------|----------|--------|
| Conductor in the algebraic vacuum | Prop 2.1 | Proved unconditionally |
| Ground state floor ρ > 2 | Prop 3.2 | Proved unconditionally |
| Ground state asymptotics ρ_min → 2 | Prop 3.2(ii) | Conditional on Hardy–Littlewood |
| Bandwidth ratio R ≥ 2.3 | Table 2, Obs 4.1 | Computational (k = 7…14) |
| N = 1024 detailed landscape | Table 3, Figure 1 | Computational |

## Figure

### Figure 1 — Zero-Ramification Conductor Gap at N = 2¹⁰ = 1024

![Figure 1](figures/figure1_N1024.png)

**Left:** All 510 decompositions of N = 1024. Goldbach pairs (blue, n = 22) are bounded below at ρ = 2.316 (ground state p = 3, q = 1021) and cluster in a narrow band. Composites (orange, n = 361) spread from ρ = 0 to ρ = 3.6. **Right:** Density histogram. Mean gap Δρ = 0.650.

## Repository Contents

```
├── README.md
├── LICENSE
├── paper/
│   ├── Algebraic_Vacuum_Zero_Ramification_Conductor_Model.tex
│   └── Algebraic_Vacuum_Zero_Ramification_Conductor_Model.pdf   (7 pages)
├── figures/
│   ├── figure1_N1024.pdf
│   └── figure1_N1024.png
├── scripts/
│   ├── goldbach_rigid_scan.py   # Main scan: Figure 1 + Tables 1–3 + 2^k evolution
│   └── export_data.py           # Exports CSV data files
└── data/
    ├── decompositions_N1024.csv     # All 510 decompositions of N=1024
    └── bandwidth_evolution_2k.csv   # Bandwidth metrics for k=7…14
```

## Quick Start

```bash
pip install numpy matplotlib

# Run the zero-ramification scan (generates Figure 1 + all tables)
python scripts/goldbach_rigid_scan.py

# Export CSV data
python scripts/export_data.py
```

### Compiling the paper

```bash
cd paper
cp ../figures/figure1_N1024.pdf .
pdflatex Algebraic_Vacuum_Zero_Ramification_Conductor_Model.tex
pdflatex Algebraic_Vacuum_Zero_Ramification_Conductor_Model.tex
```

## Data Format

### decompositions_N1024.csv

| Column | Description |
|--------|-------------|
| `N` | Even number (1024) |
| `p`, `q` | Summands (p + q = N) |
| `type` | Goldbach, Composite, or Mixed |
| `rad_odd_p`, `rad_odd_q` | Odd radicals of summands |
| `conductor_proxy` | (rad_odd(p) × rad_odd(q))² |
| `rho` | Chen's ratio: log(conductor_proxy) / log(N) |

### bandwidth_evolution_2k.csv

| Column | Description |
|--------|-------------|
| `N`, `k` | N = 2^k |
| `num_goldbach` | Count of Goldbach pairs |
| `rho_min`, `rho_mean`, `rho_max` | ρ statistics over Goldbach pairs |
| `BW_goldbach`, `BW_composite` | Bandwidth of each class |
| `ratio` | BW_composite / BW_goldbach |

## Citation

```bibtex
@article{Chen2026AV,
  author  = {Ruqing Chen},
  title   = {The Algebraic Vacuum: Zero-Ramification Conductor Model
             for the Goldbach Conjecture at {$N = 2^k$}},
  year    = {2026},
  note    = {Preprint},
  url     = {https://github.com/Ruqing1963/goldbach-algebraic-vacuum-zero-ramification}
}
```

## Related Repositories

- [goldbach-mirror-conductor-rigidity](https://github.com/Ruqing1963/goldbach-mirror-conductor-rigidity) — Paper #7
- [goldbach-mirror-II-geometric-foundations](https://github.com/Ruqing1963/goldbach-mirror-II-geometric-foundations) — Paper #8

## License

[MIT License](LICENSE)
