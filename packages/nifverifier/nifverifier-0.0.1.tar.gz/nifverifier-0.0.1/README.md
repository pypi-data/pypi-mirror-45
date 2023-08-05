# NIF PT Verify and Create python package

This is a simple package to verify and create new NIF (Número Identificação Fiscal) in Portugal.

You can install the package using pip

```
pip install nifverifier
```

The solo contributor for this package is the geek, gentle, innocent and kind-hearted CharlieBrown

How to use this package: 

```python
from nifverifier import am_i_a_dead_ass_valid_nif, generate_dead_ass_valid_nif

invalid_nif = "123123123"
valid_nif = "216860180"

am_i_a_dead_ass_valid_nif(invalid_nif) # false
am_i_a_dead_ass_valid_nif(valid_nif) # true

# Lets generate a valid NIF
# Valid initials values are: "1, 2, 3, 5, 6, 8, 9"
generate_dead_ass_valid_nif(initial_value=1)
generate_dead_ass_valid_nif(initial_value=4) # Raise exception


```