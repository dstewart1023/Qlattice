#!/usr/bin/env python3

import sys
import math as m
import numpy as np

import qlat as q

@q.timer_verbose
def gm_evolve_fg(gm, gf_init, ga, fg_dt, dt):
    geo = gf_init.geo()
    gf = q.GaugeField(geo)
    gf @= gf_init
    #
    gm_force = q.GaugeMomentum(geo)
    #
    q.set_gm_force(gm_force, gf, ga)
    #
    q.gf_evolve(gf, gm_force, fg_dt)
    #
    q.set_gm_force(gm_force, gf, ga)
    #
    q.display_gm_force_magnitudes(gm_force, 5)
    q.displayln_info(q.get_gm_force_magnitudes(gm_force, 5))
    #
    gm_force *= dt
    gm += gm_force

@q.timer_verbose
def run_hmc_evolve(gm, gf, ga, rs, steps, md_time = 1.0):
    energy = q.gm_hamilton_node(gm) + q.gf_hamilton_node(gf, ga)
    #
    dt = md_time / steps
    lam = 0.5 * (1.0 - 1.0 / m.sqrt(3.0));
    theta = (2.0 - m.sqrt(3.0)) / 48.0;
    ttheta = theta * dt * dt * dt;
    #
    q.gf_evolve(gf, gm, lam * dt)
    #
    for i in range(steps):
        gm_evolve_fg(gm, gf, ga, 4.0 * ttheta / dt, 0.5 * dt);
        q.gf_evolve(gf, gm, (1.0 - 2.0 * lam) * dt);
        gm_evolve_fg(gm, gf, ga, 4.0 * ttheta / dt, 0.5 * dt);
        if i < steps - 1:
            q.gf_evolve(gf, gm, 2.0 * lam * dt);
        else:
            q.gf_evolve(gf, gm, lam * dt);
    #
    q.unitarize(gf)
    #
    delta_h = q.gm_hamilton_node(gm) + q.gf_hamilton_node(gf, ga) - energy;
    delta_h = q.glb_sum(delta_h)
    #
    return delta_h

@q.timer_verbose
def metropolis_accept(delta_h, traj, rs):
    flag_d = 0.0
    accept_prob = 0.0
    if q.get_id_node() == 0:
        if delta_h <= 0.0:
            accept_prob = 1.0
            flag_d = 1.0
        else:
            accept_prob = m.exp(-delta_h)
            rand_num = rs.u_rand_gen(1.0, 0.0)
            if rand_num <= accept_prob:
                flag_d = 1.0
    flag_d = q.glb_sum(flag_d)
    accept_prob = q.glb_sum(accept_prob)
    flag = flag_d > 0.5
    q.displayln_info("metropolis_accept: flag={:d} with accept_prob={:.1f}% delta_h={:.16f} traj={:d}".format(
        flag, accept_prob * 100.0, delta_h, traj))
    return flag, accept_prob

@q.timer_verbose
def run_hmc(gf, ga, traj, rs):
    #
    is_reverse_test = traj < 3
    #
    geo = gf.geo()
    gf0 = q.GaugeField(geo)
    gf0 @= gf
    #
    gm = q.GaugeMomentum(geo)
    gm.set_rand(rs.split("set_rand_gauge_momentum"), 1.0)
    #
    steps = 6
    md_time = 1.0
    #
    delta_h = run_hmc_evolve(gm, gf0, ga, rs, steps, md_time)
    #
    if is_reverse_test:
        gm_r = q.GaugeMomentum(geo)
        gm_r @= gm
        gf0_r = q.GaugeField(geo)
        gf0_r @= gf0
        delta_h_rev = run_hmc_evolve(gm_r, gf0_r, ga, rs, steps, -md_time)
        gf0_r -= gf;
        q.displayln_info("run_hmc_evolve reversed delta_diff: {} / {}".format(delta_h + delta_h_rev, delta_h))
        q.displayln_info("run_hmc_evolve reversed gf_diff: {} / {}".format(q.qnorm(gf0_r), q.qnorm(gf0)))
    #
    flag, accept_prob = metropolis_accept(delta_h, traj, rs.split("metropolis_accept"))
    #
    if flag or traj <= 20:
        q.displayln_info("run_hmc: update gf (traj={:d})".format(traj))
        gf @= gf0

@q.timer_verbose
def test_hmc(total_site, ga):
    #
    q.qmkdir_info("results");
    q.qmkdir_info("results/gf_info");
    q.qmkdir_info("results/wilson_flow_energy_info");
    q.qmkdir_info("results/gm_force_info");
    #
    geo = q.Geometry(total_site, 1)
    rs = q.RngState("test_hmc-{}x{}x{}x{}".format(total_site[0], total_site[1], total_site[2], total_site[3]))
    gf = q.GaugeField(geo)
    q.set_unit(gf);
    traj = 0
    for i in range(4):
        traj += 1
        run_hmc(gf, ga, traj, rs.split("hmc-{}".format(traj)))
        plaq_avg = q.gf_avg_plaq(gf)
        plaq_sum = np.prod(total_site) * 6.0 * (1.0 - plaq_avg)
        q.displayln_info(f"CHECK: traj={traj} ; plaq_avg={plaq_avg:.14E}")
        wilson_loop = q.gf_avg_wilson_loop_normalized_tr(gf, 1, 1)
        q.displayln_info(f"CHECK: wilson_loop {wilson_loop:.14E}")
        if traj % 2 == 0:
            q.display_gauge_field_info_table_with_wilson_flow(
                    "results/gf_info/traj={}.lat".format(traj),
                    "results/wilson_flow_energy_info/traj={}.lat".format(traj),
                    gf, 0.1, 5, 2)
            q.save_gm_force_magnitudes_list(
                    "results/gm_force_info/traj={}.lat".format(traj))

@q.timer_verbose
def main():
    total_site = [4, 4, 4, 8]
    ga = q.GaugeAction(2.13, -0.331)
    test_hmc(total_site, ga)
    ga = q.GaugeAction(5.5, 0.0)
    test_hmc(total_site, ga)

size_node_list = [
        [1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 1, 1, 4],
        [1, 2, 2, 2],
        [2, 2, 2, 2],
        [2, 2, 2, 4]]

q.begin(sys.argv, size_node_list)

# q.show_machine()

q.qremove_all_info("results")

main()

q.timer_display()

q.displayln_info(f"CHECK: finished successfully.")

q.end()
