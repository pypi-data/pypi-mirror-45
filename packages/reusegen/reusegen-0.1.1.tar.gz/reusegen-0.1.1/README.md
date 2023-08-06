# reusegen

Generators are exhausted during iteration:

```Python
xs = (x * x for x in range(10))
ys = [x + 1 for x in xs]  # [1, 2, ...]
zs = [x + 2 for x in xs]  # []
```

Sometimes this is not expected. With reusegen, you can reuse generators like lists:

```Python
from reusegen import reuse
xs = reuse(x * x for x in range(10))
ys = [x + 1 for x in xs]
zs = [x + 1 for x in xs]
print(ys == zs)  # True
```

And it also works as decorator:

```Python
@reuse
def double(xs):
  for x in xs:
    yield x * 2
```

By default, the results of generator is cached. You could make it cacheless to save memory as original generator:

```Python
xs = reuse(x * x for x in range(10), cache=False)
```

The generator will be executed multiple times.


## TODO

Add cacheless version of `reuse`.
