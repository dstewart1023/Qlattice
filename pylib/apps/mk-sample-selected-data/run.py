#!/usr/bin/env python3

# Need --mpi X.X.X.X runtime option

import qlat as q
import qlat_gpt as qg
import rbc_ukqcd as ru

import os

def get_save_path(fn):
    return os.path.join("results", fn)

def get_n_points(job_tag, traj, inv_type, inv_acc):
    t = [ [ 32, 4, 2 ], [ 16, 4, 2 ] ]
    return t[inv_type][inv_acc]

@q.timer
def mk_sample_gauge_field(job_tag, traj):
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_sample_gauge_field")
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    gf = q.GaugeField(geo)
    gf.set_rand(rs, sigma = 0.25, n_step = 4)
    for i in range(4):
        q.gf_wilson_flow_step(gf, 0.05)
    gf.unitarize()
    return gf

@q.timer
def mk_sample_gauge_transform(job_tag, traj):
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_sample_gauge_transform")
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    gt = q.GaugeTransform(geo)
    gt.set_rand(rs, sigma = 0.2, n_step = 1)
    gt.unitarize()
    return gt

@q.timer
def mk_rand_psel(job_tag, traj):
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_rand_psel")
    total_site = ru.get_total_site(job_tag)
    n_points = get_n_points(job_tag, traj, 0, 0)
    psel = q.PointSelection()
    psel.set_rand(rs, total_site, n_points)
    return psel

@q.timer
def mk_rand_fsel(job_tag, traj):
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_rand_fsel")
    total_site = ru.get_total_site(job_tag)
    n_per_tslice = total_site[0] * total_site[1] * total_site[2] // 16
    fsel = q.FieldSelection()
    fsel.set_rand(rs, total_site, n_per_tslice)
    return fsel

@q.timer
def mk_fselc(fsel, psel):
    fselc = fsel.copy()
    fselc.add_psel(psel)
    return fselc

@q.timer
def mk_rand_wall_src_info(job_tag, traj, inv_type):
    # wi is a list of [ idx tslice inv_type inv_acc ]
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_rand_wall_src_info")
    inv_acc_s = 1
    inv_acc_e = 2
    total_site = ru.get_total_site(job_tag)
    t_size = total_site[3]
    wi_s = [ [ t, inv_type, inv_acc_s ] for t in range(t_size) ]
    n_exact = 2
    mask = [ False ] * t_size
    for i in range(n_exact):
        t_e = rs.rand_gen() % t_size
        mask[t_e] = True
    wi_e = []
    for t in range(t_size):
        if mask[t]:
            wi_e.append([ t, inv_type, inv_acc_e ])
    wi = wi_e + wi_s
    for i in range(len(wi)):
        wi[i] = [ i ] + wi[i]
    return wi

@q.timer
def save_wall_src_info(wi, path):
    # wi is a list of  [ idx tslice inv_type inv_acc ]
    if 0 != q.get_id_node():
        return None
    lines = [ " ".join([ f"{v:5d}" for v in l ]) for l in wi ]
    content = "\n".join(lines + [""])
    q.qtouch(path, content)

@q.timer
def mk_rand_point_src_info(job_tag, traj, psel):
    # pi is a list of [ idx xg inv_type inv_acc ]
    rs = q.RngState(f"seed {job_tag} {traj}").split("mk_rand_point_src_info")
    xg_list = psel.list()
    assert len(xg_list) == get_n_points(job_tag, traj, 0, 0)
    g_pi = [ [] for _ in xg_list ]
    for inv_type in [ 0, 1 ]:
        for inv_acc in [ 0, 1, 2 ]:
            for i in range(get_n_points(job_tag, traj, inv_type, inv_acc)):
                g_pi[i].append([ xg_list[i], inv_type, inv_acc ])
    pi = []
    for g in g_pi:
        pi += g
    for i in range(len(pi)):
        pi[i] = [ i ] + pi[i]
    return pi

@q.timer
def save_point_src_info(pi, path):
    # pi is a list of [ idx xg inv_type inv_acc ]
    if 0 != q.get_id_node():
        return None
    def mk_line(l):
        [ idx, xg, inv_type, inv_acc ] = l
        return f"{idx:5d}    {xg[0]:3d} {xg[1]:3d} {xg[2]:3d} {xg[3]:3d}    {inv_type:3d} {inv_acc:3d}"
    lines = list(map(mk_line, pi))
    content = "\n".join([ f"{len(lines)}" ] + lines + [ "" ])
    q.qtouch(path, content)

@q.timer
def compute_prop(inv, src, *, tag, sfw, fn_sp, psel, fsel, fselc):
    sol = inv * src
    s_sol = sol.sparse(fselc)
    s_sol.save_float_from_double(sfw, tag)
    sp_sol = s_sol.sparse(psel)
    sp_sol.save(fn_sp)

cache = q.mk_cache("app")

cache_inv = q.mk_cache("inv", cache)

@q.timer
def get_inv(gf, job_tag, inv_type, inv_acc, *, gt = None, mpi_split = None, n_grouped = 1):
    tag = f"{job_tag} {inv_type} {inv_acc} {id(gt)} {mpi_split} {n_grouped}"
    if tag in cache_inv:
        return cache_inv[tag]
    inv = ru.mk_inverter(gf, job_tag, inv_type, inv_acc,
            gt = gt,
            mpi_split = mpi_split,
            n_grouped = n_grouped)
    cache_inv[tag] = inv
    return inv

@q.timer
def compute_prop_wsrc(gf, gt, tslice, job_tag, inv_type, inv_acc, *, idx, sfw, path_sp, psel, fsel, fselc):
    tag = f"tslice={tslice} ; type={inv_type} ; accuracy={inv_acc}"
    fn_sp = os.path.join(path_sp, f"{tag}.lat")
    if q.does_file_exist_sync_node(fn_sp):
        return None
    q.check_time_limit()
    q.displayln_info(f"compute_prop_wsrc: idx={idx} tslice={tslice}", job_tag, inv_type, inv_acc)
    inv = get_inv(gf, job_tag, inv_type, inv_acc, gt = gt)
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    src = q.mk_wall_src(geo, tslice)
    compute_prop(inv, src, tag = tag, sfw = sfw, fn_sp = fn_sp, psel = psel, fsel = fsel, fselc = fselc)

@q.timer
def compute_prop_wsrc_all(gf, gt, wi, job_tag, inv_type, *, path_s, path_sp, psel, fsel, fselc):
    sfw = q.open_fields(path_s, "a", [ 1, 1, 1, 4 ])
    for inv_acc in [ 2, 1 ]:
        for p in wi:
            idx, tslice, inv_type_p, inv_acc_p = p
            if inv_type_p == inv_type and inv_acc_p == inv_acc:
                compute_prop_wsrc(gf, gt, tslice, job_tag, inv_type, inv_acc,
                        idx = idx, sfw = sfw, path_sp = path_sp, psel = psel, fsel = fsel, fselc = fselc)
        q.clean_cache(cache_inv)
    sfw.close()

@q.timer
def compute_prop_psrc(gf, xg, job_tag, inv_type, inv_acc, *, idx, sfw, path_sp, psel, fsel, fselc):
    tag = f"xg=({xg[0]},{xg[1]},{xg[2]},{xg[3]}) ; type={inv_type} ; accuracy={inv_acc}"
    fn_sp = os.path.join(path_sp, f"{tag}.lat")
    if q.does_file_exist_sync_node(fn_sp):
        return None
    q.check_time_limit()
    q.displayln_info(f"compute_prop_psrc: idx={idx} xg={xg}", job_tag, inv_type, inv_acc)
    inv = get_inv(gf, job_tag, inv_type, inv_acc)
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    src = q.mk_point_src(geo, xg)
    compute_prop(inv, src, tag = tag, sfw = sfw, fn_sp = fn_sp, psel = psel, fsel = fsel, fselc = fselc)

@q.timer
def compute_prop_psrc_all(gf, pi, job_tag, inv_type, *, path_s, path_sp, psel, fsel, fselc):
    sfw = q.open_fields(path_s, "a", [ 1, 1, 1, 8 ])
    for inv_acc in [ 2, 1, 0 ]:
        for p in pi:
            idx, xg, inv_type_p, inv_acc_p = p
            if inv_type_p == inv_type and inv_acc_p == inv_acc:
                compute_prop_psrc(gf, xg, job_tag, inv_type, inv_acc,
                        idx = idx, sfw = sfw, path_sp = path_sp, psel = psel, fsel = fsel, fselc = fselc)
        q.clean_cache(cache_inv)
    sfw.close()

@q.timer
def check_mk_sample(job_tag, traj):
    # return True if config is finished
    fns = []
    fns.append(get_save_path(f"wall-src-info-light/{job_tag}/traj={traj}.txt"))
    fns.append(get_save_path(f"wall-src-info-strange/{job_tag}/traj={traj}.txt"))
    fns.append(get_save_path(f"point-src-info/{job_tag}/traj={traj}.txt"))
    for fn in fns:
        if not q.does_file_exist_sync_node(fn):
            return False
    return True

@q.timer
def run_mk_sample(job_tag, traj):
    if check_mk_sample(job_tag, traj):
        return
    q.qmkdir_info("locks")
    q.qmkdir_info(get_save_path(f""))
    q.qmkdir_info(get_save_path(f"configs"))
    q.qmkdir_info(get_save_path(f"configs/{job_tag}"))
    q.qmkdir_info(get_save_path(f"gauge-transform"))
    q.qmkdir_info(get_save_path(f"gauge-transform/{job_tag}"))
    q.qmkdir_info(get_save_path(f"point-selection"))
    q.qmkdir_info(get_save_path(f"point-selection/{job_tag}"))
    q.qmkdir_info(get_save_path(f"field-selection"))
    q.qmkdir_info(get_save_path(f"field-selection/{job_tag}"))
    q.qmkdir_info(get_save_path(f"wall-src-info-light"))
    q.qmkdir_info(get_save_path(f"wall-src-info-light/{job_tag}"))
    q.qmkdir_info(get_save_path(f"wall-src-info-strange"))
    q.qmkdir_info(get_save_path(f"wall-src-info-strange/{job_tag}"))
    q.qmkdir_info(get_save_path(f"prop-wsrc-light"))
    q.qmkdir_info(get_save_path(f"prop-wsrc-light/{job_tag}"))
    q.qmkdir_info(get_save_path(f"prop-wsrc-strange"))
    q.qmkdir_info(get_save_path(f"prop-wsrc-strange/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-light"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-light/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-light/{job_tag}/traj={traj}"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-strange"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-strange/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-wsrc-strange/{job_tag}/traj={traj}"))
    q.qmkdir_info(get_save_path(f"point-src-info"))
    q.qmkdir_info(get_save_path(f"point-src-info/{job_tag}"))
    q.qmkdir_info(get_save_path(f"prop-psrc-light"))
    q.qmkdir_info(get_save_path(f"prop-psrc-light/{job_tag}"))
    q.qmkdir_info(get_save_path(f"prop-psrc-strange"))
    q.qmkdir_info(get_save_path(f"prop-psrc-strange/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-light"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-light/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-light/{job_tag}/traj={traj}"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-strange"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-strange/{job_tag}"))
    q.qmkdir_info(get_save_path(f"psel-prop-psrc-strange/{job_tag}/traj={traj}"))
    #
    total_site = ru.get_total_site(job_tag)
    geo = q.Geometry(total_site, 1)
    q.displayln_info("geo.show() =", geo.show())
    #
    gf = mk_sample_gauge_field(job_tag, traj)
    gf.show_info()
    gf.save(get_save_path(f"configs/{job_tag}/ckpoint_lat.{traj}"))
    #
    gt = mk_sample_gauge_transform(job_tag, traj)
    gt.save_double(get_save_path(f"gauge-transform/{job_tag}/traj={traj}.field"))
    #
    psel = mk_rand_psel(job_tag, traj)
    fsel = mk_rand_fsel(job_tag, traj)
    fselc = mk_fselc(fsel, psel)
    psel.save(get_save_path(f"point-selection/{job_tag}/traj={traj}.txt"))
    fsel.save(get_save_path(f"field-selection/{job_tag}/traj={traj}.field"))
    #
    wi_light = mk_rand_wall_src_info(job_tag, traj, inv_type = 0)
    wi_strange = mk_rand_wall_src_info(job_tag, traj, inv_type = 1)
    pi = mk_rand_point_src_info(job_tag, traj, psel)
    #
    if not q.does_file_exist_sync_node(get_save_path(f"wall-src-info-light/{job_tag}/traj={traj}.txt")):
        if q.obtain_lock(f"locks/{job_tag}-{traj}-wsrc-light"):
            compute_prop_wsrc_all(gf, gt, wi_light, job_tag, inv_type = 0,
                    path_s = get_save_path(f"prop-wsrc-light/{job_tag}/traj={traj}"),
                    path_sp = get_save_path(f"psel-prop-wsrc-light/{job_tag}/traj={traj}"),
                    psel = psel, fsel = fsel, fselc = fselc)
            save_wall_src_info(wi_light, get_save_path(f"wall-src-info-light/{job_tag}/traj={traj}.txt"));
            q.release_lock()
    #
    if not q.does_file_exist_sync_node(get_save_path(f"wall-src-info-strange/{job_tag}/traj={traj}.txt")):
        if q.obtain_lock(f"locks/{job_tag}-{traj}-wsrc-strange"):
            compute_prop_wsrc_all(gf, gt, wi_strange, job_tag, inv_type = 1,
                    path_s = get_save_path(f"prop-wsrc-strange/{job_tag}/traj={traj}"),
                    path_sp = get_save_path(f"psel-prop-wsrc-strange/{job_tag}/traj={traj}"),
                    psel = psel, fsel = fsel, fselc = fselc)
            save_wall_src_info(wi_strange, get_save_path(f"wall-src-info-strange/{job_tag}/traj={traj}.txt"));
            q.release_lock()
    #
    if not q.does_file_exist_sync_node(get_save_path(f"point-src-info/{job_tag}/traj={traj}.txt")):
        if q.obtain_lock(f"locks/{job_tag}-{traj}-psrc"):
            compute_prop_psrc_all(gf, pi, job_tag, inv_type = 0,
                    path_s = get_save_path(f"prop-psrc-light/{job_tag}/traj={traj}"),
                    path_sp = get_save_path(f"psel-prop-psrc-light/{job_tag}/traj={traj}"),
                    psel = psel, fsel = fsel, fselc = fselc)
            compute_prop_psrc_all(gf, pi, job_tag, inv_type = 1,
                    path_s = get_save_path(f"prop-psrc-strange/{job_tag}/traj={traj}"),
                    path_sp = get_save_path(f"psel-prop-psrc-strange/{job_tag}/traj={traj}"),
                    psel = psel, fsel = fsel, fselc = fselc)
            save_point_src_info(pi, get_save_path(f"point-src-info/{job_tag}/traj={traj}.txt"));
            q.release_lock()

qg.begin_with_gpt()

for job_tag in [ "test-4nt16" ]:
    for traj in range(1000, 1400, 100):
        run_mk_sample(job_tag, traj)
        q.timer_display()

qg.end_with_gpt()