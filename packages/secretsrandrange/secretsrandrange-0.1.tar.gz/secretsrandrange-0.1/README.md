# secretsrandrange
*Implementation of randrange using secrets.*

## Installation
### Install with pip
```
pip3 install -U secretsrandrange
```

secretsrandrange.randrange(
	start:int,
	stop=typing.Union[int, NoneType],
	step:int=1
		) -> int
    Return a randomly selected element from range(start, stop, step).
    This is equivalent to choice(range(start, stop, step)),
    but doesn’t actually build a range object.
    :param start: int: Start number.
    :param stop: Stop number. (Default value = Optional[int])
    :param step: int: Step (Default value = 1)
