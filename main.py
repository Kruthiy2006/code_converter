def code_convert(code):
    lines = code.split('\n')
    result_list = []

    indent_level = 0   #  MUST BE OUTSIDE LOOP

    for line in lines:

        # remove inline comment
        if "//" in line:
            line = line.split("//")[0]

        line = line.strip()

        if line == "":
            continue

        if line.startswith("#include") or "int main" in line or "return 0" in line:
            continue

        # 🔹 Handle closing brace FIRST
        if line == "}":
            indent_level -= 1
            continue
        if line.startswith("int ") and ";" in line:
            continue

        # 🔹 Detect opening brace
        open_brace = False
        if line.endswith("{"):
            open_brace = True
            line = line[:-1].strip()

        # ------------------------
        # Conversion Logic
        # ------------------------

        # IF
        if line.startswith("if"):
            start = line.find("(")
            end = line.find(")")
            condition = line[start+1:end]
            line = f"if {condition}:"

        # ELSE IF
        elif line.startswith("else if"):
            start = line.find("(")
            end = line.find(")")
            condition = line[start+1:end]
            line = f"elif {condition}:"

        # WHILE
        elif line.startswith("while"):
            start = line.find("(")
            end = line.find(")")
            condition = line[start+1:end]
            line = f"while {condition}:"

        # FOR
        elif line.startswith("for"):
            start = line.find("(")
            end = line.find(")")
            inside = line[start+1:end]
            parts = inside.split(";")

            init = parts[0].strip().replace("int", "").strip()
            var, start_val = init.split("=")
            var = var.strip()
            start_val = start_val.strip()

            update = parts[2].strip()
            step = 1 if "++" in update else -1

            condition = parts[1].strip()
            if "<=" in condition:
                end_val = int(condition.split("<=")[1].strip()) + 1
            elif "<" in condition:
                end_val = int(condition.split("<")[1].strip())
            elif ">=" in condition:
                end_val = int(condition.split(">=")[1].strip()) - 1
            else:
                end_val = int(condition.split(">")[1].strip())

            if step == 1:
                line = f"for {var} in range({start_val}, {end_val}):"
            else:
                line = f"for {var} in range({start_val}, {end_val}, {step}):"

        # PRINT
        elif line.startswith("printf"):
            line = line.replace("printf", "print").replace(";", "")

        # ------------------------
        # Apply indentation
        # ------------------------
        indentation = "    " * indent_level
        result_list.append(indentation + line)

        # increase indent AFTER appending
        if open_brace:
            indent_level += 1

    return "\n".join(result_list)
#main

if __name__ == "__main__":

    filename = input("Enter C file name: ")

    with open(filename, "r") as f:
        code = f.read()

    converted = code_convert(code)

    print("\nConverted Python Code:\n")
    print(converted)