# generatecedula
*Python3 module to generate random and verify
uruguay identification document.*

## Installation
### Install with pip
```
pip3 install -U generatecedula
```

## Usage
```
In [1]: import gencedula

In [2]: for x in range(10):
	print(
		gencedula.generate_cedula(
			start=4_000_000,
			stop=5_000_000,
			step=200
			)
		)
46308006
47486005
49378000
41064007
40756005
45282003
47958004
44844000
41564007
49684003
```
