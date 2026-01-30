# Mojo stdlib

Just a copy of https://github.com/modular/modular/tree/main/mojo/stdlib for reference

## Syncing

To sync the stdlib and docs from the modular submodule:

```bash
uv run sync_stdlib.py
```

Or directly:

```bash
./sync_stdlib.py
```

This script will:
1. Update the git submodule
2. Copy `modular/mojo/stdlib` and `modular/mojo/docs` to `mojo/stdlib` and `mojo/docs` (deleting existing copies first)
3. Make a git commit with the changes
