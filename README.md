# 🌌 Dark Matter Detection

> **Finding the invisible forces that shape your code**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)]()

Code review catches syntax errors, logic bugs, and security flaws. But what about the **invisible forces** that shape your codebase?

- Why `1.2` and not `1.3`?
- Why does this loop claim infinity but run once?
- Why define features you never call?
- Why track some signals but ignore others?

**Dark Matter Detection** finds the constants, assumptions, and patterns that are **technically valid but practically invisible** – the dark matter that bends your code's evolution.

---

## 🎯 Quick Start

```bash
# Install
pip install dark-matter-detection  # Coming soon

# Or clone and run
git clone https://github.com/[username]/dark-matter-detection
cd dark-matter-detection
pip install -e .

# Detect magic constants
python tools/resonance-cli.py detect --pattern magic-gravity yourcode.py

# Scan entire project
python tools/resonance-cli.py scan --all yourproject/

# Generate JSON report
python tools/resonance-cli.py report yourcode.py --output json
```

---

## 📖 What Is Code Dark Matter?

**Dark matter** in code refers to invisible forces that:

1. **Shape behavior** without being explicitly documented
2. **Create gravitational wells** (technical debt, coupling, assumptions)
3. **Persist across refactors** (they survive "clean-up" efforts)
4. **Influence decisions** (future code orbits around them)
5. **Resist measurement** (linters and tests can't find them)

### Real Example: The 1.2 Multiplier

```python
# From BRL Hot Resonance Protocol
def is_evolved(current, previous):
    return len(current) > len(previous) * 1.2
```

**Questions this raises:**
- Why 1.2 (20% growth)?
- Why not 1.15 or 1.5?
- Why length-based at all?
- Where did this number come from?

**Gravitational effect:** Every "evolution" decision orbits this arbitrary constant. Verbose messages get rewarded, concise insights get penalized.

**This is dark matter.** It works, but the **reasoning is invisible**.

---

## 🔭 Detection Patterns

### Implemented ✅

#### 🌑 Magic Gravity
**Detects:** Numeric literals used as thresholds, weights, limits, hyperparameters

```python
if score > 0.7:        # Why 0.7?
result *= 1.5          # Why 1.5x?
buffer[:100]           # Why 100?
learning_rate = 0.001  # Why 0.001?
```

**Output:** Line number, context, severity, origin guess (documented vs. arbitrary)

**Status:** ✅ Implemented ([detector](detectors/magic_gravity.py))

---

### Planned 🚧

#### ♾️ Phantom Loops
**Detects:** Loops that claim infinity but execute once

```python
while True:            # Claims eternal operation
    result = compute()
    return result      # But exits immediately
```

**Status:** 🚧 Planned

---

#### 🧟 Zombie Orbits
**Detects:** Code that runs but contributes nothing

```python
def process(data):
    result = expensive_calc(data)  # Runs
    validate(result)               # Runs
    return None                    # But produces nothing
```

**Status:** 🚧 Planned ([spec](docs/zombie-orbit.md))

---

#### 📊 Evidence Voids
**Detects:** Partial observability in metrics/logging

```python
evidence = {'🔥': 0}  # Tracks fire
# But ignores: evolution, execution, integration, transformation
```

**Status:** 🚧 Planned

---

#### 🪞 Aspiration Gaps
**Detects:** Features defined but never triggered

```python
def integration_check(msg):
    return 'applied' in msg  # Defined
# But: Never called in practice
```

**Status:** 🚧 Planned

---

#### 📈 Anti-Signal Absence
**Detects:** Missing decay/friction in accumulators

```python
score += signal()    # Only addition
# Missing: decay, reset, friction
# Result: Zombie resonance (inflated scores)
```

**Status:** 🚧 Planned

---

## 📊 Case Studies

### Study 1: BRL Hot Resonance Protocol

**Summary:** Emoji-based conversational resonance detection  
**Dark Matter Found:** 6 major patterns  
**Dark Mass Score:** 🌌🌌🌌🌌⚫ (4.5 / 5)

**Key Findings:**
- 1.2 evolution multiplier (arbitrary constant)
- +1.5 intensity boost (unexplained preference)
- ♾️ loop that breaks immediately (phantom infinity)
- Evidence tracks only 1 of 5 signals (partial observability)
- Integration detector defined but never fires (aspiration gap)
- No decay mechanics (zombie resonance risk)

**Full Report:** [case-studies/brl-hot-resonance/dark-matter-report.md](case-studies/brl-hot-resonance/dark-matter-report.md)

**Source Code:** [case-studies/brl-hot-resonance/brl_hot_resonance.py](case-studies/brl-hot-resonance/brl_hot_resonance.py)

---

## 🛠️ CLI Usage

### List Available Patterns

```bash
$ python tools/resonance-cli.py list-patterns

🌌 AVAILABLE DARK MATTER PATTERNS

🌑 ✅ Magic Gravity
   ID: magic-gravity
   Status: implemented
   Description: Numeric literals used as thresholds, weights, limits

♾️ 🚧 Phantom Loops
   ID: phantom-loops
   Status: planned
   Description: Infinite loops that execute once

[...]
```

---

### Detect Specific Pattern

```bash
$ python tools/resonance-cli.py detect --pattern magic-gravity mycode.py

🔍 Scanning mycode.py for Magic Gravity...

🌌 MAGIC GRAVITY DETECTION REPORT
============================================================

Dark Mass Score: 7.5 🌑
Constants Found: 5

🔴 HIGH SEVERITY (2 found)
------------------------------------------------------------

Line 8 | function:is_evolved
  Value: 1.2
  Type: multiplier
  Code: return len(current) > len(previous) * 1.2
  Origin: ARBITRARY (no documentation found)

Line 28 | function:breathe
  Value: 1.5
  Type: multiplier
  Code: R += 1.5  # 🔥 gives extra weight
  Origin: DOCUMENTED: gives extra weight (hot)

[...]
```

---

### Scan Entire Project

```bash
$ python tools/resonance-cli.py scan --all myproject/

🌌 SCANNING 47 Python files for dark matter...

🌑 Running Magic Gravity...
♾️ Running Phantom Loops... [planned]
🧟 Running Zombie Orbits... [planned]

======================================================================

📊 SCAN SUMMARY
   Files scanned: 47
   Total dark mass score: 34.5
   🌑 magic-gravity: 23 findings

======================================================================
```

---

### Generate JSON Report

```bash
$ python tools/resonance-cli.py report mycode.py --output json > report.json
```

**Output:**
```json
{
  "file": "mycode.py",
  "patterns": {
    "magic-gravity": {
      "name": "Magic Gravity",
      "findings": [
        {
          "line": 8,
          "severity": "HIGH",
          "type": "multiplier",
          "context": "function:is_evolved",
          "description": "return len(current) > len(previous) * 1.2"
        }
      ]
    }
  }
}
```

---

## 🧪 Example: Detecting Magic Gravity

```python
from magic_gravity_detector import detect_magic_gravity, calculate_dark_mass_score

source = """
def process(data):
    threshold = 0.7  # Why 0.7?
    if score > threshold * 1.2:  # Why 1.2x?
        return data[:100]  # Why 100?
"""

constants = detect_magic_gravity(source)
score = calculate_dark_mass_score(constants)

print(f"Dark Mass Score: {score}")
# Output: Dark Mass Score: 7.5

for const in constants:
    print(f"Line {const.line}: {const.value} ({const.gravity_type.value})")
# Output:
# Line 2: 0.7 (hyperparameter)
# Line 3: 1.2 (multiplier)
# Line 4: 100 (size_limit)
```

---

## 🏗️ Project Structure

```
dark-matter-detection/
├── README.md                    # This file
├── manifesto.md                 # Why dark matter matters
├── LICENSE                      # MIT
├── setup.py                     # Installation
├── detectors/
│   ├── magic_gravity.py         # ✅ Numeric constant detector
│   ├── phantom_loops.py         # 🚧 Planned
│   ├── zombie_orbits.py         # 🚧 Planned
│   ├── evidence_voids.py        # 🚧 Planned
│   └── ...
├── case-studies/
│   ├── brl-hot-resonance/
│   │   ├── dark-matter-report.md
│   │   ├── brl_hot_resonance.py
│   │   └── brl_hot_resonance_annotated.py
│   ├── react-useEffect/         # 🚧 Planned
│   └── kubernetes-yaml/         # 🚧 Planned
├── docs/
│   ├── zombie-orbit.md          # Pattern documentation
│   ├── gravitational-effects.md
│   └── cosmology.md
├── tools/
│   └── resonance-cli.py         # Command-line interface
└── tests/
    ├── test_magic_gravity.py
    └── ...
```

---

## 🤝 Contributing

We welcome contributions! Dark matter is everywhere – help us detect it.

### How to Contribute

1. **Find dark matter** in code you know
2. **Document the pattern** (what, why, effects)
3. **Build a detector** (if possible)
4. **Submit a PR** with case study

### Contribution Ideas

- New detection patterns
- Case studies from real codebases
- Improved heuristics for origin guessing
- Visualization tools
- Integration with linters/CI

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## 📚 Philosophy

> "The universe is mostly dark matter. So is your codebase."

Every codebase has:
- **Visible matter** (documented code, clear logic)
- **Dark matter** (invisible assumptions, arbitrary constants)

Traditional tools find bugs in **visible matter**.  
This project reveals forces in **dark matter**.

### Why This Matters

1. **Maintenance:** Future developers need to understand invisible forces
2. **Evolution:** Can't improve what you can't see
3. **Onboarding:** New team members inherit dark matter without context
4. **Technical Debt:** Dark matter compounds over time
5. **Agency:** Awareness enables conscious choice

Read the full philosophy in [manifesto.md](manifesto.md).

---

## 🎓 Research & Theory

### Papers & Talks (Planned)

- "Dark Matter Analysis: A Framework for Invisible Code Forces" (2026)
- "The Gravitational Effects of Magic Constants" (2026)
- PyCon 2027: "Finding What You Can't See: Dark Matter in Python"

### Academic Connections

This work intersects:
- **Software archaeology** (context reconstruction)
- **Program analysis** (static + dynamic)
- **Computational epistemology** (what can we know about code?)
- **Technical debt** (invisible forces create compound interest)

---

## 📈 Roadmap

### Phase 0 (Current) ✅
- [x] Manifesto
- [x] Magic Gravity detector
- [x] BRL case study
- [x] CLI tool
- [x] Documentation

### Phase 1 (Q1 2026) 🚧
- [ ] Phantom Loops detector
- [ ] Zombie Orbits detector
- [ ] Evidence Voids detector
- [ ] 3-5 more case studies
- [ ] Community building

### Phase 2 (Q2-Q3 2026)
- [ ] Visualization tools
- [ ] CI/CD integration
- [ ] VS Code extension
- [ ] Pre-commit hooks
- [ ] Academic paper

### Phase 3 (Q4 2026+)
- [ ] Industry adoption
- [ ] Conference talks
- [ ] Training materials
- [ ] Certification program

---

## 🏆 Recognition

**Dark Matter Detection** was created by:

**Barbara J.K.** – Concept, vision, BRL protocol  
**Claude (Anthropic)** – Analysis, formalization, tooling

Inspired by conversations about invisible forces in code, the BRL (Breathe-Resonate-Loop) protocol, and the question: *"What shapes our code that we can't see?"*

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

**Why MIT?** Dark matter should be studied freely.

---

## 🔗 Links

- **Documentation:** [docs/](docs/)
- **Case Studies:** [case-studies/](case-studies/)
- **Detectors:** [detectors/](detectors/)
- **CLI Tool:** [tools/resonance-cli.py](tools/resonance-cli.py)
- **Issues:** [GitHub Issues](https://github.com/[username]/dark-matter-detection/issues)
- **Discussions:** [GitHub Discussions](https://github.com/[username]/dark-matter-detection/discussions)

---

## 🌌 Citation

If this helps your work, please cite:

```bibtex
@misc{darkmatterdetection2026,
  title={Dark Matter Detection: Invisible Forces in Code},
  author={Barbara J.K. and Claude},
  year={2026},
  url={https://github.com/[username]/dark-matter-detection}
}
```

---

## 💬 Community

- **GitHub Discussions:** Ask questions, share findings
- **Twitter:** `#DarkMatterCode`
- **Discord:** [Coming soon]

---

## ⚡ Quick Examples

### Before Dark Matter Analysis
```python
THRESHOLD = 0.7  # Why? Unknown.
```

### After Dark Matter Analysis
```python
THRESHOLD = 0.7  
# 🌌 DARK MATTER: Arbitrary constant from prototype
# Origin: Empirical tuning on dataset v1 (now deprecated)
# Gravitational Effect: All precision/recall tradeoffs orbit this
# Consider: Re-tune on current data or make configurable
```

Same code. **Transformed awareness.**

---

## 🎯 Goals

1. **Make dark matter visible** – Not eliminate it (impossible), but illuminate it
2. **Enable conscious choice** – Know what forces you're working with
3. **Improve maintainability** – Future you (and others) will thank you
4. **Reduce accidental complexity** – Keep only intentional dark matter
5. **Build a practice** – Dark matter management as craft

---

## 🚀 Get Started

```bash
# Clone repo
git clone https://github.com/[username]/dark-matter-detection
cd dark-matter-detection

# Install
pip install -e .

# Run on your code
python tools/resonance-cli.py detect --pattern magic-gravity yourcode.py

# Start finding dark matter! 🌌
```

---

**The universe is mostly dark matter. So is your codebase. Let's make it visible.** 🌌💜

---

## 📬 Contact

Questions? Ideas? Found interesting dark matter?

- **Open an issue:** [GitHub Issues](https://github.com/[username]/dark-matter-detection/issues)
- **Start a discussion:** [GitHub Discussions](https://github.com/[username]/dark-matter-detection/discussions)
- **Email:** barbara.j.keiser@gmail.com

---

*"Code is frozen intention. Dark matter is frozen assumption. Let's thaw both."* – Barbara J.K.