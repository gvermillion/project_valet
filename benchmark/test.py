import pickle as pkl
from ase.calculators.vasp import Vasp2
import ase
from quantum_valet.valet import AutotuneBandgap
import numpy as np

bench_set = pkl.load(open('bench_set/matproj_bench_set_clean.pkl','rb'))
key = 'mp-804'
bs = bench_set[key]

sys = bs['structure_initial']
setup = bs['potcar']
calc = Vasp2()
calc.read_incar('../calculators/INCAR.volume_scan')
calc.set(xc='pbe',setups=setup,kpts=[5.,5.,5.],gamma=True)
sys.set_calculator(calc)
valet = AutotuneBandgap(sys,calc,key)
valet.get_bandgap()


bench_sys = bs['structure_final']
bench_vol = bench_sys.get_volume()
bench_bandgap = bs['bandgap']

valet_vol = valet.system.get_volume()
valet_sys = valet.system.copy()


results = {'bench_bandgap':bench_bandgap,'bench_vol':bench_vol,'bench_sys':bench_sys,'valet_vol':valet_vol,
          'valet_sys':valet_sys,'valet_bandgap':valet.bandgap,'valet_bandgap_direct':valet.bandgap_direct}



print(results)
