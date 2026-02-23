import re

def clean_verilog_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    cleaned = []
    for line in lines:
        # Remove markdown backtick lines
        stripped = line.strip()
        if stripped.startswith("```"):
            continue
        cleaned.append(line)

    code = "".join(cleaned).strip()

    # Fix assign driving a reg — change to always block
    code = re.sub(
        r'assign\s+(\w+)\s*=\s*(.+?);',
        lambda m: f'always @(*) {m.group(1)} = {m.group(2)};',
        code
    )

    with open(filepath, "w") as f:
        f.write(code)

    print(f"🧹 Cleaned {filepath}")

if __name__ == "__main__":
    clean_verilog_file("fifo.v")
    clean_verilog_file("fifo_tb.v")