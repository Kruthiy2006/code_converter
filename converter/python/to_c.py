def convert(code):
    lines = code.split("\n")
    result = []

    result.append("#include <stdio.h>")
    result.append("")
    result.append("int main() {")

    indent_level = 1

    for raw_line in lines:
        stripped = raw_line.strip()

        if not stripped:
            continue

        indentation = "    " * indent_level

        # ---------------- PRINT ----------------
        if stripped.startswith("print("):
            inside = stripped[6:-1]

            if inside.startswith("f"):
                inside = inside[2:-1]
                inside = inside.replace("{", "%d\", ")
                result.append(indentation + f'printf("{inside}");')
            else:
                result.append(indentation + f'printf("%s\\n", {inside});')

        # ---------------- INPUT ----------------
        elif "input()" in stripped:
            var = stripped.split("=")[0].strip()
            result.append(indentation + f"int {var};")
            result.append(indentation + f'scanf("%d", &{var});')

        # ---------------- FOR ----------------
        elif stripped.startswith("for"):
            inside = stripped[stripped.find("(")+1:stripped.find(")")]
            parts = inside.split(",")
            start = parts[0].strip()
            end = parts[1].strip()
            var = stripped.split()[1]

            result.append(indentation + f"for(int {var}={start}; {var}<{end}; {var}++) {{")
            indent_level += 1

        # ---------------- WHILE ----------------
        elif stripped.startswith("while"):
            condition = stripped[6:-1]
            result.append(indentation + f"while({condition}) {{")
            indent_level += 1

        # ---------------- IF ----------------
        elif stripped.startswith("if"):
            condition = stripped[3:-1]
            result.append(indentation + f"if({condition}) {{")
            indent_level += 1

        # ---------------- DEDENT ----------------
        if raw_line.startswith("    ") and not stripped.startswith(("if", "for", "while")):
            indent_level = max(1, indent_level)

    result.append("    return 0;")
    result.append("}")

    return "\n".join(result)