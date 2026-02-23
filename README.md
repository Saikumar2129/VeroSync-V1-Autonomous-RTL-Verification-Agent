# VeroSync V1 — Autonomous RTL Verification Agent

An AI-powered agent that autonomously generates Verilog RTL, writes testbenches, detects compiler errors, and repairs them in a loop — without human intervention.

Built in 2 days by a final year B.E. CSE student after attending VLSI Design Conference 2026.

---

## What It Does

VeroSync runs a full autonomous verification pipeline:

1. **Generate RTL** — Claude generates synthesizable Verilog from a natural language spec
2. **Generate Testbench** — Claude writes a SystemVerilog testbench for the design
3. **Clean** — Deterministic Python cleaner removes markdown artifacts from AI output
4. **Compile** — iverilog compiles both files and captures any errors
5. **Auto-Fix** — Claude reads the errors and repairs both files intelligently
6. **Loop** — Repeats until compilation succeeds (max 5 retries)
7. **Simulate** — vvp runs the simulation and outputs a VCD waveform file

### Demo: 8-bit Synchronous FIFO

The V1 prototype verifies an 8-bit wide, 8-entry deep Synchronous FIFO. The testbench writes `0xAA` and `0xBB` into the FIFO and verifies they come out in the correct order.

---

## Results

✅ Compilation successful in 2 attempts
✅ Simulation passed — 0xAA and 0xBB verified correct
✅ VCD waveform generated and visualized in WaveTrace

---

## Project Structure

```
VeroSync_Project/
├── agent_v1.py        # Main orchestrator — runs the full pipeline
├── generate_rtl.py    # Generates Verilog RTL using Claude API
├── build_tb.py        # Generates SystemVerilog testbench using Claude API
├── auto_fixer.py      # Detects errors and repairs both files using Claude API
├── cleaner.py         # Deterministic cleaner — removes markdown artifacts
├── fifo.v             # AI-generated RTL design (changes each run)
├── fifo_tb.v          # AI-generated testbench (changes each run)
├── dump.vcd           # Simulation waveform output
├── requirements.txt   # Python dependencies
└── .env               # API keys (NOT committed — see .gitignore)
```

---

## Tech Stack

- **Python 3.14** — Core agent logic
- **Claude API (claude-sonnet-4-20250514)** — RTL generation, testbench generation, error repair
- **Icarus Verilog (iverilog)** — Open-source Verilog compiler
- **vvp** — Simulation runtime
- **WaveTrace (VS Code)** — VCD waveform visualization
- **python-dotenv** — Secure API key management

---

## Setup

### Prerequisites

- Python 3.10+
- Icarus Verilog: `brew install icarus-verilog` (Mac)
- Anthropic API key: https://console.anthropic.com

### Installation

```bash
git clone https://github.com/YOUR_USERNAME/VeroSync.git
cd VeroSync

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Run

```bash
python3 agent_v1.py
```

---

## Key Engineering Decisions

**Hybrid Approach: Deterministic + AI**
The cleaner.py uses pure Python rules to fix known, repeatable errors. Claude handles unknown semantic errors that require reasoning. Faster, cheaper, more reliable than using AI for everything.

**Why Claude over local LLMs**
Initial version used Ollama (qwen2.5-coder:7b). Failed to fix hardware-specific errors across 5 retries. Claude fixed on the first attempt. Model quality matters for complex technical domains.

---

## Roadmap

- [x] V1 — Autonomous syntax fixing with simulate → fail → fix loop
- [ ] V2 — VCD Logic Checker: detect functional errors from waveform analysis
- [ ] V3 — Autonomous logic bug fixing in RTL
- [ ] V4 — Generalized for any RTL module
- [ ] V5 — UVM testbench generation, formal verification integration

---

## Inspiration

Inspired by a talk on AI for chip verification at VLSI Design Conference 2026.
Research: VeriAssist, RTL-Repair, LLM4EDA, Veri-Sure.

---

## Author

**Sai Kumar** — Final Year B.E. CSE
Building VeroSync — Autonomous Verification Platform for the AI-generated RTL era.

---

*"The verification bottleneck in chip design is real. LLMs are generating RTL. Nobody is building the trust layer that verifies it. That's what VeroSync is."*