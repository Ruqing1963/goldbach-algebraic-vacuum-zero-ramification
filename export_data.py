"""
export_data.py — Export zero-ramification scan data to CSV
"""
import math, csv
import numpy as np

def sieve(limit):
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[i]:
            is_prime[i*i::i] = bytearray(len(is_prime[i*i::i]))
    return is_prime

def odd_radical(n):
    if n <= 1: return 1
    r, temp = 1, n
    while temp % 2 == 0: temp //= 2
    d = 3
    while d * d <= temp:
        if temp % d == 0:
            r *= d
            while temp % d == 0: temp //= d
        d += 2
    if temp > 1: r *= temp
    return r

LIMIT = 16384
is_prime = sieve(LIMIT + 1)

# 1. Full scan at N=1024
N = 1024
rows = []
for p in range(3, N // 2 + 1):
    q = N - p
    if q <= 1: continue
    rp = odd_radical(p)
    rq = odd_radical(q)
    cond = (rp * rq) ** 2
    rho = math.log(cond) / math.log(N) if cond > 1 else 0.0
    if is_prime[p] and is_prime[q]: typ = "Goldbach"
    elif not is_prime[p] and not is_prime[q]: typ = "Composite"
    else: typ = "Mixed"
    rows.append([N, p, q, typ, rp, rq, cond, round(rho, 6)])

with open('/home/claude/repo9/data/decompositions_N1024.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['N', 'p', 'q', 'type', 'rad_odd_p', 'rad_odd_q', 'conductor_proxy', 'rho'])
    w.writerows(rows)
print(f"Exported {len(rows)} rows to decompositions_N1024.csv")

# 2. 2^k evolution table
rows2 = []
for k in range(7, 15):
    Nk = 2**k
    gb_rhos, comp_rhos = [], []
    for p in range(3, Nk // 2 + 1):
        q = Nk - p
        if q <= 1: continue
        rp = odd_radical(p)
        rq = odd_radical(q)
        cond = (rp * rq) ** 2
        rho = math.log(cond) / math.log(Nk) if cond > 1 else 0.0
        if is_prime[p] and is_prime[q]:
            gb_rhos.append(rho)
        elif not is_prime[p] and not is_prime[q] and rho > 0:
            comp_rhos.append(rho)
    if gb_rhos and comp_rhos:
        bw_gb = max(gb_rhos) - min(gb_rhos)
        bw_comp = max(comp_rhos) - min(comp_rhos)
        ratio = bw_comp / bw_gb if bw_gb > 0 else 0
        rows2.append([Nk, k, len(gb_rhos),
                       round(min(gb_rhos), 6), round(float(np.mean(gb_rhos)), 6), round(max(gb_rhos), 6),
                       round(bw_gb, 6), round(bw_comp, 6), round(ratio, 2)])

with open('/home/claude/repo9/data/bandwidth_evolution_2k.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['N', 'k', 'num_goldbach', 'rho_min', 'rho_mean', 'rho_max', 'BW_goldbach', 'BW_composite', 'ratio'])
    w.writerows(rows2)
print(f"Exported {len(rows2)} rows to bandwidth_evolution_2k.csv")
