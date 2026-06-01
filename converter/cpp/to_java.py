def convert(code):
    lines = code.split("\n")
    result = []

    result.append("public class Main {")
    result.append("    public static void main(String[] args) {")

    indent_level = 2

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
            line = f"System.out.println({content});"

        # INPUT
        elif "cin >>" in line:
            var = line.replace("cin >>", "").strip()
            result.insert(1, "    import java.util.Scanner;")
            result.insert(3, "        Scanner sc = new Scanner(System.in);")
            line = f"int {var} = sc.nextInt();"

        result.append(indentation + line)

        if open_brace:
            indent_level += 1

    result.append("    }")
    result.append("}")

    return "\n".join(result)