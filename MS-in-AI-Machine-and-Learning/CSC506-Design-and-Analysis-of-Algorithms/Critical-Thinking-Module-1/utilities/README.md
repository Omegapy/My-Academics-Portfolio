# utilities — Terminal UI Helpers

Reusable Python package providing **console-based UI components** and **input-validation prompts** for terminal applications.

> **Author:** Alexander Ricciardi
> **License:** Apache-2.0

---

## Package Structure

```
CTA-1/utilities/
├── __init__.py                  # Package initializer
├── menu_banner_utilities.py     # Banner & Menu classes
├── validation_utilities.py      # Input-validation prompt functions
└── README.md
```

---

## Modules

### `menu_banner_utilities.py` — Banners & Menus

Provides two classes that render ASCII-bordered UI elements to the console.

#### `Banner`

Renders a box-style banner with configurable alignment, dividers, and auto-expanding width.

```
╔══════════════╗
║  First line  ║
╚══════════════╝
```

| Parameter     | Type                                        | Description                                    |
|---------------|---------------------------------------------|------------------------------------------------|
| `content`     | `Sequence[tuple[str, Alignment, bool]]`     | Lines to display — each tuple is `(text, alignment, is_divider)`. Partial tuples and bare strings are accepted. |
| `inner_width` | `int`                                       | Minimum inner width (auto-expands to fit text) |

**Key methods:**

| Method     | Returns | Description                       |
|------------|---------|-----------------------------------|
| `render()` | `str`   | Builds the full banner as a single string with borders, text lines, and dividers |

---

#### `Menu`

Builds a numbered (or prefix-labeled) console menu using `Banner` under the hood.

```
╔══════════════════════╗
║     Menu Example     ║
╠══════════════════════╣
║ 1. Option            ║
║ 2. Option            ║
║ 3. Option            ║
╚══════════════════════╝
```

| Parameter     | Type                    | Description                                              |
|---------------|-------------------------|----------------------------------------------------------|
| `title`       | `str`                   | Header text displayed at the top of the menu             |
| `options`     | `Sequence[str]`         | List of option labels                                    |
| `inner_width` | `int`                   | Minimum inner width                                      |
| `prefixes`    | `Sequence[str] \| None` | Custom prefixes (e.g., `['a','r','c']`); numbered by default |

**Key methods:**

| Method                  | Returns     | Description                                           |
|-------------------------|-------------|-------------------------------------------------------|
| `render()`              | `str`       | Renders the full menu (title + options) as a banner   |
| `_choices()`            | `list[str]` | Returns choice indices as strings (e.g., `["1","2"]`) |
| `_choice_index_range()` | `str`       | Returns range string (e.g., `"1-3"`)                  |
| `_choice_index_list()`  | `str`       | Returns formatted list (e.g., `"1, 2, or 3"`)        |

---

### `validation_utilities.py` — Input Validation Prompts

A collection of **loop-based prompt functions** that re-ask the user until valid input is provided. Invalid entries display a colored error message (via `colorama`).

| Function                                   | Returns    | Validates                              |
|--------------------------------------------|------------|----------------------------------------|
| `validate_prompt_yes_or_no(prompt)`        | `bool`     | `y/yes` → `True`, `n/no` → `False`    |
| `wait_for_enter()`                         | `None`     | Pauses until Enter is pressed          |
| `validate_prompt_int(prompt)`              | `int`      | Any integer                            |
| `validate_prompt_positive_int(prompt)`     | `int`      | Integer ≥ 0                            |
| `validate_prompt_nonezero_positive_int(prompt)` | `int` | Integer > 0                            |
| `validate_prompt_float(prompt)`            | `float`    | Any float                              |
| `validate_prompt_positive_float(prompt)`   | `float`    | Float ≥ 0.0                            |
| `validate_prompt_nonezero_positive_float(prompt)` | `float` | Float > 0.0                        |
| `validate_prompt_string(prompt)`           | `str`      | Non-empty string                       |
| `validate_prompt_date(prompt, *, formats, normalize_format)` | `str` | Valid date in any accepted format; returns normalized string (e.g., `"February 1, 2020"`) |

---

## Dependencies

| Package    | Purpose                               |
|------------|---------------------------------------|
| `colorama` | Cross-platform colored terminal text  |

---

## Usage

```python
from utilities.menu_banner_utilities import Banner, Menu
from utilities.validation_utilities import (
    validate_prompt_yes_or_no,
    validate_prompt_int,
    validate_prompt_string,
)

# Display a banner
banner = Banner([("Welcome", "center", False)])
print(banner.render())

# Display a menu
menu = Menu("Main Menu", ["Start", "Settings", "Exit"])
print(menu.render())

# Prompt for validated input
name  = validate_prompt_string("Enter your name: ")
count = validate_prompt_int("Enter a number: ")
again = validate_prompt_yes_or_no("Run again?")
```
