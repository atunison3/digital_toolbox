from collections.abc import Iterable
from pathlib import Path


def print_project_tree(
    root: str | Path = ".",
    *,
    ignore: Iterable[str] = (
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".DS_Store",
        "*.pyc",
        "*.pyo",
        "*.egg-info",
        "dist",
        "build",
        ".idea",
        ".vscode",
    ),
    max_depth: int | None = None,
) -> None:
    """
    Print a fancy Unicode directory tree of the project.
    """
    root = Path(root).resolve()
    ignore_set = set(ignore)

    def should_ignore(path: Path) -> bool:
        name = path.name
        if name in ignore_set:
            return True
        # simple glob-style support for patterns like *.pyc
        for pattern in ignore_set:
            if pattern.startswith("*.") and name.endswith(pattern[1:]):
                return True
        return False

    def tree(dir_path: Path, prefix: str = "", depth: int = 0) -> None:
        if max_depth is not None and depth > max_depth:
            return

        try:
            entries = sorted(
                [p for p in dir_path.iterdir() if not should_ignore(p)],
                key=lambda p: (not p.is_dir(), p.name.lower()),
            )
        except PermissionError:
            return

        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "└── " if is_last else "├── "
            print(prefix + connector + entry.name)

            if entry.is_dir():
                extension = "    " if is_last else "│   "
                tree(entry, prefix + extension, depth + 1)

    print(root.name + "/")
    tree(root)


# ------------------------------------------------------------------
# Usage examples
# ------------------------------------------------------------------
if __name__ == "__main__":
    print_project_tree()  # current directory
    # print_project_tree("accounting")            # specific folder
    # print_project_tree(max_depth=2)             # limit depth
