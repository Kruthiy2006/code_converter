def convert(code):
    lines = code.split("\n")
    result = []

    result.append("public class Main {")
    result.append("    public static void main(String[] args) {")

    indent_level = 2

    for raw_line in lines:

        # Remove inline comments
        if "//" in raw_line:
            raw_line = raw_line.split("//")[0]

        stripped = raw_line.strip()

        if not stripped:
            continue

        # Skip includes and main and return
        if stripped.startswith("#include") or "int main" in stripped or "return 0" in stripped:
            continue

        # Handle closing brace FIRST
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
        # Remove C data types
        # ------------------------
        types = ["int", "float", "double", "char"]
        for t in types:
            if stripped.startswith(t + " "):
                stripped = stripped.replace(t, "", 1).strip()

        # ------------------------
        # PRINTF → System.out.println
        # ------------------------
        if stripped.startswith("printf"):
            inside = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            parts = inside.split(",")

            if len(parts) == 2:
                text = parts[0].strip().strip('"')
                var = parts[1].strip()

                # Replace %d and %f
                text = text.replace("%d", '" + ' + var + ' + "')
                text = text.replace("%f", '" + ' + var + ' + "')

                stripped = f'System.out.println("{text}");'
            else:
                stripped = f"System.out.println({inside});"

        # ------------------------
        # IF
        # ------------------------
        elif stripped.startswith("if"):
            condition = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            stripped = f"if({condition})"

        # ELSE IF
        elif stripped.startswith("else if"):
            condition = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            stripped = f"else if({condition})"

        # WHILE
        elif stripped.startswith("while"):
            condition = stripped[stripped.find("(")+1 : stripped.rfind(")")]
            stripped = f"while({condition})"

        # Remove trailing semicolon
        stripped = stripped.replace(";", "")

        # Add line
        result.append(indentation + stripped)

        # Increase indent AFTER appending
        if open_brace:
            result.append(indentation + "{")
            indent_level += 1

    # Close class properly
    result.append("    }")
    result.append("}")

    return "\n".join(result)