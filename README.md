# pyjs
JavaScript parser and interpreter written in python

```python
import pyjs

tree = pyjs.parse("console.log('hello, world')")
```

## JS support state

- [x] assignments
- [x] function calls with any number of arguments
- [ ] if-else blocks
- [ ] loops
- [x] named `function` definitions
- [ ] anonymous `function` definitions
- [ ] arrow function definitions
- [ ] string templates
- [ ] async functions