# gill

Utilities for interacting with the GIL.

```python
from gill import locked_gil


with locked_gil():
    # No pre-emption from other threads.
```

# development

```
poetry install
poetry build
poetry publish
```
