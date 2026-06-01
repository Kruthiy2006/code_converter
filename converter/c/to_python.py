def convert(code):

    lines = code.split("\n")
    result = []
    indent = 0

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Skip includes and main
        if line.startswith("#include") or "int main" in line:
            continue

        if "return 0" in line:
            continue

        # Closing brace
        if line == "}":
            indent -= 1
            continue

        # Remove data types
        for t in ["int", "float", "double", "char"]:
            if line.startswith(t + " "):
                line = line.replace(t, "").strip()

        # FOR LOOP
        if line.startswith("for"):
            try:
                inside = line[line.find("(")+1 : line.find(")")]
                parts = inside.split(";")

                init = parts[0].replace("int", "").strip()
                var = init.split("=")[0].strip()
                start = init.split("=")[1].strip()

                condition = parts[1]
                if "<=" in condition:
                    end = int(condition.split("<=")[1].strip()) + 1
                elif "<" in condition:
                    end = int(condition.split("<")[1].strip())
                else:
                    end = int(condition.split(">")[1].strip())

                line = f"for {var} in range({start}, {end}):"

            except:
                line = "# Unsupported for loop format"

        # IF
        elif line.startswith("if"):
            condition = line[line.find("(")+1 : line.find(")")]
            line = f"if {condition}:"

        # PRINTF
        elif "printf" in line:
            inside = line[line.find("(")+1 : line.rfind(")")]
            parts = inside.split(",")

            if len(parts) == 2:
                text = parts[0].replace('"', '').replace("%d", "{}")
                var = parts[1].strip()
                line = f'print(f"{text}".format({var}))'
            else:
                line = f'print({inside})'

        # Remove semicolon
        line = line.replace(";", "")

        result.append("    " * indent + line)

        if "{" in line:
            indent += 1

    return "\n".join(result)