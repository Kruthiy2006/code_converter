def convert(code):
    lines = code.split("\n")
    result = []

    result.append("#include <stdio.h>")
    result.append("")
    result.append("int main() {")

    indent_level = 1

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("package") or line.startswith("import") or line.startswith("public class"):
            continue

        if "public static void main" in line:
            continue

        if line == "}":
            indent_level -= 1
            continue

        open_brace = False
        if line.endswith("{"):
            open_brace = True
            line = line[:-1].strip()

        indentation = "    " * indent_level

        # print
        if "System.out.println" in line:
            inside = line[line.find("(")+1 : line.rfind(")")]
            line = f'printf("%d\\n", {inside});'

        # remove types
        types = ["int", "double", "float", "char"]
        for t in types:
            if line.startswith(t + " "):
                break

        result.append(indentation + line)

        if open_brace:
            indent_level += 1

    result.append("    return 0;")
    result.append("}")

    return "\n".join(result)