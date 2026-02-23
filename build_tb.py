import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def create_testbench():
    print("📍 Checkpoint 1: Script started.")
    
    if not os.path.exists("fifo.v"):
        print("❌ Error: fifo.v not found!")
        return

    print("📖 Checkpoint 2: Reading fifo.v...")
    with open("fifo.v", "r") as f:
        rtl_code = f.read()

    print("🧠 Checkpoint 3: Contacting Claude...")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"Write a Verilog testbench for this FIFO RTL. Use reg for inputs, wire for outputs. Include clock generation, reset, write and read tests. Output ONLY raw Verilog. No markdown, no backticks.\n\n{rtl_code}"
        }]
    )

    print("✅ Checkpoint 4: Received response from Claude.")
    tb = response.content[0].text.replace("```verilog", "").replace("```", "").strip()

    with open("fifo_tb.v", "w") as f:
        f.write(tb)
    
    print("✨ Checkpoint 5: fifo_tb.v written!")

if __name__ == "__main__":
    create_testbench()