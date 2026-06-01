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

        # Skip includes and namespace
        if line.startswith("#include") or line.startswith("using namespace"):
            continue

        # Skip main declaration
        if "int main" in line:
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

        # Remove C++ types
        types = ["int", "double", "float", "char", "string", "bool"]
        for t in types:
            if line.startswith(t + " "):
                line = line.replace(t, "", 1).strip()

        # ---------------- PRINT ----------------
        if "cout <<" in line:
            content = line.replace("cout <<", "").replace("<< endl", "").strip()
            line = f"print({content})"

        # ---------------- INPUT ----------------
        elif "cin >>" in line:
            var = line.replace("cin >>", "").strip()
            line = f"{var} = int(input())"

        # ---------------- IF ----------------
        elif line.startswith("if"):
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

            init = parts[0].replace("int", "").strip()
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