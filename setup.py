from quantum_valet.valet import AutotuneBandgap
from ase.calculators.vasp import Vasp2
from ase.io import read
import pickle as pkl

poscar = 'valet_workspace/GaN_804/POSCAR' 
kpts = [4.,4.,4.] 
incar = 'calculators/INCAR.scwf'
potcar_pkl = 'calculators/GaN_potcars.pkl'

atoms = read(poscar) 
potcars = pkl.load(open(potcar_pkl,'rb')) 
calc = Vasp2() 
calc.read_incar(incar) 
calc.set(kpts=kpts,gamma=True) # Gamma must be True for vasp to work in all cases 
atoms.set_calculator(calc)  
