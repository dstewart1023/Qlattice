#!/usr/bin/env python3

from auto_contractor.operators import *

import functools
import math
import os
import time
import importlib
import sys
import math
import cmath

import qlat_gpt as qg

from qlat_scripts.v1 import *

is_cython = False

# ----

load_path_list[:] = [
        "results",
        "qcddata",
        "qcddata-1",
        "qcddata-2",
        "qcddata-3",
        "qcddata-4",
        "qcddata-5",
        ]

# ----

@q.timer
def get_cexpr_meson_corr():
    fn_base = "cache/auto_contract_cexpr/get_cexpr_meson_corr"
    def calc_cexpr():
        diagram_type_dict = dict()
        diagram_type_dict[((('x_1', 'x_2'), 1), (('x_2', 'x_1'), 1))] = 'Type1'
        diagram_type_dict[((('x_1', 'x_1'), 1), (('x_2', 'x_2'), 1))] = None
        exprs = [
                mk_fac(1) + f"1",
                mk_pi_p("x_2", True)    * mk_pi_p("x_1")             + f"pi+^dag(0) * pi+(-tsep)",
                mk_k_p("x_2", True)     * mk_k_p("x_1")              + f"K+^dag(0) * K+(-tsep)",
                mk_pi_p("x_2", True)    * mk_j5pi_mu("x_1", 3, True) + f"pi+^dag(0) * j5pi_t^dag(-tsep)",
                mk_k_p("x_2", True)     * mk_j5k_mu("x_1", 3, True)  + f"K+^dag(0) * j5k_t^dag(-tsep)",
                mk_j5pi_mu("x_2", 3)    * mk_pi_p("x_1")             + f"j5pi_t(0) * pi+(-tsep)",
                mk_j5k_mu("x_2", 3)     * mk_k_p("x_1")              + f"j5k_t(0) * K+(-tsep)",
                mk_j5pi_mu("x_2", 3)    * mk_j5pi_mu("x_1", 3, True) + f"j5pi_t(0) * j5pi_t^dag(-tsep)",
                mk_j5k_mu("x_2", 3)     * mk_j5k_mu("x_1", 3, True)  + f"j5k_t(0) * j5k_t^dag(-tsep)",
                mk_a0_p("x_2", True)    * mk_a0_p("x_1")             + f"a0+^dag(0) * a0+(-tsep)",
                mk_kappa_p("x_2", True) * mk_kappa_p("x_1")          + f"kappa+^dag(0) * kappa+(-tsep)",
                mk_j_mu("x_2", 3)       * mk_j_mu("x_1", 3)          + f"j_t(0) * j_t(-tsep)",
                sum([ mk_j_mu("x_2", mu) * mk_j_mu("x_1", mu) for mu in range(4) ])
                + f"j_mu(0) * j_mu(-tsep)",
                sum([ mk_j5pi_mu("x_2", mu) * mk_j5pi_mu("x_1", mu, True) for mu in range(4) ])
                + f"j5pi_mu(0) * j5pi_mu^dag(-tsep)",
                sum([ mk_j5k_mu("x_2", mu) * mk_j5k_mu("x_1", mu, True) for mu in range(4) ])
                + f"j5k_mu(0) * j5k_mu^dag(-tsep)",
                ]
        cexpr = contract_simplify_compile(
                *exprs,
                is_isospin_symmetric_limit=True,
                diagram_type_dict=diagram_type_dict,
                )
        return cexpr
    return cache_compiled_cexpr(calc_cexpr, fn_base, is_cython=is_cython)

@q.timer_verbose
def auto_contract_meson_corr(job_tag, traj, get_get_prop):
    fname = q.get_fname()
    fn = f"{job_tag}/auto-contract/traj-{traj}/meson_corr.lat"
    if get_load_path(fn) is not None:
        return
    cexpr = get_cexpr_meson_corr()
    expr_names = get_cexpr_names(cexpr)
    get_prop = get_get_prop()
    total_site = q.Coordinate(get_param(job_tag, "total_site"))
    t_size = total_site[3]
    geo = q.Geometry(total_site, 1)
    total_volume = geo.total_volume()
    def load_data():
        t_t_list = get_mpi_chunk(
                [ (t_src, t_snk,) for t_snk in range(t_size) for t_src in range(t_size) ],
                rng_state = None)
        for t_src, t_snk in t_t_list:
            yield t_src, t_snk
    @q.timer
    def feval(args):
        t_src, t_snk = args
        t = (t_snk - t_src) % t_size
        pd = {
                "x_2": ("wall", t_snk,),
                "x_1": ("wall", t_src,),
                "size": total_site,
                }
        val = eval_cexpr(cexpr, positions_dict=pd, get_prop=get_prop)
        return val, t
    def sum_function(val_list):
        values = np.zeros((t_size, len(expr_names),), dtype=complex)
        for val, t in val_list:
            values[t] += val
        return q.glb_sum(values.transpose(1, 0))
    chunk_size = get_param(job_tag, "measurement", "auto_contractor_chunk_size", default = 128)
    q.timer_fork(0)
    res_sum = q.parallel_map_sum(feval, load_data(), sum_function=sum_function, chunksize=chunk_size)
    q.displayln_info(f"{fname}: timer_display for parallel_map_sum")
    q.timer_display()
    q.timer_merge()
    res_sum *= 1.0 / t_size
    assert q.qnorm(res_sum[0] - 1.0) < 1e-10
    ld = q.mk_lat_data([
        [ "expr_name", len(expr_names), expr_names, ],
        [ "t_sep", t_size, [ str(q.rel_mod(t, t_size)) for t in range(t_size) ], ],
        ])
    ld.from_numpy(res_sum)
    ld.save(get_save_path(fn))
    q.displayln_info(f"CHECK: {fname}: ld sig: {q.get_double_sig(ld, q.RngState()):.5E}")

@q.timer_verbose
def auto_contract_meson_corr_psnk(job_tag, traj, get_get_prop):
    fname = q.get_fname()
    fn = f"{job_tag}/auto-contract/traj-{traj}/meson_corr_psnk.lat"
    if get_load_path(fn) is not None:
        return
    cexpr = get_cexpr_meson_corr()
    expr_names = get_cexpr_names(cexpr)
    total_site = q.Coordinate(get_param(job_tag, "total_site"))
    t_size = total_site[3]
    geo = q.Geometry(total_site, 1)
    total_volume = geo.total_volume()
    get_prop = get_get_prop()
    xg_list = get_all_points(total_site)
    xg_local_list = [ q.Coordinate(xg) for xg in geo.xg_list() ]
    def load_data():
        for t_src in range(t_size):
            for xg_snk in xg_local_list:
                yield t_src, xg_snk
    @q.timer
    def feval(args):
        t_src, xg_snk = args
        t = (xg_snk[3] - t_src) % t_size
        pd = {
                "x_2" : ("point", xg_snk,),
                "x_1" : ("wall", t_src,),
                "size" : total_site,
                }
        val = eval_cexpr(cexpr, positions_dict=pd, get_prop=get_prop)
        return val, t
    def sum_function(val_list):
        values = np.zeros((t_size, len(expr_names),), dtype=complex)
        for val, t in val_list:
            values[t] += val
        return q.glb_sum(values.transpose(1, 0))
    chunk_size = get_param(job_tag, "measurement", "auto_contractor_chunk_size", default = 128)
    q.timer_fork(0)
    res_sum = q.parallel_map_sum(feval, load_data(), sum_function=sum_function, chunksize=chunk_size)
    q.displayln_info(f"{fname}: timer_display for parallel_map_sum")
    q.timer_display()
    q.timer_merge()
    res_sum *= 1.0 / total_volume
    assert q.qnorm(res_sum[0] - 1.0) < 1e-10
    ld = q.mk_lat_data([
        [ "expr_name", len(expr_names), expr_names, ],
        [ "t_sep", t_size, [ str(q.rel_mod(t, t_size)) for t in range(t_size) ], ],
        ])
    ld.from_numpy(res_sum)
    ld.save(get_save_path(fn))
    q.displayln_info(f"CHECK: {fname}: ld sig: {q.get_double_sig(ld, q.RngState()):.5E}")

@q.timer_verbose
def auto_contract_meson_corr_psnk_psrc(job_tag, traj, get_get_prop):
    fname = q.get_fname()
    fn = f"{job_tag}/auto-contract/traj-{traj}/meson_corr_psnk_psrc.lat"
    if get_load_path(fn) is not None:
        return
    cexpr = get_cexpr_meson_corr()
    expr_names = get_cexpr_names(cexpr)
    total_site = q.Coordinate(get_param(job_tag, "total_site"))
    t_size = total_site[3]
    geo = q.Geometry(total_site, 1)
    total_volume = geo.total_volume()
    get_prop = get_get_prop()
    xg_list = get_all_points(total_site)
    xg_local_list = [ q.Coordinate(xg) for xg in geo.xg_list() ]
    r_list = get_r_list(job_tag)
    r_sq_interp_idx_coef_list = get_r_sq_interp_idx_coef_list(job_tag)
    def load_data():
        for xg_src in xg_local_list:
            yield xg_src
    @q.timer
    def feval(args):
        xg_src = args
        res_list = []
        for xg_snk in xg_list:
            x_rel = q.smod(xg_snk - xg_src, total_site)
            r_sq = x_rel.r_sqr()
            r_idx_low, r_idx_high, coef_low, coef_high = r_sq_interp_idx_coef_list[r_sq]
            t = x_rel[3]
            pd = {
                    "x_2": ("point", xg_snk,),
                    "x_1": ("point", xg_src,),
                    "size": total_site,
                    }
            val = eval_cexpr(cexpr, positions_dict=pd, get_prop=get_prop)
            res_list.append((val, t, r_idx_low, r_idx_high, coef_low, coef_high,))
        return res_list
    def sum_function(val_list):
        values = np.zeros((t_size, len(r_list), len(expr_names),), dtype=complex)
        for idx, res_list in enumerate(val_list):
            for val, t, r_idx_low, r_idx_high, coef_low, coef_high in res_list:
                values[t, r_idx_low] += coef_low * val
                values[t, r_idx_high] += coef_high * val
            q.displayln_info(f"{fname}: {idx+1}/{len(xg_local_list)}")
        return q.glb_sum(values.transpose(2, 0, 1))
    q.timer_fork(0)
    res_sum = q.parallel_map_sum(feval, load_data(), sum_function=sum_function, chunksize=1)
    q.displayln_info(f"{fname}: timer_display for parallel_map_sum")
    q.timer_display()
    q.timer_merge()
    res_sum *= 1.0 / (total_volume * total_volume / t_size)
    assert q.qnorm(res_sum[0].sum(1) - 1.0) < 1e-10
    ld = q.mk_lat_data([
        [ "expr_name", len(expr_names), expr_names, ],
        [ "t_sep", t_size, [ str(q.rel_mod(t, t_size)) for t in range(t_size) ], ],
        [ "r", len(r_list), [ f"{r:.5f}" for r in r_list ], ],
        ])
    ld.from_numpy(res_sum)
    ld.save(get_save_path(fn))
    q.displayln_info(f"CHECK: {fname}: ld sig: {q.get_double_sig(ld, q.RngState()):.5E}")

@q.timer_verbose
def auto_contract_meson_corr_psnk_psrc_rand(job_tag, traj, get_get_prop):
    fname = q.get_fname()
    fn = f"{job_tag}/auto-contract/traj-{traj}/meson_corr_psnk_psrc_rand.lat"
    if get_load_path(fn) is not None:
        return
    cexpr = get_cexpr_meson_corr()
    expr_names = get_cexpr_names(cexpr)
    total_site = q.Coordinate(get_param(job_tag, "total_site"))
    t_size = total_site[3]
    geo = q.Geometry(total_site, 1)
    total_volume = geo.total_volume()
    get_prop = get_get_prop()
    xg_list = get_all_points(total_site)
    xg_local_list = [ q.Coordinate(xg) for xg in geo.xg_list() ]
    r_list = get_r_list(job_tag)
    r_sq_interp_idx_coef_list = get_r_sq_interp_idx_coef_list(job_tag)
    sample_num = get_param(job_tag, "measurement", "auto_contract_meson_corr_psnk_psrc_rand", "sample_num", default=128)
    sample_size = get_param(job_tag, "measurement", "auto_contract_meson_corr_psnk_psrc_rand", "sample_size", default=128)
    rs = q.RngState(f"{job_tag}-{traj}-{fname}")
    mpi_chunk = get_mpi_chunk(list(range(sample_num)))
    def load_data():
        for idx in mpi_chunk:
            yield idx
    @q.timer
    def feval(args):
        idx = args
        res_list = []
        for idx2 in range(sample_size):
            rsi = rs.split(f"{idx}-{idx2}")
            xg_src = rsi.c_rand_gen(total_site)
            xg_snk = rsi.c_rand_gen(total_site)
            x_rel = q.smod(xg_snk - xg_src, total_site)
            r_sq = x_rel.r_sqr()
            r_idx_low, r_idx_high, coef_low, coef_high = r_sq_interp_idx_coef_list[r_sq]
            t = x_rel[3]
            pd = {
                    "x_2": ("point", xg_snk,),
                    "x_1": ("point", xg_src,),
                    "size": total_site,
                    }
            val = eval_cexpr(cexpr, positions_dict=pd, get_prop=get_prop)
            res_list.append((val, t, r_idx_low, r_idx_high, coef_low, coef_high,))
        return res_list
    def sum_function(val_list):
        values = np.zeros((t_size, len(r_list), len(expr_names),), dtype=complex)
        for idx, res_list in enumerate(val_list):
            for val, t, r_idx_low, r_idx_high, coef_low, coef_high in res_list:
                values[t, r_idx_low] += coef_low * val
                values[t, r_idx_high] += coef_high * val
            q.displayln_info(f"{fname}: {idx+1}/{len(mpi_chunk)}")
        return q.glb_sum(values.transpose(2, 0, 1))
    q.timer_fork(0)
    res_sum = q.parallel_map_sum(feval, load_data(), sum_function=sum_function, chunksize=1)
    q.displayln_info(f"{fname}: timer_display for parallel_map_sum")
    q.timer_display()
    q.timer_merge()
    res_sum *= 1.0 / (sample_num * sample_size / t_size)
    # assert q.qnorm(res_sum[0].sum(1) - 1.0) < 1e-10
    ld = q.mk_lat_data([
        [ "expr_name", len(expr_names), expr_names, ],
        [ "t_sep", t_size, [ str(q.rel_mod(t, t_size)) for t in range(t_size) ], ],
        [ "r", len(r_list), [ f"{r:.5f}" for r in r_list ], ],
        ])
    ld.from_numpy(res_sum)
    ld.save(get_save_path(fn))
    q.displayln_info(f"CHECK: {fname}: ld sig: {q.get_double_sig(ld, q.RngState()):.5E}")

# ----

def wave_function(p1, p2, radius, size):
    p1_tag, c1 = p1
    p2_tag, c2 = p2
    c12 = q.smod(c1 - c2, size)
    c12_r_sqr = c12.r_sqr()
    dis = math.sqrt(c12_r_sqr)
    wf = math.exp(-dis / radius)
    return wf

def momentum_factor(mom, p, size, is_dagger=False):
    p_tag, c = p
    phase = mom[0] * c[0] / size[0] + mom[1] * c[1] / size[1] + mom[2] * c[2] / size[2]
    phase = phase * 2.0 * math.pi
    if not is_dagger:
        mf = cmath.rect(1.0, phase)
    else:
        mf = cmath.rect(1.0, -phase)
    return mf

def mk_meson_wf(f1, f2, p1, p2, radius, mom, is_dagger=False):
    """
    i q1bar g5 q2 #dag: i q2bar g5 q1
    return the actual dagger of the operator
    """
    s1 = new_spin_index()
    s2 = new_spin_index()
    c = new_color_index()
    g5 = G(5, s1, s2)
    wf = mk_fac(f"wave_function({p1},{p2},{radius},size)")
    if not is_dagger:
        q1b = Qb(f1, p1, s1, c)
        q2v = Qv(f2, p2, s2, c)
        mf = mk_fac(f"momentum_factor({mom},{p2},size)")
        return sympy.I * wf * mf * q1b * g5 * q2v + f"(i {f1}bar g5 {f2})({p1},{p2})"
    else:
        q2b = Qb(f2, p2, s1, c)
        q1v = Qv(f1, p1, s2, c)
        mf = mk_fac(f"momentum_factor(-{mom},{p2},size)")
        return sympy.I * wf * mf * q2b * g5 * q1v + f"(i {f2}bar g5 {f1})({p2},{p1},{radius},{mom})"

def mk_scalar_meson_wf(f1, f2, p1, p2, radius, mom, is_dagger=False):
    """
    i q1bar g5 q2 #dag: i q2bar g5 q1
    return the actual dagger of the operator
    """
    s = new_spin_index()
    c = new_color_index()
    wf = mk_fac(f"wave_function({p1},{p2},{radius},size)")
    if not is_dagger:
        q1b = Qb(f1, p1, s, c)
        q2v = Qv(f2, p2, s, c)
        mf = mk_fac(f"momentum_factor({mom},{p2},size)")
        return wf * mf * q1b * q2v + f"({f1}bar {f2})({p1},{p2})"
    else:
        q2b = Qb(f2, p2, s, c)
        q1v = Qv(f1, p1, s, c)
        mf = mk_fac(f"momentum_factor(-{mom},{p2},size)")
        return wf * mf * q2b * q1v + f"({f2}bar {f1})({p2},{p1},{radius},{mom})"

def mk_pi_0_wf(p1, p2, mom, is_dagger=False):
    """
    i/sqrt(2) * (ubar g5 u - dbar g5 d)  #dag: same
    """
    radius = "r_pi"
    return 1 / sympy.sqrt(2) * (
            mk_meson_wf("u", "u", p1, p2, radius, mom, is_dagger)
            - mk_meson_wf("d", "d", p1, p2, radius, mom, is_dagger)
            ) + f"pi0({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}"

def mk_pi_p_wf(p1, p2, mom, is_dagger=False):
    """
    i ubar g5 d  #dag: i dbar g5 u
    """
    radius = "r_pi"
    return (mk_meson_wf("u", "d", p1, p2, radius, mom, is_dagger)
            + f"pi+({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

def mk_pi_m_wf(p1, p2, mom, is_dagger=False):
    """
    -i dbar g5 u  #dag: -i ubar g5 d
    """
    radius = "r_pi"
    return (-mk_meson_wf("d", "u", p1, p2, radius, mom, is_dagger)
            + f"pi-({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

def mk_sigma_wf(p1, p2, mom, is_dagger=False):
    """
    1/sqrt(2) * (ubar u + dbar d)
    """
    radius = "r_sigma"
    return 1 / sympy.sqrt(2) * (
            mk_scalar_meson_wf("u", "u", p1, p2, radius, mom, is_dagger)
            + mk_scalar_meson_wf("d", "d", p1, p2, radius, mom, is_dagger)
            ) + f"sigma({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}"

def mk_kk_p_wf(p1, p2, mom, is_dagger=False):
    """
    i ubar g5 s  #dag:  i sbar g5 u
    """
    radius = "r_kk"
    return (mk_meson_wf("u", "s", p1, p2, radius, mom, is_dagger)
            + f"K+({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

def mk_kk_m_wf(p1, p2, mom, is_dagger=False):
    """
    -i sbar g5 u  #dag: -i ubar g5 s
    """
    radius = "r_kk"
    return (-mk_meson_wf("s", "u", p1, p2, radius, mom, is_dagger)
            + f"K-({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

def mk_kk_0_wf(p1, p2, mom, is_dagger=False):
    """
    i dbar g5 s  #dag: i sbar g5 d
    """
    radius = "r_kk"
    return (mk_meson_wf("d", "s", p1, p2, radius, mom, is_dagger)
            + f"K0({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

def mk_kk_0_bar_wf(p1, p2, mom, is_dagger=False):
    """
    -i sbar g5 d  #dag: -i dbar g5 s
    """
    radius = "r_kk"
    return (-mk_meson_wf("s", "d", p1, p2, radius, mom, is_dagger)
            + f"K0b({p1},{p2},{radius},{mom}){show_dagger(is_dagger)}")

# ----

all_mom_list_dict = {
        0: [
            q.Coordinate([ 0, 0, 0, 0, ]),
            ],
        1: [
            q.Coordinate([ 0, 0, 1, 0, ]),
            q.Coordinate([ 0, 1, 0, 0, ]),
            q.Coordinate([ 1, 0, 0, 0, ]),
            q.Coordinate([ 0, 0, -1, 0, ]),
            q.Coordinate([ 0, -1, 0, 0, ]),
            q.Coordinate([ -1, 0, 0, 0, ]),
            ],
        2: [
            q.Coordinate([ 0, 1, 1, 0, ]),
            q.Coordinate([ 1, 0, 1, 0, ]),
            q.Coordinate([ 1, 1, 0, 0, ]),
            q.Coordinate([ 0, -1, 1, 0, ]),
            q.Coordinate([ -1, 0, 1, 0, ]),
            q.Coordinate([ -1, 1, 0, 0, ]),
            q.Coordinate([ 0, 1, -1, 0, ]),
            q.Coordinate([ 1, 0, -1, 0, ]),
            q.Coordinate([ 1, -1, 0, 0, ]),
            q.Coordinate([ 0, -1, -1, 0, ]),
            q.Coordinate([ -1, 0, -1, 0, ]),
            q.Coordinate([ -1, -1, 0, 0, ]),
            ],
        3: [
            q.Coordinate([ 1, 1, 1, 0, ]),
            q.Coordinate([ -1, 1, 1, 0, ]),
            q.Coordinate([ 1, -1, 1, 0, ]),
            q.Coordinate([ -1, -1, 1, 0, ]),
            q.Coordinate([ 1, 1, -1, 0, ]),
            q.Coordinate([ -1, 1, -1, 0, ]),
            q.Coordinate([ 1, -1, -1, 0, ]),
            q.Coordinate([ -1, -1, -1, 0, ]),
            ],
        4: [
            q.Coordinate([ 0, 0, 2, 0, ]),
            q.Coordinate([ 0, 2, 0, 0, ]),
            q.Coordinate([ 2, 0, 0, 0, ]),
            q.Coordinate([ 0, 0, -2, 0, ]),
            q.Coordinate([ 0, -2, 0, 0, ]),
            q.Coordinate([ -2, 0, 0, 0, ]),
            ],
        }

def get_mom_list(mom_idx):
    return all_mom_list_dict[mom_idx]

# ----

@q.timer
def get_cexpr_meson_corr_wf():
    fn_base = "cache/auto_contract_cexpr/get_cexpr_meson_corr_wf"
    def calc_cexpr():
        diagram_type_dict = dict()
        def get_mom_avg_expr_list(f):
            """
            f(mom) -> expr
            """
            expr_list = []
            for mom_idx, mom_list in all_mom_list_dict.items():
                expr = 0
                fac = 1 / mk_sym(len(mom_list))
                desp = ""
                for mom in mom_list:
                    e = f(mom)
                    if desp == "":
                        desp = e.description
                    expr += fac * e
                expr = expr + desp
                expr_list.append(expr)
            return expr_list
        exprs = [ mk_fac(1) + f"1", ]
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (-mk_pi_m_wf("y_2", "x_2", -mom) * mk_pi_p_wf("x_1", "y_1", mom))
                )
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (mk_pi_p_wf("x_2", "y_2", mom, True) * mk_pi_p_wf("x_1", "y_1", mom))
                )
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (-mk_kk_m_wf("y_2", "x_2", -mom) * mk_kk_p_wf("x_1", "y_1", mom))
                )
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (mk_kk_p_wf("x_2", "y_2", mom, True) * mk_kk_p_wf("x_1", "y_1", mom))
                )
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (mk_sigma_wf("y_2", "x_2", -mom) * mk_sigma_wf("x_1", "y_1", mom))
                )
        exprs += get_mom_avg_expr_list(
                lambda mom:
                (mk_sigma_wf("x_2", "y_2", mom, True) * mk_sigma_wf("x_1", "y_1", mom))
                )
        cexpr = contract_simplify_compile(
                *exprs,
                is_isospin_symmetric_limit=True,
                diagram_type_dict=diagram_type_dict,
                )
        return cexpr
    return cache_compiled_cexpr(calc_cexpr, fn_base, is_cython=is_cython)

@q.timer_verbose
def auto_contract_meson_corr_wf(job_tag, traj, get_get_prop):
    fname = q.get_fname()
    fn = f"{job_tag}/auto-contract/traj-{traj}/meson_corr_wf.lat"
    if get_load_path(fn) is not None:
        return
    cexpr = get_cexpr_meson_corr_wf()
    expr_names = get_cexpr_names(cexpr)
    total_site = q.Coordinate(get_param(job_tag, "total_site"))
    t_size = total_site[3]
    geo = q.Geometry(total_site, 1)
    total_volume = geo.total_volume()
    get_prop = get_get_prop()
    xg_list = get_all_points(total_site)
    xg_local_list = [ q.Coordinate(xg) for xg in geo.xg_list() ]
    sample_num = get_param(job_tag, "measurement", "auto_contract_meson_corr_wf", "sample_num", default=128)
    sample_size = get_param(job_tag, "measurement", "auto_contract_meson_corr_wf", "sample_size", default=32 * 1024)
    rs = q.RngState(f"{job_tag}-{traj}-{fname}")
    mpi_chunk = get_mpi_chunk(list(range(sample_num)))
    def load_data():
        for idx in mpi_chunk:
            yield idx
    @q.timer
    def feval(args):
        idx = args
        res_list = []
        for idx2 in range(sample_size):
            rsi = rs.split(f"{idx}-{idx2}")
            x_1 = rsi.c_rand_gen(total_site)
            x_2 = rsi.c_rand_gen(total_site)
            y_1 = rsi.c_rand_gen(total_site)
            y_1[3] = x_1[3]
            y_2 = rsi.c_rand_gen(total_site)
            y_2[3] = x_2[3]
            x_2_1_rel = q.smod(x_2 - x_1, total_site)
            t_sep = x_2_1_rel[3]
            pd = {
                    "x_2": ("point", x_2,),
                    "y_2": ("point", y_2,),
                    "x_1": ("point", x_1,),
                    "y_1": ("point", y_1,),
                    "size": total_site,
                    "wave_function": wave_function,
                    "momentum_factor": momentum_factor,
                    "Coordinate": q.Coordinate,
                    "r_pi": 1.5,
                    "r_sigma": 1.5,
                    "r_kk": 2.0,
                    }
            val = eval_cexpr(cexpr, positions_dict=pd, get_prop=get_prop)
            res_list.append((val, t_sep,))
        return res_list
    def sum_function(val_list):
        values = np.zeros((t_size, len(expr_names),), dtype=complex)
        for idx, res_list in enumerate(val_list):
            for val, t_sep, in res_list:
                values[t_sep] += val
            q.displayln_info(f"{fname}: {idx+1}/{len(mpi_chunk)}")
        return q.glb_sum(values.transpose(1, 0,))
    q.timer_fork(0)
    res_sum = q.parallel_map_sum(feval, load_data(), sum_function=sum_function, chunksize=1)
    q.displayln_info(f"{fname}: timer_display for parallel_map_sum")
    q.timer_display()
    q.timer_merge()
    res_sum *= 1.0 / (sample_num * sample_size / t_size)
    # assert q.qnorm(res_sum[0].sum(1) - 1.0) < 1e-10
    ld = q.mk_lat_data([
        [ "expr_name", len(expr_names), expr_names, ],
        [ "t_sep", t_size, [ str(q.rel_mod(t, t_size)) for t in range(t_size) ], ],
        ])
    ld.from_numpy(res_sum)
    ld.save(get_save_path(fn))
    q.displayln_info(f"CHECK: {fname}: ld sig: {q.get_double_sig(ld, q.RngState()):.5E}")

# ----

@q.timer_verbose
def run_job(job_tag, traj):
    #
    traj_gf = 1000 # fix gauge field in checking
    #
    fns_props = [
            (f"{job_tag}/prop-psrc-light/traj-{traj_gf}.qar", f"{job_tag}/prop-psrc-light/traj-{traj_gf}/geon-info.txt",),
            (f"{job_tag}/prop-psrc-strange/traj-{traj_gf}.qar", f"{job_tag}/prop-psrc-strange/traj-{traj_gf}/geon-info.txt",),
            (f"{job_tag}/prop-wsrc-light/traj-{traj_gf}.qar", f"{job_tag}/prop-wsrc-light/traj-{traj_gf}/geon-info.txt",),
            (f"{job_tag}/prop-wsrc-strange/traj-{traj_gf}.qar", f"{job_tag}/prop-wsrc-strange/traj-{traj_gf}/geon-info.txt",),
            (f"{job_tag}/psel-prop-wsrc-light/traj-{traj_gf}.qar", f"{job_tag}/psel-prop-wsrc-light/traj-{traj_gf}/checkpoint.txt",),
            (f"{job_tag}/psel-prop-wsrc-strange/traj-{traj_gf}.qar", f"{job_tag}/psel-prop-wsrc-strange/traj-{traj_gf}/checkpoint.txt",),
            ]
    #
    fns_produce = fns_props + [
            f"{job_tag}/auto-contract/traj-{traj}/checkpoint.txt",
            #
            (f"{job_tag}/configs/ckpoint_lat.{traj_gf}", f"{job_tag}/configs/ckpoint_lat.IEEE64BIG.{traj_gf}",),
            #
            f"{job_tag}/gauge-transform/traj-{traj_gf}.field",
            #
            f"{job_tag}/eig/traj-{traj_gf}",
            f"{job_tag}/eig-strange/traj-{traj_gf}",
            ]
    fns_need = [
            # f"{job_tag}/gauge-transform/traj-{traj}.field",
            # f"{job_tag}/point-selection/traj-{traj}.txt",
            # f"{job_tag}/field-selection/traj-{traj}.field",
            # f"{job_tag}/wall-src-info-light/traj-{traj}.txt",
            # f"{job_tag}/wall-src-info-strange/traj-{traj}.txt",
            # (f"{job_tag}/configs/ckpoint_lat.{traj}", f"{job_tag}/configs/ckpoint_lat.IEEE64BIG.{traj}",),
            ]
    if not check_job(job_tag, traj, fns_produce, fns_need):
        return
    #
    get_gf = run_gf(job_tag, traj_gf)
    get_gt = run_gt(job_tag, traj_gf, get_gf)
    get_gf_ape = run_gf_ape(job_tag, get_gf)
    #
    def run_with_eig():
        get_eig = run_eig(job_tag, traj_gf, get_gf)
        if get_eig is None:
            return
        # run_get_inverter_checker(job_tag, traj_gf, inv_type = 0, get_gf = get_gf, get_gt = get_gt, get_eig = get_eig)
        run_prop_psrc_checker(job_tag, traj_gf, inv_type = 0, get_gf = get_gf, get_eig = get_eig, get_gt = get_gt)
        run_prop_wsrc_checker(job_tag, traj_gf, inv_type = 0, get_gf = get_gf, get_eig = get_eig, get_gt = get_gt)
        q.clean_cache(q.cache_inv)
    #
    def run_with_eig_strange():
        get_eig = run_eig_strange(job_tag, traj_gf, get_gf)
        if get_eig is None:
            return
        # run_get_inverter_checker(job_tag, traj_gf, inv_type = 1, get_gf = get_gf, get_gt = get_gt, get_eig = get_eig)
        run_prop_psrc_checker(job_tag, traj_gf, inv_type = 1, get_gf = get_gf, get_eig = get_eig, get_gt = get_gt)
        run_prop_wsrc_checker(job_tag, traj_gf, inv_type = 1, get_gf = get_gf, get_eig = get_eig, get_gt = get_gt)
        q.clean_cache(q.cache_inv)
    #
    run_with_eig()
    run_with_eig_strange()
    #
    run_r_list(job_tag)
    get_get_prop = run_get_prop_checker(job_tag, traj_gf, get_gf=get_gf, get_gt=get_gt)
    #
    fn_checkpoint = f"{job_tag}/auto-contract/traj-{traj}/checkpoint.txt"
    if get_load_path(fn_checkpoint) is None and get_get_prop is not None:
        if q.obtain_lock(f"locks/{job_tag}-{traj}-auto-contract"):
            q.timer_fork()
            # ADJUST ME
            auto_contract_meson_corr_wf(job_tag, traj, get_get_prop)
            auto_contract_meson_corr_psnk_psrc_rand(job_tag, traj, get_get_prop)
            #
            auto_contract_meson_corr(job_tag, traj_gf, get_get_prop)
            auto_contract_meson_corr_psnk(job_tag, traj_gf, get_get_prop)
            auto_contract_meson_corr_psnk_psrc(job_tag, traj_gf, get_get_prop)
            #
            # q.qtouch_info(get_save_path(fn_checkpoint))
            q.release_lock()
            q.displayln_info("timer_display for runjob")
            q.timer_display()
            q.timer_merge()
            # q.clean_cache()

def get_all_cexpr():
    benchmark_eval_cexpr(get_cexpr_meson_corr())

set_param("test-4nt16", "trajs", value=list(range(1000, 1010)))
set_param("test-4nt16", "mk_sample_gauge_field", "rand_n_step", value=2)
set_param("test-4nt16", "mk_sample_gauge_field", "flow_n_step", value=8)
set_param("test-4nt16", "mk_sample_gauge_field", "hmc_n_traj", value=1)
set_param("test-4nt16", "lanc_params", 0, 0, "cheby_params", value={ "low": 0.45, "high": 5.5, "order": 20, })
set_param("test-4nt16", "lanc_params", 0, 0, "irl_params", value={ "Nstop": 1000, "Nk": 1100, "Nm": 1300, "resid": 1e-8, "betastp": 0.0, "maxiter": 20, "Nminres": 0, })
set_param("test-4nt16", "clanc_params", 0, 0, "nbasis", value=1000)
set_param("test-4nt16", "clanc_params", 0, 0, "block", value=[ 4, 4, 2, 2, ])
set_param("test-4nt16", "clanc_params", 0, 0, "cheby_params", value={ "low": 0.45, "high": 5.5, "order": 20, })
set_param("test-4nt16", "clanc_params", 0, 0, "save_params", value={ "nsingle": 100, "mpi": [ 1, 1, 1, 4, ], })
set_param("test-4nt16", "clanc_params", 0, 0, "irl_params", value={ "Nstop": 1000, "Nk": 1100, "Nm": 1300, "resid": 1e-8, "betastp": 0.0, "maxiter": 20, "Nminres": 0, })
set_param("test-4nt16", "clanc_params", 1, 0, value=get_param("test-4nt16", "clanc_params", 0, 0).copy())
set_param("test-4nt16", "lanc_params", 1, 0, value=get_param("test-4nt16", "lanc_params", 0, 0).copy())
set_param("test-4nt16", "lanc_params", 1, 0, "fermion_params", value=get_param("test-4nt16", "fermion_params", 1, 0).copy())

set_param("test-4nt64", "trajs", value=list(range(1000, 1127)))
set_param("test-4nt64", "lanc_params", 0, 0, "cheby_params", value={ "low": 0.22, "high": 5.5, "order": 30, })
set_param("test-4nt64", "lanc_params", 0, 0, "irl_params", value={ "Nstop": 1000, "Nk": 1100, "Nm": 1300, "resid": 1e-8, "betastp": 0.0, "maxiter": 20, "Nminres": 0, })
set_param("test-4nt64", "clanc_params", 0, 0, "nbasis", value=1000)
set_param("test-4nt64", "clanc_params", 0, 0, "block", value=[ 4, 4, 2, 8, ])
set_param("test-4nt64", "clanc_params", 0, 0, "cheby_params", value={ "low": 0.22, "high": 5.5, "order": 30, })
set_param("test-4nt64", "clanc_params", 0, 0, "save_params", value={ "nsingle": 100, "mpi": [ 1, 1, 1, 4, ], })
set_param("test-4nt64", "clanc_params", 0, 0, "irl_params", value={ "Nstop": 1000, "Nk": 1100, "Nm": 1300, "resid": 1e-8, "betastp": 0.0, "maxiter": 20, "Nminres": 0, })
set_param("test-4nt64", "clanc_params", 1, 0, value=get_param("test-4nt64", "clanc_params", 0, 0).copy())
set_param("test-4nt64", "lanc_params", 1, 0, value=get_param("test-4nt64", "lanc_params", 0, 0).copy())
set_param("test-4nt64", "lanc_params", 1, 0, "fermion_params", value=get_param("test-4nt64", "fermion_params", 1, 0).copy())

qg.begin_with_gpt()

job_tags = [
        "test-4nt16",
        # "test-4nt64",
        ]

q.check_time_limit()

get_all_cexpr()

for job_tag in job_tags:
    q.displayln_info(pprint.pformat(get_param(job_tag)))
    q.displayln_info("CHECK: ", get_param(job_tag))
    for traj in get_param(job_tag, "trajs"):
        run_job(job_tag, traj)

q.timer_display()

q.displayln_info("CHECK: finished successfully.")

qg.end_with_gpt()
