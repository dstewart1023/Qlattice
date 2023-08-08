from .rbc_ukqcd_params import dict_params
from .rbc_ukqcd_params import set_param, get_param

tag = "trajs"
dict_params["test-4nt8"][tag] = list(range(1000, 1400, 100))
dict_params["test-4nt16"][tag] = list(range(1000, 1400, 100))
dict_params["48I"][tag] = list(range(2300, 500, -1))
dict_params["64I"][tag] = list(range(500, 6000, 10))
dict_params["24D"][tag] = list(range(5100, 1000, -10))
dict_params["32D"][tag] = list(range(500, 3000, 10))
dict_params["32Dfine"][tag] = list(range(500, 3000, 10))
dict_params["24DH"][tag] = list(range(200, 1000, 10))
dict_params["16IH2"][tag] = list(range(1000, 10000, 10))
dict_params["32IfineH"][tag] = list(range(1000, 10000, 10))
dict_params["32IcoarseH1"][tag] = list(range(300, 2000, 10))
dict_params["24IH1"][tag] = list(range(1000, 10000, 10))
dict_params["24IH2"][tag] = list(range(1000, 10000, 10))
dict_params["24IH3"][tag] = list(range(1000, 10000, 10))
dict_params["24IH4"][tag] = list(range(1000, 10000, 10))
dict_params["32IH1"][tag] = list(range(1000, 10000, 10))
dict_params["32IH2"][tag] = list(range(1000, 10000, 10)) + list(range(1002, 10000, 10))
dict_params["32IH3"][tag] = list(range(1000, 10000, 10))

tag = "n_points_psel"
dict_params["test-4nt8"][tag] = 6
dict_params["test-4nt16"][tag] = 32
dict_params["48I"][tag] = 2048 # Summit data 2022
# dict_params["48I"][tag] = 1024 # Mira data 2020
dict_params["64I"][tag] = 1024
dict_params["24D"][tag] = 1024
dict_params["32D"][tag] = 2048
dict_params["32Dfine"][tag] = 1024
dict_params["24DH"][tag] = 1024
dict_params["32IfineH"][tag] = 512
dict_params["32IcoarseH1"][tag] = 512
dict_params["16IH2"][tag] = 256
dict_params["24IH3"][tag] = 512
dict_params["24IH2"][tag] = 512
dict_params["24IH1"][tag] = 512
dict_params["32IH1"][tag] = 512
dict_params["32IH2"][tag] = 512
dict_params["32IH3"][tag] = 512

tag = "n_exact_wsrc"
dict_params["test-4nt8"][tag] = 2

tag = "prob_exact_wsrc"
dict_params["test-4nt16"][tag] = 1/8
dict_params["16IH2"][tag] = 1/16
dict_params["48I"][tag] = 1/48
dict_params["64I"][tag] = 1/64
dict_params["24D"][tag] = 1/32
dict_params["32D"][tag] = 1/32
dict_params["32Dfine"][tag] = 1/32
dict_params["24DH"][tag] = 1/32
dict_params["32IfineH"][tag] = 1/32
dict_params["32IcoarseH1"][tag] = 1/32
dict_params["24IH1"][tag] = 1/32
dict_params["24IH2"][tag] = 1/32
dict_params["24IH3"][tag] = 1/32
dict_params["32IH1"][tag] = 1/32
dict_params["32IH2"][tag] = 1/32
dict_params["32IH3"][tag] = 1/32

tag = "n_per_tslice_smear"
dict_params["test-4nt8"][tag] = 2
dict_params["test-4nt16"][tag] = 2
dict_params["48I"][tag] = 10
dict_params["64I"][tag] = 8
dict_params["24D"][tag] = 16
dict_params["32D"][tag] = 32
dict_params["32Dfine"][tag] = 16
dict_params["24DH"][tag] = 16
dict_params["16IH2"][tag] = 8
dict_params["32IfineH"][tag] = 8
dict_params["32IcoarseH1"][tag] = 8
dict_params["24IH1"][tag] = 8
dict_params["24IH2"][tag] = 8
dict_params["24IH3"][tag] = 8
dict_params["32IH1"][tag] = 8
dict_params["32IH2"][tag] = 8
dict_params["32IH3"][tag] = 8

tag = "prob_acc_1_smear"
dict_params["test-4nt8"][tag] = 1/4
dict_params["test-4nt16"][tag] = 1/4
dict_params["48I"][tag] = 1/32
dict_params["64I"][tag] = 1/32
dict_params["24D"][tag] = 1/32
dict_params["32D"][tag] = 1/32
dict_params["32Dfine"][tag] = 1/32
dict_params["24DH"][tag] = 1/32
dict_params["16IH2"][tag] = 1/16
dict_params["32IfineH"][tag] = 1/32
dict_params["32IcoarseH1"][tag] = 1/32
dict_params["24IH1"][tag] = 1/32
dict_params["24IH2"][tag] = 1/32
dict_params["32IH2"][tag] = 1/32
dict_params["32IH1"][tag] = 1/32

tag = "prob_acc_2_smear"
dict_params["test-4nt8"][tag] = 1/16
dict_params["test-4nt16"][tag] = 1/16
dict_params["48I"][tag] = 1/128
dict_params["64I"][tag] = 1/128
dict_params["24D"][tag] = 1/128
dict_params["32D"][tag] = 1/128
dict_params["32Dfine"][tag] = 1/128
dict_params["24DH"][tag] = 1/128
dict_params["16IH2"][tag] = 1/64
dict_params["32IfineH"][tag] = 1/128
dict_params["32IcoarseH1"][tag] = 1/128
dict_params["24IH1"][tag] = 1/128
dict_params["24IH2"][tag] = 1/128
dict_params["32IH2"][tag] = 1/128
dict_params["32IH1"][tag] = 1/128

tag = "prob_acc_1_psrc"
dict_params["test-4nt8"][tag] = 1/4
dict_params["test-4nt16"][tag] = 1/4
dict_params["48I"][tag] = 1/32
dict_params["64I"][tag] = 1/32
dict_params["24D"][tag] = 1/32
dict_params["32D"][tag] = 1/32
dict_params["32Dfine"][tag] = 1/32
dict_params["24DH"][tag] = 1/32
dict_params["16IH2"][tag] = 1/16
dict_params["32IfineH"][tag] = 1/32
dict_params["32IcoarseH1"][tag] = 1/32
dict_params["24IH1"][tag] = 1/32
dict_params["24IH2"][tag] = 1/32
dict_params["24IH3"][tag] = 1/32
dict_params["32IH1"][tag] = 1/32
dict_params["32IH2"][tag] = 1/32

tag = "prob_acc_2_psrc"
dict_params["test-4nt8"][tag] = 1/16
dict_params["test-4nt16"][tag] = 1/16
dict_params["48I"][tag] = 1/128
dict_params["64I"][tag] = 1/128
dict_params["24D"][tag] = 1/128
dict_params["32D"][tag] = 1/128
dict_params["32Dfine"][tag] = 1/128
dict_params["24DH"][tag] = 1/128
dict_params["16IH2"][tag] = 1/64
dict_params["32IfineH"][tag] = 1/128
dict_params["32IcoarseH1"][tag] = 1/128
dict_params["24IH1"][tag] = 1/128
dict_params["24IH2"][tag] = 1/128
dict_params["24IH3"][tag] = 1/128
dict_params["32IH1"][tag] = 1/128
dict_params["32IH2"][tag] = 1/128

tag = "n_rand_u1_fsel"
dict_params["test-4nt8"][tag] = 4
dict_params["test-4nt16"][tag] = 4
dict_params["24D"][tag] = 64
dict_params["32D"][tag] = 64
dict_params["32Dfine"][tag] = 64
dict_params["24DH"][tag] = 64
dict_params["48I"][tag] = 64
dict_params["64I"][tag] = 64
dict_params["16IH2"][tag] = 16
dict_params["32IfineH"][tag] = 64
dict_params["32IcoarseH1"][tag] = 64
dict_params["24IH1"][tag] = 64
dict_params["24IH2"][tag] = 64
dict_params["24IH3"][tag] = 64
dict_params["32IH1"][tag] = 64
dict_params["32IH2"][tag] = 64

tag = "prob_acc_1_rand_u1"
dict_params["test-4nt8"][tag] = 1/4
dict_params["test-4nt16"][tag] = 1/4
dict_params["48I"][tag] = 1/32
dict_params["64I"][tag] = 1/32
dict_params["24D"][tag] = 1/32
dict_params["32D"][tag] = 1/32
dict_params["32Dfine"][tag] = 1/32
dict_params["24DH"][tag] = 1/32
dict_params["16IH2"][tag] = 1/16
dict_params["32IfineH"][tag] = 1/32
dict_params["32IcoarseH1"][tag] = 1/32
dict_params["24IH1"][tag] = 1/32
dict_params["24IH2"][tag] = 1/32
dict_params["24IH3"][tag] = 1/32
dict_params["32IH1"][tag] = 1/32
dict_params["32IH2"][tag] = 1/32

tag = "prob_acc_2_rand_u1"
dict_params["test-4nt8"][tag] = 1/16
dict_params["test-4nt16"][tag] = 1/16
dict_params["48I"][tag] = 1/128
dict_params["64I"][tag] = 1/128
dict_params["24D"][tag] = 1/128
dict_params["32D"][tag] = 1/128
dict_params["32Dfine"][tag] = 1/128
dict_params["24DH"][tag] = 1/128
dict_params["16IH2"][tag] = 1/64
dict_params["32IfineH"][tag] = 1/128
dict_params["32IcoarseH1"][tag] = 1/128
dict_params["24IH1"][tag] = 1/128
dict_params["24IH2"][tag] = 1/128
dict_params["24IH3"][tag] = 1/128
dict_params["32IH1"][tag] = 1/128
dict_params["32IH2"][tag] = 1/128

tag = "prop_smear_coef"
dict_params["test-4nt8"][tag] = 0.9375
dict_params["test-4nt16"][tag] = 0.9375
dict_params["64I"][tag] = 0.9375
dict_params["48I"][tag] = 0.9375
dict_params["24D"][tag] = 0.9375
dict_params["32Dfine"][tag] = 0.9375
dict_params["24DH"][tag] = 0.9375
dict_params["16IH2"][tag] = 0.9375
dict_params["32IfineH"][tag] = 0.9375
dict_params["32IcoarseH1"][tag] = 0.9375
dict_params["24IH1"][tag] = 0.9375
dict_params["24IH2"][tag] = 0.9375
dict_params["24IH3"][tag] = 0.9375
dict_params["32IH1"][tag] = 0.9375
dict_params["32IH2"][tag] = 0.9375

tag = "prop_smear_step"
dict_params["test-4nt8"][tag] = 10
dict_params["test-4nt16"][tag] = 10
dict_params["24D"][tag] = 10
dict_params["24DH"][tag] = 10
dict_params["32Dfine"][tag] = 18
dict_params["48I"][tag] = 29
dict_params["64I"][tag] = 54
dict_params["16IH2"][tag] = 31
dict_params["32IfineH"][tag] = 96
dict_params["32IcoarseH1"][tag] = 31
dict_params["24IH1"][tag] = 31
dict_params["24IH2"][tag] = 31
dict_params["24IH3"][tag] = 31
dict_params["32IH1"][tag] = 55
dict_params["32IH2"][tag] = 55

tag = "gf_ape_smear_coef"
dict_params["test-4nt8"][tag] = 0.5
dict_params["test-4nt16"][tag] = 0.5
dict_params["48I"][tag] = 0.5
dict_params["64I"][tag] = 0.5
dict_params["24D"][tag] = 0.5
dict_params["32Dfine"][tag] = 0.5
dict_params["24DH"][tag] = 0.5
dict_params["16IH2"][tag] = 0.5
dict_params["32IfineH"][tag] = 0.5
dict_params["32IcoarseH1"][tag] = 0.5
dict_params["24IH1"][tag] = 0.5
dict_params["24IH2"][tag] = 0.5
dict_params["24IH3"][tag] = 0.5
dict_params["32IH1"][tag] = 0.5
dict_params["32IH2"][tag] = 0.5

tag = "gf_ape_smear_step"
dict_params["test-4nt8"][tag] = 30
dict_params["test-4nt16"][tag] = 30
dict_params["48I"][tag] = 30
dict_params["64I"][tag] = 30
dict_params["24D"][tag] = 30
dict_params["32Dfine"][tag] = 30
dict_params["24DH"][tag] = 30
dict_params["16IH2"][tag] = 30
dict_params["32IfineH"][tag] = 30
dict_params["32IcoarseH1"][tag] = 30
dict_params["24IH1"][tag] = 30
dict_params["24IH2"][tag] = 30
dict_params["24IH3"][tag] = 30
dict_params["32IH1"][tag] = 30
dict_params["32IH2"][tag] = 30

tag = "fermion_params"
dict_params["test-4nt8"][tag][0][2]["Ls"] = 10
dict_params["test-4nt8"][tag][1][2]["Ls"] = 10
dict_params["test-4nt8"][tag][2][2]["Ls"] = 10
# dict_params["test-4nt16"][tag][0][2]["Ls"] = 10
# dict_params["test-4nt16"][tag][1][2]["Ls"] = 10
# dict_params["test-4nt16"][tag][2][2]["Ls"] = 10

tag = "meson_tensor_tsep"
dict_params["test-4nt8"][tag] = 1
dict_params["test-4nt16"][tag] = 2
dict_params["24D"][tag] = 8
dict_params["32D"][tag] = 8
dict_params["32Dfine"][tag] = 10
dict_params["24DH"][tag] = 8
dict_params["16IH2"][tag] = 6
dict_params["32IfineH"][tag] = 12
dict_params["32IcoarseH1"][tag] = 6
dict_params["24IH1"][tag] = 6
dict_params["24IH2"][tag] = 6
dict_params["24IH3"][tag] = 6
dict_params["32IH1"][tag] = 8
dict_params["32IH2"][tag] = 8
dict_params["48I"][tag] = 12
dict_params["64I"][tag] = 18

tag = "meson_jwjj_threshold"
dict_params["test-4nt8"][tag] = 0.1
dict_params["test-4nt16"][tag] = 0.5
dict_params["24D"][tag] = 0.4
dict_params["32D"][tag] = 0.1
dict_params["32Dfine"][tag] = 0.1
dict_params["24DH"][tag] = 0.02
dict_params["16IH2"][tag] = 0.01
dict_params["32IfineH"][tag] = 0.001
dict_params["32IcoarseH1"][tag] = 0.005
dict_params["24IH1"][tag] = 0.01
dict_params["24IH2"][tag] = 0.01
dict_params["24IH3"][tag] = 0.01
dict_params["32IH1"][tag] = 0.002
dict_params["32IH2"][tag] = 0.002
dict_params["48I"][tag] = 0.01
dict_params["64I"][tag] = 0.01

tag = "meson_tsep_list"
dict_params["test-4nt8"][tag] = list(range(1, 8))
dict_params["test-4nt16"][tag] = list(range(2, 16, 2))
dict_params["24D"][tag] = list(range(4, 64, 4))
dict_params["32D"][tag] = list(range(4, 64, 4))
dict_params["32Dfine"][tag] = list(range(6, 64, 4))
dict_params["24DH"][tag] = list(range(4, 64, 4))
dict_params["48I"][tag] = list(range(4, 96, 4))
dict_params["64I"][tag] = list(range(6, 128, 4))
