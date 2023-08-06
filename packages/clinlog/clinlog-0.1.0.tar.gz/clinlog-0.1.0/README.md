# clinlog

[![PyPI version](https://badge.fury.io/py/clinlog.svg)](https://badge.fury.io/py/clinlog)
[![PyPI version](https://img.shields.io/github/license/salpreh/clinlog.svg)](https://img.shields.io/github/license/salpreh/clinlog.svg)

**Package to easily log styled messages on console using [colorama](https://github.com/tartley/colorama)**

---
## Basic usage
Create a `Logger` object and use his convenient methods to print styled messages in console. You can define a default tag for each kind of message on the `Logger` instance.

### Print style methods
- `print_error()`
- `print_warn()`
- `print_info()`
- `print_confirm()`
- `print_norm()`

The signature for all print methods are the same:
1. **message _(str)_**: Message to print.
2. **tag _(str)_**: (Optional) Prefix to print with the message. If `None` the default tag for this kind of messages is used. An empty string will remove the tag for this print.
3. **bold _(bool)_**: (Optional) `True` to use bright style to print the message (kind of bold font). By default `False`.
4. **highlight _(bool)_**: `True` to use the color on the background and a high contrast color for the message text.
5. **invert_color _(bool)_**: `True` to invert font color when highlight flag is on, this will switch between black and white. By default `False`.

### Default print tag attributes
- `error_tag`
- `warn_tag`
- `info_tag`
- `confirm_tag`
- `norm_tag`

### Code Sample
```py
from clinlog import Logger

# Create the logger
log = Logger()

# Set default error tag
log.error_tag = '[ERROR]: '

# Print error styled message
log.print_error('Unable to access config file', bold=True)

# Print warning highlighted and bold
log.print_warn('The execution will continue with default configuration', None, True, True)

# Confirmation log with provided tag
log.print_confirm('Execution completed', '[SUCCESS]')
```

### Output
<img src="https://raw.githubusercontent.com/salpreh/clinlog/master/assets/output.png" alt="tree_output">

### Different styes sample
<img src="https://raw.githubusercontent.com/salpreh/clinlog/master/assets/sample.png" alt="tree_output">
