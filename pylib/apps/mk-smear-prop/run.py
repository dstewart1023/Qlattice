#!/usr/bin/env python3

# Need --mpi X.X.X.X --mpi X.X.X runtime option

import qlat_gpt as qg
import rbc_ukqcd as ru

from jobs import *

load_path_list[:] = [
        "results",
        "../mk-gf-gt/results",
        "../mk-sel/results",
        "../mk-lanc/results",
        "../qcddata",
        os.path.join(os.getenv("HOME"), "Qlat-sample-data/mk-gf-gt/results"),
        os.path.join(os.getenv("HOME"), "Qlat-sample-data/mk-sel/results"),
        os.path.join(os.getenv("HOME"), "Qlat-sample-data/mk-lanc/results"),
        os.path.join(os.getenv("HOME"), "qcddata"),
        ]

@q.timer_verbose
def compute_prop(inv, xg_src, *, job_tag, sfw, tag, path_sp, psel, fsel, fselc, psel_smear, gf_ape, gt):
    fn_sp = os.path.join(path_sp, f"{tag}.lat")
    fn_spw = os.path.join(path_sp, f"{tag} ; wsnk.lat")
    fn_sps = os.path.join(path_sp, f"{tag} ; smear-snk.lat")
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    src = q.mk_point_src(geo, xg_src)
    coef = rup.dict_params[job_tag]["prop_smear_coef"]
    step = rup.dict_params[job_tag]["prop_smear_step"]
    src_smear = src.copy()
    q.prop_smear(src_smear, gf_ape, coef, step)
    sol = inv * src_smear
    s_sol = q.SelProp(fselc)
    s_sol @= sol
    s_sol.save_float_from_double(sfw, tag)
    sp_sol = q.PselProp(psel)
    sp_sol @= s_sol
    sp_sol.save(get_save_path(fn_sp))
    sfw.flush()
    sol_gt = gt * sol
    sol_ws = sol_gt.glb_sum_tslice()
    sol_ws.save(get_save_path(fn_spw))
    sol_smear = sol.copy()
    q.prop_smear(sol_smear, gf_ape, coef, step)
    sol_smear_psel = q.PselProp(psel_smear)
    sol_smear_psel @= sol_smear
    sol_smear_psel.save(get_save_path(fn_sps))

@q.timer
def compute_prop_smear(job_tag, xg_src, inv_type, inv_acc, *,
        idx, gf, gt, sfw, path_sp, psel, fsel, fselc, psel_smear, gf_ape, eig, finished_tags):
    xg = xg_src
    xg_str = f"({xg[0]},{xg[1]},{xg[2]},{xg[3]})"
    tag = f"smear ; xg={xg_str} ; type={inv_type} ; accuracy={inv_acc}"
    if tag in finished_tags:
        return None
    q.check_stop()
    q.check_time_limit()
    q.displayln_info(f"compute_prop_smear: {job_tag} idx={idx} tag='{tag}'")
    inv = ru.get_inv(gf, job_tag, inv_type, inv_acc, eig = eig)
    compute_prop(inv, xg_src, job_tag = job_tag, sfw = sfw, tag = tag, path_sp = path_sp,
            psel = psel, fsel = fsel, fselc = fselc,
            psel_smear = psel_smear, gf_ape = gf_ape, gt = gt)

@q.timer_verbose
def compute_prop_smear_all(job_tag, traj, *,
        inv_type, gf, gt, psel, fsel, fselc, psel_smear, gf_ape, eig,
        ):
    inv_type_names = [ "light", "strange", ]
    inv_type_name = inv_type_names[inv_type]
    path_s = f"prop-smear-{inv_type_name}/{job_tag}/traj={traj}"
    path_sp = f"psel-prop-smear-{inv_type_name}/{job_tag}/traj={traj}"
    finished_tags = q.properly_truncate_fields(get_save_path(path_s + ".acc"))
    sfw = q.open_fields(get_save_path(path_s + ".acc"), "a", [ 1, 1, 1, 4, ])
    def comp(idx, xg_src, inv_acc):
        compute_prop_smear(job_tag, xg_src, inv_type, inv_acc,
                idx = idx, gf = gf, gt = gt, sfw = sfw, path_sp = path_sp,
                psel = psel, fsel = fsel, fselc = fselc,
                psel_smear = psel_smear, gf_ape = gf_ape,
                eig = eig, finished_tags = finished_tags)
    prob1 = rup.dict_params[job_tag]["prob_acc_1_smear"]
    prob2 = rup.dict_params[job_tag]["prob_acc_2_smear"]
    rs = q.RngState(f"seed {job_tag} {traj}").split(f"compute_prop_smear_all(ama)")
    for idx, xg_src in enumerate(psel_smear.to_list()):
        r = rs.split(f"{tuple(xg_src)}").u_rand_gen()
        assert 0 <= r and r <= 1
        comp(idx, xg_src, inv_acc = 0)
        if r <= prob1:
            comp(idx, xg_src, inv_acc = 1)
        if r <= prob2:
            comp(idx, xg_src, inv_acc = 2)
    sfw.close()
    q.qtouch_info(get_save_path(os.path.join(path_sp, "checkpoint.txt")))
    q.qrename_info(get_save_path(path_s + ".acc"), get_save_path(path_s))
    q.clean_cache(q.cache_inv)

@q.timer
def run_prop_smear(job_tag, traj, *, inv_type, get_gf, get_gf_ape, get_eig, get_gt, get_psel, get_fsel, get_psel_smear):
    if None in [ get_gf, get_gt, get_gf_ape, get_psel, get_fsel, ]:
        return
    if inv_type == 0 and get_eig is None:
        return
    inv_type_names = [ "light", "strange", ]
    inv_type_name = inv_type_names[inv_type]
    if get_load_path(f"prop-smear-{inv_type_name}/{job_tag}/traj={traj}") is not None:
        return
    if q.obtain_lock(f"locks/{job_tag}-{traj}-smear-{inv_type_name}"):
        gf = get_gf()
        gt = get_gt()
        if get_eig is None:
            eig = None
        else:
            eig = get_eig()
        psel = get_psel()
        fsel, fselc = get_fsel()
        psel_smear = get_psel_smear()
        gf_ape = get_gf_ape()
        compute_prop_smear_all(job_tag, traj,
                inv_type = inv_type, gf = gf, gf_ape = gf_ape, gt = gt, 
                psel = psel, fsel = fsel, fselc = fselc, eig = eig, psel_smear = psel_smear)
        q.release_lock()

@q.timer_verbose
def run_job(job_tag, traj):
    fns_produce = [
            f"prop-smear-light/{job_tag}/traj={traj}",
            f"psel-prop-smear-light/{job_tag}/traj={traj}/checkpoint.txt",
            # f"prop-smear-strange/{job_tag}/traj={traj}",
            # f"psel-prop-smear-strange/{job_tag}/traj={traj}/checkpoint.txt",
            ]
    fns_need = [
            (f"configs/{job_tag}/ckpoint_lat.{traj}", f"configs/{job_tag}/ckpoint_lat.IEEE64BIG.{traj}",),
            f"gauge-transform/{job_tag}/traj={traj}.field",
            f"point-selection/{job_tag}/traj={traj}.txt",
            f"field-selection/{job_tag}/traj={traj}.field",
            f"eig/{job_tag}/traj={traj}",
            f"eig/{job_tag}/traj={traj}/metadata.txt",
            f"eig/{job_tag}/traj={traj}/eigen-values.txt",
            ]
    if not check_job(job_tag, traj, fns_produce, fns_need):
        return
    #
    traj_gf = traj
    if job_tag[:5] == "test-":
        # ADJUST ME
        traj_gf = 1000
        #
    #
    get_gf = run_gf(job_tag, traj_gf)
    get_gt = run_gt(job_tag, traj_gf, get_gf)
    #
    get_psel = run_psel(job_tag, traj)
    get_fsel = run_fsel(job_tag, traj, get_psel)
    assert get_psel is not None
    assert get_fsel is not None
    #
    get_gf_ape = run_gf_ape(job_tag, get_gf)
    #
    get_psel_smear = run_psel_smear(job_tag, traj)
    assert get_psel_smear is not None
    #
    def run_prop(inv_type, get_eig):
        run_prop_smear(job_tag, traj,
                inv_type = inv_type,
                get_gf = get_gf,
                get_gf_ape = get_gf_ape,
                get_eig = get_eig,
                get_gt = get_gt,
                get_psel = get_psel,
                get_fsel = get_fsel,
                get_psel_smear = get_psel_smear,
                )
    #
    def run_with_eig():
        get_eig = run_eig(job_tag, traj_gf, get_gf)
        run_prop(inv_type = 0, get_eig = get_eig)
    #
    run_with_eig()
    #
    # run_prop(inv_type = 1, get_eig = None)
    #
    q.clean_cache()
    q.timer_display()

rup.dict_params["test-4nt8"]["trajs"] = list(range(1000, 1400, 100))
rup.dict_params["test-4nt16"]["trajs"] = list(range(1000, 1400, 100))
rup.dict_params["48I"]["trajs"] = list(range(3000, 500, -5))
rup.dict_params["24D"]["trajs"] = list(range(1000, 10000, 10))
rup.dict_params["16IH2"]["trajs"] = list(range(1000, 10000, 50))
rup.dict_params["32IfineH"]["trajs"] = list(range(1000, 10000, 50))

rup.dict_params["test-4nt8"]["fermion_params"][0][2]["Ls"] = 10
rup.dict_params["test-4nt8"]["fermion_params"][1][2]["Ls"] = 10
rup.dict_params["test-4nt8"]["fermion_params"][2][2]["Ls"] = 10

# rup.dict_params["test-4nt16"]["fermion_params"][0][2]["Ls"] = 10
# rup.dict_params["test-4nt16"]["fermion_params"][1][2]["Ls"] = 10
# rup.dict_params["test-4nt16"]["fermion_params"][2][2]["Ls"] = 10

rup.dict_params["test-4nt8"]["n_exact_wsrc"] = 2
rup.dict_params["48I"]["n_exact_wsrc"] = 2

tag = "prob_exact_wsrc"
rup.dict_params["test-4nt16"][tag] = 1/8
rup.dict_params["16IH2"][tag] = 1/16
rup.dict_params["32IfineH"][tag] = 1/32

tag = "n_per_tslice_smear"
rup.dict_params["test-4nt8"][tag] = 2
rup.dict_params["test-4nt16"][tag] = 2
rup.dict_params["24D"][tag] = 16

tag = "prob_acc_1_smear"
rup.dict_params["test-4nt8"][tag] = 1/4
rup.dict_params["test-4nt16"][tag] = 1/4
rup.dict_params["24D"][tag] = 1/32

tag = "prob_acc_2_smear"
rup.dict_params["test-4nt8"][tag] = 1/16
rup.dict_params["test-4nt16"][tag] = 1/16
rup.dict_params["24D"][tag] = 1/128

tag = "prop_smear_coef"
rup.dict_params["test-4nt8"][tag] = 0.9375
rup.dict_params["test-4nt16"][tag] = 0.9375
rup.dict_params["24D"][tag] = 0.9375

tag = "prop_smear_step"
rup.dict_params["test-4nt8"][tag] = 10
rup.dict_params["test-4nt16"][tag] = 10
rup.dict_params["24D"][tag] = 10

tag = "gf_ape_smear_coef"
rup.dict_params["test-4nt8"][tag] = 0.5
rup.dict_params["test-4nt16"][tag] = 0.5
rup.dict_params["24D"][tag] = 0.5

tag = "gf_ape_smear_step"
rup.dict_params["test-4nt8"][tag] = 30
rup.dict_params["test-4nt16"][tag] = 30
rup.dict_params["24D"][tag] = 30

qg.begin_with_gpt()

# ADJUST ME
job_tags = [
        "test-4nt8", "test-4nt16",
        # "test-8nt16",
        # "test-16nt32",
        # "test-32nt64",
        # "test-48nt96",
        # "test-64nt128",
        # "test-96nt192",
        # "test-128nt256",
        # "24D",
        # "16IH2",
        # "32IfineH",
        # "48I",
        ]

q.check_time_limit()

for job_tag in job_tags:
    q.displayln_info(pprint.pformat(rup.dict_params[job_tag]))
    for traj in rup.dict_params[job_tag]["trajs"]:
        run_job(job_tag, traj)

qg.end_with_gpt()