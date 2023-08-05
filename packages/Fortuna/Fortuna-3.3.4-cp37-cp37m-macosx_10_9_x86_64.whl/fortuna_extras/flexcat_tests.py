from Fortuna import *
from time import time


print("\nFlexCat Test Suite\n")

some_matrix = {
    "A": [lambda: 1, lambda: 2, lambda: 3, lambda: 4, lambda: 5],
    "B": [10, 20, 30, 40, 50],
    "C": [100, 200, 300, 400, 500],
}

str_zero_cool_dispatch = (
    "front_linear", "middle_linear", "back_linear", "quantum_linear",
    "front_gauss", "middle_gauss", "back_gauss", "quantum_gauss",
    "front_poisson", "middle_poisson", "back_poisson", "quantum_poisson",
    "quantum_monty", "flat_uniform",
)
start_FC = time()
for v_bias in str_zero_cool_dispatch:
    for k_bias in str_zero_cool_dispatch:
        f_cat = FlexCat(some_matrix, key_bias=k_bias, val_bias=v_bias)
        distribution_timer(f_cat)
stop_FC = time()


zero_cool_dispatch = (
    front_linear, middle_linear, back_linear, quantum_linear,
    front_gauss, middle_gauss, back_gauss, quantum_gauss,
    front_poisson, middle_poisson, back_poisson, quantum_poisson,
    quantum_monty, random_index,
)
start_fc = time()
for v_bias in zero_cool_dispatch:
    for k_bias in zero_cool_dispatch:
        distribution_timer(flex_cat, some_matrix, key_bias=k_bias, val_bias=v_bias)
stop_fc = time()

print(f"FlexCat Class Battery: {round(stop_FC - start_FC, 3)} sec")
print(f"flex_cat Function Battery: {round(stop_fc - start_fc, 3)} sec")


print("\nUn-flat Tests\n")
f_cat = FlexCat(some_matrix, val_bias="flat_uniform", flat=False)

distribution_timer(f_cat, cat_key="A")
distribution_timer(flex_cat, some_matrix, cat_key="A", flat=False)

distribution_timer(f_cat, cat_key="A", post_processor=lambda x: x())
distribution_timer(flex_cat, some_matrix, cat_key="A", flat=False, post_processor=lambda x: x())
