import html
import re


def format_html_preview(text: str) -> str:

    escaped = html.escape(text)

    lines = escaped.splitlines()

    output = []

    for line in lines:

        stripped = line.strip()

        if not stripped:
            output.append("<br>")
            continue

        # Main title
        if (
            len(stripped) < 100
            and stripped.upper() == stripped
            and len(stripped.split()) <= 12
        ):
            output.append(
                f"<h2>{stripped}</h2>"
            )

        # Numbered clauses
        elif re.match(
            r"^\d+[\.\)]\s+",
            stripped
        ):
            output.append(
                f"<p><strong>{stripped}</strong></p>"
            )

        # Bullets
        elif stripped.startswith("- "):
            output.append(
                f"<p>• {stripped[2:]}</p>"
            )

        else:
            output.append(
                f"<p>{stripped}</p>"
            )

    return "\n".join(output)
