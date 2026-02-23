import anthropic
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def run_compilation():
    result = subprocess.run(
        ["iverilog", "-o", "sim.out", "fifo.v", "fifo_tb.v"],
        capture_output=True, text=True
    )
    if result.stderr:
        print(f"  Compiler says: {result.stderr}")
    return result.stderr

def fix_code(error_log):
    print("🛠️ VeroSync: Sending errors to Claude for repair...")
    
    with open("fifo.v", "r") as f:
        rtl = f.read()
    with open("fifo_tb.v", "r") as f:
        tb = f.read()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f"""You are a Verilog expert. Fix both files based on these compiler errors:

ERRORS:
{error_log}

fifo.v:
{rtl}

fifo_tb.v:
{tb}

Return ONLY this format, no other text:
===FIFO.V===
<fixed fifo.v code here>
===FIFO_TB.V===
<fixed fifo_tb.v code here>"""
        }]
    )

    result = response.content[0].text
    
    if "===FIFO.V===" in result and "===FIFO_TB.V===" in result:
        parts = result.split("===FIFO_TB.V===")
        fixed_rtl = parts[0].replace("===FIFO.V===", "").replace("```verilog", "").replace("```", "").strip()
        fixed_tb = parts[1].replace("```verilog", "").replace("```", "").strip()
        
        with open("fifo.v", "w") as f:
            f.write(fixed_rtl)
        with open("fifo_tb.v", "w") as f:
            f.write(fixed_tb)
    
    print("✅ Claude repair complete.")

if __name__ == "__main__":
    errors = run_compilation()
    if errors:
        fix_code(errors)
    else:
        print("🎉 No errors!")