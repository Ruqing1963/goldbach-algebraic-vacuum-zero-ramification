"""
goldbach_rigid_scan.py — Zero-Ramification Scan at N = 2^k
============================================================
Generates the conductor energy-gap plot for N = 2^k, where rad_odd(N) = 1
eliminates background ramification entirely.

Two conductor models are compared:
  (A) Paper II formula: N_proxy = (rad_odd(p) * rad_odd(q))^2  [product]
  (B) LCM model:        N_proxy = lcm(rad_odd(p), rad_odd(q))^2 [union of support]

For N = 2^k, both reduce to functions of p and q alone (static conduit vanishes).
"""
import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Utilities ────────────────────────────────────────────────────────────────

def sieve_radicals(limit):
    """Compute rad(n) for all n up to limit via sieve."""
    rads = np.ones(limit + 1, dtype=np.int64)
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, limit + 1):
        if is_prime[i]:
            for j in range(i, limit + 1, i):
                if j != i:
                    is_prime[j] = 0
                rads[j] *= i
    primes_set = set(i for i in range(2, limit + 1) if is_prime[i])
    return rads, primes_set

def odd_rad(x, rads):
    """Odd part of radical."""
    r = int(rads[x])
    while r % 2 == 0:
        r //= 2
    return r if r > 0 else 1

# ─── Scan function ────────────────────────────────────────────────────────────

def scan_N(N, rads, primes_set):
    """Scan all decompositions p + q = N, compute Chen's ratio."""
    rows = []
    for p in range(3, N // 2 + 1):
        q = N - p
        if q <= 1:
            continue

        rp = odd_rad(p, rads)
        rq = odd_rad(q, rads)
        rM = odd_rad(N // 2, rads)

        # Paper II formula: product-based proxy
        base = rp * rq * rM * rM
        cond = base * base
        rho = math.log(cond) / math.log(N) if cond > 1 else 0.0

        # Classify
        p_is_prime = p in primes_set
        q_is_prime = q in primes_set
        if p_is_prime and q_is_prime:
            cat = 'Goldbach'
        elif p_is_prime or q_is_prime:
            cat = 'Mixed'
        else:
            cat = 'Composite'

        rows.append({
            'p': p, 'q': q,
            'rad_odd_p': rp, 'rad_odd_q': rq,
            'conductor_proxy': cond,
            'rho': rho,
            'category': cat
        })
    return rows

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN: Scan N = 1024 = 2^10
# ═══════════════════════════════════════════════════════════════════════════════

N = 1024
print(f"[*] Scanning N = {N} = 2^{int(math.log2(N))}")
print(f"    rad_odd(N/2) = rad_odd({N//2}) = {1 if N & (N-1) == 0 else '?'}")
print(f"    → Zero-ramification background: static conduit contributes NOTHING\n")

rads, primes_set = sieve_radicals(N + 1)
rows = scan_N(N, rads, primes_set)

# Separate categories
gb   = [r for r in rows if r['category'] == 'Goldbach']
mix  = [r for r in rows if r['category'] == 'Mixed']
comp = [r for r in rows if r['category'] == 'Composite']

gb.sort(key=lambda x: x['rho'])
comp.sort(key=lambda x: x['rho'])

# ─── Table output ─────────────────────────────────────────────────────────────
print("="*75)
print(f"TABLE: Ground State Decompositions at N = {N}")
print("="*75)
print(f"{'Type':<12} {'(p, q)':<16} {'rad_odd(p)':<12} {'rad_odd(q)':<12} {'ρ':<8}")
print("-"*75)
for r in gb[:5]:
    pair = f"({r['p']}, {r['q']})"
    print(f"{'Goldbach':<12} {pair:<16} {r['rad_odd_p']:<12} {r['rad_odd_q']:<12} {r['rho']:<8.4f}")
print("-"*75)
for r in comp[:5]:
    pair = f"({r['p']}, {r['q']})"
    print(f"{'Composite':<12} {pair:<16} {r['rad_odd_p']:<12} {r['rad_odd_q']:<12} {r['rho']:<8.4f}")

gb_rhos = [r['rho'] for r in gb]
mix_rhos = [r['rho'] for r in mix if r['rho'] > 0]
comp_rhos = [r['rho'] for r in comp if r['rho'] > 0]

print(f"\n  Goldbach  (n={len(gb):>3}): ρ ∈ [{min(gb_rhos):.4f}, {max(gb_rhos):.4f}], mean = {np.mean(gb_rhos):.4f}")
print(f"  Mixed     (n={len(mix):>3}): ρ ∈ [{min(mix_rhos):.4f}, {max(mix_rhos):.4f}], mean = {np.mean(mix_rhos):.4f}")
print(f"  Composite (n={len(comp):>3}): ρ ∈ [{min(comp_rhos):.4f}, {max(comp_rhos):.4f}], mean = {np.mean(comp_rhos):.4f}")
print(f"\n  Ground state: p={gb[0]['p']}, q={gb[0]['q']}, ρ = {gb[0]['rho']:.4f}")
print(f"  Bandwidth (Goldbach): {max(gb_rhos)-min(gb_rhos):.4f}")
print(f"  Bandwidth (Composite): {max(comp_rhos)-min(comp_rhos):.4f}")
print(f"  Ratio (comp/gb bandwidth): {(max(comp_rhos)-min(comp_rhos))/(max(gb_rhos)-min(gb_rhos)):.2f}x")


# ═══════════════════════════════════════════════════════════════════════════════
# FIGURE 3: Energy Gap at N = 1024 (Zero-Ramification)
# ═══════════════════════════════════════════════════════════════════════════════
print(f"\n[*] Generating Figure 3: Zero-Ramification Energy Gap at N = {N}...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5),
                                gridspec_kw={'width_ratios': [3, 1.2]})

# Left panel: scatter
p_gb = [r['p'] for r in gb]
rho_gb = [r['rho'] for r in gb]
p_mix = [r['p'] for r in mix]
rho_mix = [r['rho'] for r in mix if r['rho'] > 0]
p_mix_filt = [r['p'] for r in mix if r['rho'] > 0]
p_comp = [r['p'] for r in comp if r['rho'] > 0]
rho_comp_filt = [r['rho'] for r in comp if r['rho'] > 0]

ax1.scatter(p_comp, rho_comp_filt, s=4, color='#CC6644', alpha=0.2,
            label=f'Composite ($n={len(comp)}$)', zorder=1)
ax1.scatter(p_mix_filt, rho_mix, s=5, color='#88AA55', alpha=0.25,
            label=f'Mixed ($n={len(mix)}$)', zorder=2)
ax1.scatter(p_gb, rho_gb, s=18, color='#2255BB', alpha=0.75,
            label=f'Goldbach ($n={len(gb)}$)', zorder=3)

# Mark ground state
ax1.annotate(f'Ground state\n$p={gb[0]["p"]},\\; \\rho={gb[0]["rho"]:.3f}$',
             xy=(gb[0]['p'], gb[0]['rho']),
             xytext=(gb[0]['p'] + 60, gb[0]['rho'] - 0.3),
             fontsize=9, color='#2255BB',
             arrowprops=dict(arrowstyle='->', color='#2255BB', lw=1.2))

# Mean lines
mean_gb = np.mean(gb_rhos)
mean_comp = np.mean(comp_rhos)
ax1.axhline(y=mean_gb, color='#2255BB', linestyle='--', linewidth=1, alpha=0.5)
ax1.axhline(y=mean_comp, color='#CC6644', linestyle='--', linewidth=1, alpha=0.5)

# Gap annotation
mid = (mean_gb + mean_comp) / 2
gap = abs(mean_gb - mean_comp)
ax1.annotate('', xy=(N//2 - 30, mean_gb), xytext=(N//2 - 30, mean_comp),
             arrowprops=dict(arrowstyle='<->', color='#333333', lw=1.5))
ax1.text(N//2 - 15, mid, f'$\\Delta\\rho = {gap:.3f}$',
         fontsize=10, va='center', color='#333333')

ax1.set_xlabel('Summand $p$', fontsize=12)
ax1.set_ylabel("Chen's Ratio $\\rho(1024, p)$", fontsize=12)
ax1.set_title(f'Zero-ramification landscape: $N = 2^{{10}} = {N}$', fontsize=13)
ax1.legend(loc='lower right', fontsize=9, framealpha=0.92)
ax1.grid(True, alpha=0.15)

# Right panel: histogram
all_rho = gb_rhos + comp_rhos + mix_rhos
lo = min(r for r in all_rho if r > 0) - 0.1
hi = max(all_rho) + 0.1
bins = np.linspace(lo, hi, 50)

ax2.hist(gb_rhos, bins=bins, orientation='horizontal', color='#2255BB',
         alpha=0.6, label='Goldbach', density=True)
ax2.hist(rho_comp_filt, bins=bins, orientation='horizontal', color='#CC6644',
         alpha=0.3, label='Composite', density=True)
ax2.hist(rho_mix, bins=bins, orientation='horizontal', color='#88AA55',
         alpha=0.2, label='Mixed', density=True)

ax2.set_xlabel('Density', fontsize=11)
ax2.set_ylabel('$\\rho$', fontsize=11)
ax2.set_title('Distribution', fontsize=12)
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.15)

plt.suptitle(f'Figure 1 — Zero-Ramification Conductor Gap at $N = 2^{{10}} = {N}$',
             fontsize=14, y=1.02)
plt.tight_layout()
plt.savefig('/home/claude/figure1_N1024.pdf', dpi=300, bbox_inches='tight')
plt.savefig('/home/claude/figure1_N1024.png', dpi=200, bbox_inches='tight')
print("    Saved figure1_N1024.pdf/.png")

# ═══════════════════════════════════════════════════════════════════════════════
# Multi-N comparison: 2^k series
# ═══════════════════════════════════════════════════════════════════════════════
print(f"\n[*] Scanning 2^k series for zero-ramification evolution...")

LIMIT = 16384
rads_big, primes_big = sieve_radicals(LIMIT + 1)

print(f"\n{'N':<8} {'k':<4} {'#GB':<6} {'ρ_min':<8} {'ρ_mean':<8} {'ρ_max':<8} {'BW_GB':<8} {'BW_Comp':<8} {'Ratio':<6}")
print("-"*70)

for k in range(7, 15):
    Nk = 2**k
    if Nk > LIMIT:
        break
    rows_k = scan_N(Nk, rads_big, primes_big)
    gb_k = [r['rho'] for r in rows_k if r['category'] == 'Goldbach']
    comp_k = [r['rho'] for r in rows_k if r['category'] == 'Composite' and r['rho'] > 0]
    if gb_k and comp_k:
        bw_gb = max(gb_k) - min(gb_k)
        bw_comp = max(comp_k) - min(comp_k)
        ratio = bw_comp / bw_gb if bw_gb > 0 else float('inf')
        print(f"{Nk:<8} {k:<4} {len(gb_k):<6} {min(gb_k):<8.4f} {np.mean(gb_k):<8.4f} {max(gb_k):<8.4f} {bw_gb:<8.4f} {bw_comp:<8.4f} {ratio:<6.2f}")

print("\n[*] Done.")
