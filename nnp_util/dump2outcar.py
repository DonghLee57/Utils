import sys
import numpy as np

dump_file_name = sys.argv[1]
target = int(sys.argv[2])
step =1
c=0
tag=0
with open(dump_file_name) as dump:
	print("generated by convert_to_outcar.py (from lammps dump file)")
	for iteration, line in enumerate(dump):
		if "TIMESTEP" in line:
			if int(next(dump)) % step == 0:
				c += 1
				if c == target:
					next(dump)
					natoms = int(next(dump))
					next(dump)
					xb = np.fromstring(next(dump), sep=" ")
					yb = np.fromstring(next(dump), sep=" ")
					zb = np.fromstring(next(dump), sep=" ")
					next(dump)
					if xb.size > 2:
						xy = xb[2]
						xz = yb[2]
						yz = zb[2]
						xlo = xb[0] - min([0, xy, xz, xy+xz])
						xhi = xb[1] - max([0, xy, xz, xy+xz])
						ylo = yb[0] - min([0, yz])
						yhi = yb[1] - max([0, yz])
						zlo = zb[0]
						zhi = zb[1]
					else:
						xlo, xhi = xb
						ylo, yhi = yb
						zlo, zhi = zb
						xy = xz = yz = 0
					if tag == 0:
						print(" POTCAR:    PAW_PBE Ge 05Jan2001")
						print(" POTCAR:    PAW_PBE Te 05Jan2001\n")
						print(" POTCAR:    PAW_PBE Ge 05Jan2001")
						print(" POTCAR:    PAW_PBE Te 05Jan2001\n")
						print("   ions per type =          48 48\n")
						print("      direct lattice vectors                 reciprocal lattice vectors")
						print(f"  {xhi-xlo:>11.6f} {0:>11.6f} {0:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}")
						print(f"  {xy:>11.6f} {yhi-ylo:>11.6f} {0:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}")
						print(f"  {xz:>11.6f} {yz:>11.6f} {zhi-zlo:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}\n")

					print(f"Iteration      {iteration+1}")
					print("      direct lattice vectors                 reciprocal lattice vectors")
					print(f"  {xhi-xlo:>11.6f} {0:>11.6f} {0:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}")
					print(f"  {xy:>11.6f} {yhi-ylo:>11.6f} {0:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}")
					print(f"  {xz:>11.6f} {yz:>11.6f} {zhi-zlo:>11.6f}  {0:>11.6f} {0:>11.6f} {0:>11.6f}\n")
					print(" POSITION                                       TOTAL-FORCE (eV/Angst)")
					print(" -----------------------------------------------------------------------------------")
					pe = 0
					sort_list =[]
					for _ in range(natoms):
						sort_list.append(next(dump).split())
					sort_list.sort(key=lambda x:int(x[0]))
					for xxx in range(natoms):
						sp = sort_list[xxx]
						x = float(sp[2])
						y = float(sp[3])
						z = float(sp[4])
					# while x >= xb[1]-xb[0]:
						# x -= xb[1]-xb[0]
					# while x < 0:
						# x += xb[1]-xb[0]
					# while y >= yb[1]-yb[0]:
						# y -= yb[1]-yb[0]
					# while y < 0:
						# y += yb[1]-yb[0]
					# while z >= zb[1]-zb[0]:
						# z -= zb[1]-zb[0]
					# while z < 0:
						# z += zb[1]-zb[0]
						fx = 0.0
						fy = 0.0
						fz = 0.0
	#					pe += float(sp[7])
						print(f" {x:>13.5f} {y:>13.5f} {z:>13.5f}    {fx:>13.5f} {fy:>13.5f} {fz:>13.5f}")
					print(" -----------------------------------------------------------------------------------")
					print(" -----------------------------------------------------------------------------------")
					print(" FREE ENERGIE OF THE ION-ELECTRON SYSTEM (eV)")
					print(" -----------------------------------------------------------------------------------")
					print(f"  free  energy   TOTEN  = {pe:>18.8f} eV\n")
					print("  energy without entropy= 0 energy(sigma->0) = 0\n\n")
