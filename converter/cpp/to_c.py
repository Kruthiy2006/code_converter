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

        if line.startswith("#include") or line.startswith("using namespace"):
            continue

        if "int main" in line:
            continue

        if line == "}":
            indent_level -= 1
            continue

        open_brace = False
        if line.endswith("{"):
            open_brace = True
            line = line[:-1].strip()

        indentation = "    " * indent_level

        # PRINT
        if "cout <<" in line:
            content = line.replace("cout <<", "").replace("<< endl", "").strip()
            line = f'printf("%d\\n", {content});'

        # INPUT
        elif "cin >>" in line:
            var = line.replace("cin >>", "").strip()
            line = f'scanf("%d", &{var});'

        result.append(indentation + line)

        if open_brace:
            indent_level += 1

    result.append("    return 0;")
    result.append("}")

    return "\n".join(result)