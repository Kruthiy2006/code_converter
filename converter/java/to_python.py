def convert(code):
    lines = code.split("\n")
    result = []
    indent_level = 0

    for raw_line in lines:

        # Remove comments
        if "//" in raw_line:
            raw_line = raw_line.split("//")[0]

        line = raw_line.strip()

        if not line:
            continue

        # Skip package/import
        if line.startswith("package") or line.startswith("import"):
            continue

        # Skip class declaration
        if line.startswith("public class"):
            continue

        # Skip main declaration
        if "public static void main" in line:
            continue

        # Handle closing brace
        if line == "}":
            indent_level -= 1
            continue

        # Handle opening brace
        open_brace = False
        if line.endswith("{"):
            open_brace = True
            line = line[:-1].strip()

        # Remove semicolon
        line = line.replace(";", "")

        # ---------------- PRINT ----------------
        if "System.out.println" in line:
            inside = line[line.find("(")+1 : line.rfind(")")]
            line = f"print({inside})"

        # ---------------- VARIABLE TYPES REMOVE ----------------
        types = ["int", "double", "float", "char", "String", "boolean"]
        for t in types:
            if line.startswith(t + " "):
                line = line.replace(t, "", 1).strip()

        # ---------------- IF ----------------
        if line.startswith("if"):
            condition = line[line.find("(")+1 : line.rfind(")")]
            line = f"if {condition}:"

        # ---------------- ELSE IF ----------------
        elif line.startswith("else if"):
            condition = line[line.find("(")+1 : line.rfind(")")]
            line = f"elif {condition}:"

        # ---------------- ELSE ----------------
        elif line.startswith("else"):
            line = "else:"

        # ---------------- WHILE ----------------
        elif line.startswith("while"):
            condition = line[line.find("(")+1 : line.rfind(")")]
            line = f"while {condition}:"

        # ---------------- FOR ----------------
        elif line.startswith("for"):
            inside = line[line.find("(")+1 : line.rfind(")")]
            parts = inside.split(";")

            init = parts[0].strip().replace("int", "").strip()
            var, start = init.split("=")
            var = var.strip()
            start = start.strip()

            condition = parts[1].strip()

            if "<=" in condition:
                end = int(condition.split("<=")[1].strip()) + 1
            elif "<" in condition:
                end = condition.split("<")[1].strip()
            elif ">=" in condition:
                end = int(condition.split(">=")[1].strip()) - 1
            else:
                end = condition.split(">")[1].strip()

            line = f"for {var} in range({start}, {end}):"

        result.append("    " * indent_level + line)

        if open_brace:
            indent_level += 1

    return "\n".join(result)