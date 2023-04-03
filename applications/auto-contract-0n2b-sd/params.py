from rbc_ukqcd_params import dict_params

tag = "trajs"
dict_params["test-4nt8"][tag] = list(range(1000, 1400, 100))
dict_params["test-4nt16"][tag] = list(range(1000, 1400, 100))
dict_params["48I"][tag] = list(range(2175, 2000, -1)) + list(range(500, 3000, 5))
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
# ADJUST ME
dict_params["48I"][tag] = 1024
#
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

tag = "meson_tsep_list"
dict_params["test-4nt8"][tag] = list(range(1, 8))
dict_params["test-4nt16"][tag] = list(range(2, 16, 2))
dict_params["24D"][tag] = list(range(4, 64, 4))
dict_params["32D"][tag] = list(range(4, 64, 4))
dict_params["32Dfine"][tag] = list(range(4, 64, 4))
dict_params["24DH"][tag] = list(range(4, 64, 4))
dict_params["48I"][tag] = list(range(4, 96, 4))
dict_params["64I"][tag] = list(range(4, 128, 4))
