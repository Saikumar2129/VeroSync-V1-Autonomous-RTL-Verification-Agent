import anthropic
import os
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def create_fifo():
    print("🚀 VeroSync: Generating Clean RTL...")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": "Write a Synchronous FIFO in Verilog. Depth 8, Width 8. Ports: clk, rst, wr_en, rd_en, din[7:0], dout[7:0], full, empty. Output ONLY raw Verilog code. No markdown, no backticks, no explanations. Start directly with module keyword."
        }]
    )
    
    rtl = response.content[0].text.replace("```verilog", "").replace("```", "").strip()
    
    with open("fifo.v", "w") as f:
        f.write(rtl)
    
    print("✅ Clean RTL written to fifo.v!")

if __name__ == "__main__":
    create_fifo()