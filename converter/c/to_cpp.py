def convert(code):
    lines = code.split("\n")
    result = []

    result.append("#include <iostream>")
    result.append("using namespace std;")
    result.append("")
    result.append("int main() {")

    indent_level = 1

    for raw_line in lines:

        # Remove inline comments
        if "//" in raw_line:
            raw_line = raw_line.split("//")[0]

        stripped = raw_line.strip()

        if not stripped:
            continue

        # Skip C includes and main
        if stripped.startswith("#include") or "int main" in stripped:
            continue

        # Handle closing brace first
        if stripped == "}":
            indent_level -= 1
            continue

        # Detect opening brace
        open_brace = False
        if stripped.endswith("{"):
            open_brace = True
            stripped = stripped[:-1].strip()

        indentation = "    " * indent_level

        # ------------------------
        # printf → cout
        # ------------------------
        if stripped.startswith("printf"):
            inside = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            parts = inside.split(",")

            if len(parts) == 2:
                text = parts[0].strip().strip('"')
                var = parts[1].strip()

                text = text.replace("%d", "")
                text = text.replace("%f", "")

                stripped = f'cout << "{text}" << {var} << endl;'
            else:
                stripped = f"cout << {inside} << endl;"

        # Remove return 0 (we add our own)
        if "return 0" in stripped:
            continue

        result.append(indentation + stripped)

        # Increase indent after opening brace
        if open_brace:
            result.append(indentation + "{")
            indent_level += 1

    result.append("    return 0;")
    result.append("}")

    return "\n".join(result)