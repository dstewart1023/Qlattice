#!/usr/bin/env python3

json_results = []
check_eps = 1e-14

def json_results_append(*args):
    q.displayln_info(r"//------------------------------------------------------------\\")
    q.displayln_info(-1, *args)
    q.displayln_info(r"\\------------------------------------------------------------//")
    json_results.append(args)

import sys
import numpy as np
import qlat as q

import auto_contractor as qac

size_node_list = [
        [1, 1, 1, 1],
        [1, 1, 1, 2],
        [1, 1, 1, 4],
        [1, 1, 1, 8],
        [2, 2, 2, 2],
        [2, 2, 2, 4],
        ]

q.begin_with_mpi(size_node_list)

f1 = "u"
f2 = "s"

p1 = "x1"
s1 = "s1"
c1 = "c1"

p2 = "x2"
s2 = "s2"
c2 = "c2"

p3 = "x3"

q1v = qac.Qv(f1, p1, s1, c1)
q2b = qac.Qb(f2, p2, s2, c2)

exprs = [
    qac.mk_expr(1),
    q1v * q2b * qac.mk_scalar(f1, f2, p3),
    q1v * q2b * qac.mk_scalar5(f1, f2, p3),
    q1v * q2b * qac.mk_vec_mu(f1, f2, p3, 3),
    q1v * q2b * qac.mk_vec5_mu(f1, f2, p3, 3),
]

for expr in exprs:
    json_results_append(str(expr))

for expr in qac.contract_simplify(*exprs):
    json_results_append(str(expr))

cexpr = qac.contract_simplify_compile(*exprs)

json_results_append(
    qac.display_cexpr(cexpr)
)

for v in cexpr.list():
    json_results_append(str(v))

json_results_append(f"qac.get_diagram_type_dict(cexpr) = {qac.get_diagram_type_dict(cexpr)}")

cexpr_opt = cexpr.copy()
cexpr_opt.optimize()

json_results_append(
    qac.display_cexpr(cexpr_opt)
)

for v in cexpr_opt.list():
    json_results_append(str(v))

json_results_append(f"qac.get_diagram_type_dict(cexpr) = {qac.get_diagram_type_dict(cexpr_opt)}")

@q.timer
def get_cexpr_test(is_cython=False):
    fn_base = f"cache/auto_contract_cexpr/get_cexpr_test"
    def calc_cexpr():
        cexpr = qac.contract_simplify_compile(*exprs, is_isospin_symmetric_limit=True)
        return cexpr
    return qac.cache_compiled_cexpr(calc_cexpr, fn_base, is_cython=is_cython)

for is_cython in [ False, True, ]:
    json_results_append(
        qac.cexpr_code_gen_py(cexpr_opt, is_cython=is_cython)
    )
    ccexpr = get_cexpr_test(is_cython=is_cython)
    json_results_append(f"qac.get_diagram_type_dict(ccexpr) = {qac.get_diagram_type_dict(ccexpr)}")
    check, check_ama = qac.benchmark_eval_cexpr(ccexpr)
    json_results_append(f"get_cexpr_test benchmark_eval_cexpr check get_data_sig is_cython={is_cython}", q.get_data_sig(np.array(check, dtype=np.complex128), q.RngState()))
    json_results_append(f"get_cexpr_test benchmark_eval_cexpr check_ama get_data_sig is_cython={is_cython}", q.get_data_sig(np.array(check_ama, dtype=np.complex128), q.RngState()))

def get_prop(flavor, p1, p2):
    tag = f"get_prop({flavor!r},{p1!r},{p2!r})"
    q.displayln_info(f"Call {tag}")
    rs = q.RngState(tag)
    wm = qac.make_rand_spin_color_matrix(rs)
    assert isinstance(wm, q.WilsonMatrix)
    return wm

wm1 = get_prop(
    "l",
    ("point-snk", q.Coordinate([ 1, 2, 3, 4, ]),),
    ("point", q.Coordinate([ 3, 7, 2, 1, ]),),
)

wm2 = get_prop(
    "s",
    ("point", q.Coordinate([ 3, 7, 2, 1, ]),),
    ("point-snk", q.Coordinate([ 3, 7, 2, 1, ]),),
)

# S_l(x1,x3)*S_s(x3,x2)

wm = q.mat_mul_wm_wm(wm1, wm2)

json_results_append(f"get_prop wm: {q.get_data_sig(wm, q.RngState())}")
q.displayln_info(-1, f"{wm}")

pd = {
    "x1": ("point-snk", q.Coordinate([ 1, 2, 3, 4, ]),),
    "x2": ("point-snk", q.Coordinate([ 3, 7, 2, 1, ]),),
    "x3": ("point", q.Coordinate([ 3, 7, 2, 1, ]),),
}

res = qac.eval_cexpr(ccexpr=get_cexpr_test(), positions_dict=pd, get_prop=get_prop)

for idx, v in enumerate(res):
    json_results_append(f"eval_cexpr res[{idx}]: {q.get_data_sig(v, q.RngState())}")
    q.displayln_info(-1, f"{v}")

q.check_log_json(__file__, json_results, check_eps=check_eps)

q.timer_display()

q.end_with_mpi()

q.displayln_info(f"CHECK: finished successfully.")
