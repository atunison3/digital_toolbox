def unicode_guide() -> None:
    """Print a guide to common Unicode characters for terminal output."""

    sections = {
        "Single-line box drawing": [
            ("─", r"\u2500", "Horizontal"),
            ("│", r"\u2502", "Vertical"),
            ("┌", r"\u250C", "Top-left corner"),
            ("┐", r"\u2510", "Top-right corner"),
            ("└", r"\u2514", "Bottom-left corner"),
            ("┘", r"\u2518", "Bottom-right corner"),
            ("├", r"\u251C", "Left junction"),
            ("┤", r"\u2524", "Right junction"),
            ("┬", r"\u252C", "Top junction"),
            ("┴", r"\u2534", "Bottom junction"),
            ("┼", r"\u253C", "Four-way junction"),
        ],
        "Double-line box drawing": [
            ("═", r"\u2550", "Double horizontal"),
            ("║", r"\u2551", "Double vertical"),
            ("╔", r"\u2554", "Top-left corner"),
            ("╗", r"\u2557", "Top-right corner"),
            ("╚", r"\u255A", "Bottom-left corner"),
            ("╝", r"\u255D", "Bottom-right corner"),
            ("╠", r"\u2560", "Left junction"),
            ("╣", r"\u2563", "Right junction"),
            ("╦", r"\u2566", "Top junction"),
            ("╩", r"\u2569", "Bottom junction"),
            ("╬", r"\u256C", "Four-way junction"),
        ],
        "Rounded corners": [
            ("╭", r"\u256D", "Top-left corner"),
            ("╮", r"\u256E", "Top-right corner"),
            ("╰", r"\u2570", "Bottom-left corner"),
            ("╯", r"\u256F", "Bottom-right corner"),
        ],
        "Heavy box drawing": [
            ("━", r"\u2501", "Heavy horizontal"),
            ("┃", r"\u2503", "Heavy vertical"),
            ("┏", r"\u250F", "Top-left corner"),
            ("┓", r"\u2513", "Top-right corner"),
            ("┗", r"\u2517", "Bottom-left corner"),
            ("┛", r"\u251B", "Bottom-right corner"),
        ],
        "Arrows and status symbols": [
            ("→", r"\u2192", "Right arrow"),
            ("←", r"\u2190", "Left arrow"),
            ("↑", r"\u2191", "Up arrow"),
            ("↓", r"\u2193", "Down arrow"),
            ("⇒", r"\u21D2", "Double right arrow"),
            ("↳", r"\u21B3", "Downward return arrow"),
            ("✓", r"\u2713", "Check mark"),
            ("✔", r"\u2714", "Heavy check mark"),
            ("✗", r"\u2717", "Ballot X"),
            ("✘", r"\u2718", "Heavy ballot X"),
            ("⚠", r"\u26A0", "Warning"),
            ("●", r"\u25CF", "Filled circle"),
            ("○", r"\u25CB", "Empty circle"),
            ("■", r"\u25A0", "Filled square"),
            ("□", r"\u25A1", "Empty square"),
        ],
        "Punctuation": [
            ("—", r"\u2014", "Em dash"),
            ("–", r"\u2013", "En dash"),
            ("•", r"\u2022", "Bullet"),
            ("…", r"\u2026", "Ellipsis"),
            ("·", r"\u00B7", "Middle dot"),
        ],
    }

    table_width = 58

    print("╔" + "═" * table_width + "╗")
    print(f"║{'UNICODE TERMINAL GUIDE':^{table_width}}║")
    print("╚" + "═" * table_width + "╝")

    for section_name, characters in sections.items():
        print()
        print(
            f"┌─ {section_name} "
            + "─"
            * max(
                0,
                table_width - len(section_name) - 3,
            )
            + "┐"
        )

        print(f"│ {'Character':<10}" f"{'Escape':<12}" f"{'Description':<32} │")
        print("├" + "─" * 11 + "┬" + "─" * 12 + "┬" + "─" * 33 + "┤")

        for character, escape, description in characters:
            print(f"│ {character:<10}" f"│ {escape:<10} " f"│ {description:<31} │")

        print("└" + "─" * 11 + "┴" + "─" * 12 + "┴" + "─" * 33 + "┘")

    print()
    print("Example boxes")
    print()

    print("Single line:")
    print("┌──────────────────┐")
    print("│ Database created │")
    print("└──────────────────┘")

    print()
    print("Double line:")
    print("╔══════════════════╗")
    print("║ Database created ║")
    print("╚══════════════════╝")

    print()
    print("Rounded corners:")
    print("╭──────────────────╮")
    print("│ Database created │")
    print("╰──────────────────╯")

    print()
    print("Heavy line:")
    print("┏━━━━━━━━━━━━━━━━━━┓")
    print("┃ Database created ┃")
    print("┗━━━━━━━━━━━━━━━━━━┛")

    print()
    print("Status messages")
    print("✔ Database created")
    print("⚠ Configuration file missing")
    print("✘ Connection failed")
    print("→ Retrying connection")


if __name__ == "__main__":
    unicode_guide()
