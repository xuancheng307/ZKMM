"""
Generate three SVG figures for the thesis proposal report.
  Fig 1: Taylor vs Minimax ULP error for exp(x)-1
  Fig 2: ULP histograms for exp, ln, erf
  Fig 3: Batch scaling Method G vs B
"""

import math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ── Global style ──────────────────────────────────────────────────────────────
BLUE = '#2b6cb0'
RED = '#e53e3e'
GREEN = '#38a169'

plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
})

OUT_DIR = r'D:\畢業論文v4\提案報告\figures'


def remove_top_right_spines(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)


# ── Horner evaluation (pure Python big-int) ───────────────────────────────────
def horner_eval(D, R):
    """Evaluate P = (((D[0]*R + D[1])*R + D[2])*R + D[3])*R + D[4]) * R
    using Python ints. D has 5 elements (D5..D1). Returns P."""
    acc = D[0]
    for i in range(1, 5):
        acc = acc * R + D[i]
    P = acc * R
    return P


S = 65536
S5 = S ** 5  # 65536^5


# ══════════════════════════════════════════════════════════════════════════════
# Figure 1: Taylor vs Minimax ULP error for exp(x)-1
# ══════════════════════════════════════════════════════════════════════════════
def generate_fig1():
    print("Generating fig1_taylor_vs_minimax.svg ...")

    D_minimax = [772, 166960606, 47192951395326, 9220542387939544845,
                 1208935047551242989517054]
    D_taylor = [546, 178956971, 46912496118443, 9223372036854775808,
                1208925819614629174706176]

    R_max = 45426
    R_vals = list(range(0, R_max + 1))

    ulp_minimax = []
    ulp_taylor = []

    for R in R_vals:
        # Minimax
        P_m = horner_eval(D_minimax, R)
        w_m = P_m // S5

        # Taylor
        P_t = horner_eval(D_taylor, R)
        w_t = P_t // S5

        # Reference
        w_ref = round(math.expm1(R / S) * S)

        ulp_minimax.append(abs(w_m - w_ref))
        ulp_taylor.append(abs(w_t - w_ref))

    max_ulp_minimax = max(ulp_minimax)
    max_ulp_taylor = max(ulp_taylor)
    print(f"  exp: max ULP minimax={max_ulp_minimax}, taylor={max_ulp_taylor}")

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(R_vals, ulp_taylor, color=RED, linewidth=0.3, alpha=0.7,
            label=f'Taylor (max ULP={max_ulp_taylor})')
    ax.plot(R_vals, ulp_minimax, color=BLUE, linewidth=0.3, alpha=0.7,
            label=f'Minimax (max ULP={max_ulp_minimax})')
    ax.set_xlabel('R (fixed-point input)')
    ax.set_ylabel('ULP Error')
    ax.set_ylim(0, 14)
    ax.set_title(r'$\exp(x)-1$ on $[0,\,\ln 2)$: Taylor vs Minimax ULP Error')
    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, color='lightgray', linewidth=0.5)
    remove_top_right_spines(ax)

    fig.tight_layout()
    path = f'{OUT_DIR}\\fig1_taylor_vs_minimax.svg'
    fig.savefig(path, format='svg')
    plt.close(fig)
    print(f"  Saved: {path}")
    return ulp_minimax  # reuse for fig2


# ══════════════════════════════════════════════════════════════════════════════
# Figure 2: ULP histograms for exp, ln, erf
# ══════════════════════════════════════════════════════════════════════════════
def compute_ulp_array(D, R_max, ref_func):
    """Compute ULP array for a given function."""
    ulps = []
    for R in range(0, R_max + 1):
        P = horner_eval(D, R)
        w = P // S5
        w_ref = round(ref_func(R / S) * S)
        ulps.append(abs(w - w_ref))
    return ulps


def generate_fig2(exp_ulps=None):
    print("Generating fig2_ulp_histograms.svg ...")

    # ── exp ──
    if exp_ulps is None:
        D_exp = [772, 166960606, 47192951395326, 9220542387939544845,
                 1208935047551242989517054]
        exp_ulps = compute_ulp_array(D_exp, 45426, math.expm1)
    max_exp = max(exp_ulps)
    print(f"  exp: max ULP={max_exp}")

    # ── ln ──
    D_ln = [3344, -730064963, 87363023329837, -9166709246312651464,
            1208759815998055276524329]
    ln_ulps = compute_ulp_array(D_ln, 45426, math.log1p)
    max_ln = max(ln_ulps)
    print(f"  ln:  max ULP={max_ln}")

    # ── erf ──
    D_erf = [787, 579083775, -125846944001408, 289907292761500882,
             1362777516625049393273811]
    erf_ulps = compute_ulp_array(D_erf, 65535, math.erf)
    max_erf = max(erf_ulps)
    print(f"  erf: max ULP={max_erf}")

    # ── Plot ──
    fig, axes = plt.subplots(1, 3, figsize=(12, 4))

    datasets = [
        (exp_ulps, 'exp', f'$\\exp(x)-1$\nmax ULP={max_exp}', BLUE),
        (ln_ulps, 'ln', f'$\\ln(1+x)$\nmax ULP={max_ln}', BLUE),
        (erf_ulps, 'erf', f'$\\mathrm{{erf}}(x)$\nmax ULP={max_erf}', BLUE),
    ]

    for i, (ulps, name, title, color) in enumerate(datasets):
        ax = axes[i]
        max_u = max(ulps)
        bins = np.arange(0, max_u + 2) - 0.5  # center bars on integers
        ax.hist(ulps, bins=bins, color=color, edgecolor='white', alpha=0.85)
        ax.set_title(title)
        ax.set_xlabel('ULP')
        if i == 0:
            ax.set_ylabel('Count')

        # Annotate ULP=0 percentage
        count_zero = ulps.count(0)
        pct = count_zero / len(ulps) * 100
        ax.annotate(f'ULP=0: {pct:.1f}%',
                     xy=(0, count_zero), xytext=(max_u * 0.4, count_zero * 0.8),
                     fontsize=10, color='black',
                     arrowprops=dict(arrowstyle='->', color='gray', lw=1.2))

        ax.set_xticks(range(0, max_u + 1))
        remove_top_right_spines(ax)
        ax.grid(True, axis='y', color='lightgray', linewidth=0.5)

    fig.tight_layout()
    path = f'{OUT_DIR}\\fig2_ulp_histograms.svg'
    fig.savefig(path, format='svg')
    plt.close(fig)
    print(f"  Saved: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Figure 3: Batch scaling Method G vs B
# ══════════════════════════════════════════════════════════════════════════════
def generate_fig3():
    print("Generating fig3_batch_scaling.svg ...")

    N = [1, 10, 100, 1000]
    G_prove = [115.9, 127.1, 237.0, 1010.6]
    B_prove = [58.9, 56.3, 60.9, 135.1]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(N, G_prove, color=BLUE, marker='o', markersize=8, linewidth=2,
            label='Method G (generic)')
    ax.plot(N, B_prove, color=RED, marker='s', markersize=8, linewidth=2,
            label='Method B (batched)')

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Number of function calls (N)')
    ax.set_ylabel('Prove time (ms)')
    ax.set_title('Batch Scaling: Method G vs Method B')

    # Annotate 7.5x gap at N=1000
    ax.annotate('7.5x gap',
                xy=(1000, G_prove[3]),
                xytext=(300, G_prove[3] * 1.8),
                fontsize=12, fontweight='bold', color=BLUE,
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))

    ax.legend(loc='upper left', framealpha=0.9)
    ax.grid(True, which='both', color='lightgray', linewidth=0.5)
    remove_top_right_spines(ax)

    # Set sensible tick labels for log scale
    ax.set_xticks(N)
    ax.set_xticklabels([str(n) for n in N])

    fig.tight_layout()
    path = f'{OUT_DIR}\\fig3_batch_scaling.svg'
    fig.savefig(path, format='svg')
    plt.close(fig)
    print(f"  Saved: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    print("=" * 60)
    print("Generating thesis proposal figures")
    print("=" * 60)

    exp_ulps = generate_fig1()
    generate_fig2(exp_ulps)
    generate_fig3()

    print("=" * 60)
    print("All 3 figures generated successfully!")
    print("=" * 60)
