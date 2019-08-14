import pickle as pkl
from ase.calculators.vasp import Vasp2
import ase
from quantum_valet.valet import AutotuneBandgap
import numpy as np
import signal

bench_set = pkl.load(open('bench_set/matproj_bench_set_clean.pkl','rb'))
bench_results = []

def signal_handler(signum, frame):
    raise Exception("Timed out!")


'''

EDIT THIS STUFF FOR TIMING

'''
##################################################
signal.signal(signal.SIGALRM, signal_handler)
signal.alarm(10)   # Ten seconds

try:
    long_function_call()
except Exception, msg:
    print "Timed out!"
##################################################

for i,key in enumerate(bench_set.keys()):
    bs = bench_set[key]
    sys = bs['structure_initial']
    setup = bs['potcar']

    calc = Vasp2()
    calc.read_incar('../calculators/INCAR.volume_scan')
    calc.set(xc='pbe',setups=setup,kpts=[5.,5.,5.],gamma=True)
    sys.set_calculator(calc)
    valet = AutotuneBandgap(sys,calc,key)
    valet.get_bandgap()
    results = {'bench_bandgap':bench_bandgap,'bench_vol':bench_vol,'bench_sys':bench_sys,'valet_vol':valet_vol,
          'valet_sys':valet_sys,'valet_bandgap':valet.bandgap,'system':key,'valet':valet}
    bench_results.append(results)
    if i%25 == 0:
        print('{} of {}'.format(i,len(bench_set.keys())))
        with open('valet_bench_checkpoint.pkl','wb') as fout:
            pkl.dump(bench_results,fout)        
            print('Checkpoint')

with open('valet_bench_results.pkl','wb') as fout:
    pkl.dump(bench_results,fout)
