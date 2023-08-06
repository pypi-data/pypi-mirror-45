from Fortuna import *
from time import time


some_array = tuple(i for i in range(11))

print("\nQuantum Monty Methods:\n")
start_QM = time()
monty = QuantumMonty(some_array)
distribution_timer(monty.flat_uniform)
distribution_timer(monty.front_linear)
distribution_timer(monty.middle_linear)
distribution_timer(monty.back_linear)
distribution_timer(monty.quantum_linear)
distribution_timer(monty.front_gauss)
distribution_timer(monty.middle_gauss)
distribution_timer(monty.back_gauss)
distribution_timer(monty.quantum_gauss)
distribution_timer(monty.front_poisson)
distribution_timer(monty.middle_poisson)
distribution_timer(monty.back_poisson)
distribution_timer(monty.quantum_poisson)
distribution_timer(monty.quantum_monty)
stop_QM = time()

print("\nLazy Cat: Functional, More General Form of QuantumMonty:\n")
start_LC = time()
distribution_timer(lazy_cat, some_array, zero_cool=random_index)
distribution_timer(lazy_cat, some_array, zero_cool=front_linear)
distribution_timer(lazy_cat, some_array, zero_cool=middle_linear)
distribution_timer(lazy_cat, some_array, zero_cool=back_linear)
distribution_timer(lazy_cat, some_array, zero_cool=quantum_linear)
distribution_timer(lazy_cat, some_array, zero_cool=front_gauss)
distribution_timer(lazy_cat, some_array, zero_cool=middle_gauss)
distribution_timer(lazy_cat, some_array, zero_cool=back_gauss)
distribution_timer(lazy_cat, some_array, zero_cool=quantum_gauss)
distribution_timer(lazy_cat, some_array, zero_cool=front_poisson)
distribution_timer(lazy_cat, some_array, zero_cool=middle_poisson)
distribution_timer(lazy_cat, some_array, zero_cool=back_poisson)
distribution_timer(lazy_cat, some_array, zero_cool=quantum_poisson)
distribution_timer(lazy_cat, some_array, zero_cool=quantum_monty)
stop_LC = time()

print("\nStatic Slicing:")
monty = QuantumMonty(some_array[:5])            # this copies data
distribution_timer(monty.flat_uniform)          # range from the front

monty = QuantumMonty(some_array[-5:])           # must recreate for new slice, copies data again.
distribution_timer(monty.flat_uniform)          # range from the back


print("\nDynamic Slicing:")                     # this does never copies data
distribution_timer(lazy_cat, some_array, 5)     # equivalent to
distribution_timer(lazy_cat, some_array[:5])    # range from the front

distribution_timer(lazy_cat, some_array, -5)    # equivalent to
distribution_timer(lazy_cat, some_array[-5:])   # range from the back


def zero_cool_by_2(x):
    return random_range(x, step=2)


print("\nCustom ZeroCool Method:")
distribution_timer(zero_cool_by_2, 11)          # -> [0, 10] by 2, even values
distribution_timer(zero_cool_by_2, -11)         # -> [-1, -11] by 2, odd values

print("\nLazy Cat with Custom ZeroCool Method:")
distribution_timer(lazy_cat, some_array, zero_cool=zero_cool_by_2)
distribution_timer(lazy_cat, some_array, 5, zero_cool=zero_cool_by_2)  # even positive index [0, 4] by 2
distribution_timer(lazy_cat, some_array, -5, zero_cool=zero_cool_by_2)  # odd negative index [-5, -1] by 2

print("\nZeroCool Lambda, same as zero_cool_by_2(x)")
distribution_timer(lazy_cat, some_array, zero_cool=lambda x: random_range(x, step=2))


QM, LC = round(stop_QM - start_QM, 3), round(stop_LC - start_LC, 3)
print(f"QuantumMonty Class: {QM} sec")
print(f"LazyCat Function: {LC} sec")
