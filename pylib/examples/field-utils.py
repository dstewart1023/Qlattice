#!/usr/bin/env python3

import sys
import qlat as q
import numpy as np

size_node_list = [
    [1, 1, 1, 1],
    [1, 1, 1, 2],
    [1, 1, 1, 4],
    [1, 1, 1, 8],
    [2, 2, 2, 2],
    [2, 2, 2, 4]]

q.begin(sys.argv, size_node_list)

q.qremove_all_info("results")
q.qmkdir_info("results")

total_site = [4, 4, 4, 8]
geo = q.Geometry(total_site, 1)
q.displayln_info("geo.show() =", geo.show())
rs = q.RngState("seed")

gf = q.GaugeField(geo)

gf.set_rand(rs.split("gf-init"), 0.3, 1)

gf.show_info()

fft_f = q.mk_fft(True, is_normalizing = True)
fft_b = q.mk_fft(False, is_normalizing = True)

gfm = fft_f * gf

gf1 = fft_b * gfm

gf1.show_info()

f_factor = q.mk_phase_field(gf.geo(), [1, 0, 0, 0,])

gf *= f_factor

gf.show_info()

q.displayln_info(gf.get_elems([0, 0, 0, 0,]))

gf_sum_initial = gf.glb_sum()

gf_sum = gf_sum_initial.copy()

q.displayln_info(gf_sum)

gf_sum_tslice = gf.glb_sum_tslice()

for t in range(total_site[3]):
    gf_sum -= gf_sum_tslice.get_elems(t)

q.displayln_info(q.qnorm(gf_sum))

assert q.qnorm(gf_sum) <= 1e-16

qnorm = q.qnorm(gf_sum_tslice.to_numpy())
q.displayln_info(f"CHECK: t_dir=3 (default) qnorm(gf_sum_tslice)={qnorm:.14E}")

for t_dir in range(4):
    gf_sum_tslice = gf.glb_sum_tslice(t_dir = t_dir)
    n_points = gf_sum_tslice.n_points()
    multiplicity = gf_sum_tslice.multiplicity()
    psel_list = gf_sum_tslice.psel.to_list()
    q.displayln_info(f"CHECK: t_dir={t_dir} n_points={n_points} multiplicity={multiplicity} psel_list={psel_list}")
    qnorm = q.qnorm(gf_sum_tslice.to_numpy())
    q.displayln_info(f"CHECK: t_dir={t_dir} qnorm(gf_sum_tslice)={qnorm:.14E}")
    gf_sum = gf_sum_initial.copy()
    for t in range(total_site[t_dir]):
        gf_sum -= gf_sum_tslice.get_elems(t)
    q.displayln_info(f"t_dir={t_dir} qnorm diff", q.qnorm(gf_sum))
    assert q.qnorm(gf_sum) <= 1e-16

f = gf.as_complex_field()

q.displayln_info(f.get_elems([0, 0, 0, 0,]))

gf1 = q.GaugeField()

gf1.from_complex_field(f)

gf1 -= gf

q.displayln_info("diff norm", gf1.qnorm())

n_per_tslice = 16
fsel = q.FieldSelection(geo.total_site(), n_per_tslice, rs.split("fsel"))

prop = q.Prop(geo)
prop.set_rand(rs.split("prop-1"))
s_prop = q.SelProp(fsel)
s_prop @= prop
prop @= s_prop

sum_tslice1 = prop.glb_sum_tslice()

sum_tslice2 = s_prop.glb_sum_tslice()

sum_tslice = sum_tslice1.copy()
sum_tslice -= sum_tslice2

q.displayln_info(f"{sum_tslice1.qnorm()} {sum_tslice2.qnorm()} {sum_tslice.qnorm()}")

gf_vec = [ q.mk_merged_fields_ms([ (gf, m,), ]) for m in range(4) ]

gf1 = q.GaugeField()

gf1 @= q.mk_merged_fields_ms([ (gf_vec[m], 0) for m in range(4) ])

gf1.show_info()

gf2 = q.GaugeField()

gf2 @= q.mk_merged_fields_ms([ (gf, m) for m in range(4) ])

gf2.show_info()

q.timer_display()

q.displayln_info(f"CHECK: finished successfully.")

q.end()
