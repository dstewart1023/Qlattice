#!/usr/bin/env python3

import qlat as q

import qlat_gpt as qg
import rbc_ukqcd as ru
import subprocess

qg.begin_with_gpt()

job_tag = "test-4nt8"
traj = 1000

q.qremove_all_info("results")
q.qmkdir_info("results")

total_site = ru.get_total_site(job_tag)
geo = q.Geometry(total_site, 1)
q.displayln_info("geo.show() =", geo.show())
rs = q.RngState(f"seed-{job_tag}-{traj}")

gf = q.GaugeField(geo)
gf.set_rand(rs.split("gf-init"), 0.05, 2)
gf.unitarize()
gf.show_info()

gt = qg.gauge_fix_coulomb(gf)

n_per_tslice_smear = 8
fsel_smear = q.FieldSelection(total_site, n_per_tslice_smear, rs)
psel_smear = fsel_smear.to_psel()

n_points = 256
psel = q.PointSelection()
psel.set_rand(rs, total_site, n_points)

n_per_tslice = 16
fsel = q.FieldSelection()
fsel.set_rand(rs, total_site, n_per_tslice)

fselc = fsel.copy()
fselc.add_psel(psel)

gf_ape = gf.copy()
q.gf_spatial_ape_smear(gf_ape, 0.5, 30)
gf_ape = q.mk_left_expanded_gauge_field(gf_ape)

inv_type = 1
inv_acc = 0

inv = ru.mk_inverter(gf, job_tag, inv_type, inv_acc, n_grouped = q.get_num_node())

xg = psel_smear.to_list()[0]

tag = f"smear ; xg={tuple(xg)} ; type={inv_type} ; accuracy={inv_acc}"

q.displayln_info(tag)
src = q.mk_point_src(geo, xg)

q.displayln_info(f"qnorm(src) = {q.qnorm(src)}")

smear_coef = 0.9375
smear_step = 10
q.prop_smear(src, gf_ape, smear_coef, smear_step)

q.displayln_info(f"qnorm(src) = {q.qnorm(src)} after smear")

sol = inv * src

q.displayln_info(f"qnorm(sol) = {q.qnorm(sol)}")

sol_psel = q.PselProp(psel)
sol_psel @= sol
sol_psel.save(f"results/{tag} ; psnk.lat")

q.displayln_info(f"qnorm(sol_psel) = {q.qnorm(sol_psel)}")

sfw = q.open_fields("results/prop-smear", "w", [ 1, 1, 2, 4, ])

sol_s = q.SelProp(fselc)
sol_s @= sol

q.displayln_info(f"qnorm(sol_s) = {q.qnorm(sol_s)}")

sol_s.save_float_from_double(sfw, f"{tag}")

sfw.close()

sol_gt = gt * sol

sol_ws = sol_gt.glb_sum_tslice()
sol_ws.save(f"results/{tag} ; wsnk.lat")

q.displayln_info(f"qnorm(sol_ws) = {q.qnorm(sol_ws)}")

sol_smear_psel = q.PselProp(psel_smear)

sol_smear = sol.copy()

q.prop_smear(sol_smear, gf_ape, smear_coef, smear_step)

q.displayln_info(f"qnorm(sol_smear) = {q.qnorm(sol_smear)}")

sol_smear_psel = q.PselProp(psel_smear)
sol_smear_psel @= sol_smear
sol_smear_psel.save(f"results/{tag} ; smear-snk.lat")

q.displayln_info(f"qnorm(sol_smear_psel) = {q.qnorm(sol_smear_psel)}")

if q.get_id_node() == 0:
    subprocess.run("find results -type f | sort | xargs -n 1 -d '\n' md5sum", shell=True)

q.timer_display()

q.displayln_info(f"CHECK: finished successfully.")

qg.end_with_gpt()
