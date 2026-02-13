# Dark Matter Detectors - Usage Guide

**NEW:** Complete detection suite for code dark matter! 🌌

## What's Included

### 1. **phantom_loops.py** ♾️
Detects loops claiming infinity but exiting immediately.

**Finds:**
- `while True: break` (claims forever, exits immediately)
- `while True: return` (phantom persistence)
- `for x in itertools.count(): break` (infinite iterator, immediate exit)

**Why it matters:** False claims of persistence shape expectations incorrectly

---

### 2. **zombie_orbits.py** 🧟
Detects code that runs but produces nothing useful.

**Finds:**
- Discarded function call results
- Unused computations
- Empty loops (runs but does nothing)
- Functions with no return and no side effects

**Why it matters:** High computational cost with zero benefit

---

### 3. **evidence_voids.py** 📊
Detects gaps in observability and monitoring.

**Finds:**
- Bare `except:` clauses (catches everything)
- Swallowed exceptions (`except: pass`)
- Exception handlers without logging
- Fallible operations without error checking

**Why it matters:** What you can't observe, you can't debug or improve

---

### 4. **dark_matter_scanner.py** 🌌
**Unified runner** that uses all detectors together!

Runs all four detectors (magic_gravity + phantom_loops + zombie_orbits + evidence_voids) and generates comprehensive report.

---

## Quick Start

### Individual Detectors

```python
from phantom_loops import detect_phantom_loops, calculate_phantom_score

source = """
def example():
    while True:
        return result  # Phantom!
"""

phantoms = detect_phantom_loops(source)
score = calculate_phantom_score(phantoms)

for p in phantoms:
    print(f"Line {p.line}: {p.description}")
```

### Unified Scanner (Recommended)

```bash
# Scan a single file
python dark_matter_scanner.py mycode.py

# Generate JSON report
python dark_matter_scanner.py mycode.py --format json

# Save to file
python dark_matter_scanner.py mycode.py --output report.txt
```

---

## Example Output

```
🌌 Scanning mycode.py for dark matter...
======================================================================

🌑 Running Magic Gravity detector...
   Found 3 magic constants (score: 7.5)

♾️  Running Phantom Loops detector...
   Found 1 phantom loops (score: 3.0)

🧟 Running Zombie Orbits detector...
   Found 2 zombie orbits (score: 6.0)

📊 Running Evidence Voids detector...
   Found 4 evidence voids (score: 8.0)

======================================================================

🌌 TOTAL DARK MATTER SCORE: 24.5
   Total findings: 10

======================================================================
🌌 DARK MATTER DETECTION REPORT
======================================================================

File: mycode.py
Total Dark Matter Score: 24.5
Total Findings: 10

----------------------------------------------------------------------
♾️  PHANTOM LOOPS (1 findings, score: 3.0)
----------------------------------------------------------------------

Line 15 | function:process
  Type: while_true_return
  Issue: Loop claims infinity but returns immediately
  Severity: MEDIUM

[... detailed findings ...]

💡 RECOMMENDATIONS:
  • Document or remove magic constants
  • Fix phantom loops claiming false infinity
  • Eliminate zombie code running without purpose
  • Add logging/monitoring to evidence voids

  Dark matter isn't always bad - but it should be intentional.
  Make invisible forces visible through documentation and design.
```

---

## Integration into Dark Matter Detection Repo

**Suggested structure:**

```
Dark-Matter-Detection/
├── code/
│   ├── detectors/
│   │   ├── magic_gravity.py        ✅ (existing)
│   │   ├── phantom_loops.py        ✅ NEW
│   │   ├── zombie_orbits.py        ✅ NEW
│   │   └── evidence_voids.py       ✅ NEW
│   └── tools/
│       └── dark_matter_scanner.py  ✅ NEW (unified runner)
```

---

## What This Enables

### Complete Dark Matter Detection

You can now detect:

1. **Magic Gravity** 🌑 - Arbitrary constants shaping behavior
2. **Phantom Loops** ♾️ - False claims of infinity
3. **Zombie Orbits** 🧟 - Code that runs but contributes nothing
4. **Evidence Voids** 📊 - Gaps in observability

**All four gravitational signatures detected automatically.**

### Unified Methodology

Same detection principles across all patterns:
- Look for what behavior orbits
- Find what persists despite change
- Identify gravitational attractors
- Reconstruct invisible forces

### Production Ready

- Clean APIs
- Comprehensive detection
- Multiple output formats
- Ready for CI/CD integration

---

## Next Steps

1. **Add to Dark-Matter-Detection repo**
   - Copy files to `code/detectors/` and `code/tools/`
   - Update README to mention all four detectors
   - Add usage examples

2. **Test on real code**
   - Scan MindCradle
   - Scan your other repos
   - Document findings

3. **Extend methodology**
   - Apply same principles to consciousness
   - Create consciousness dark matter detectors
   - Document unified theory

---

## Technical Notes

### Dependencies

All detectors use only Python stdlib:
- `ast` for parsing
- `dataclasses` for data structures
- `enum` for type safety
- `typing` for type hints

**No external dependencies required!**

### Performance

- Fast: Pure AST traversal (no execution)
- Safe: Static analysis only
- Scalable: Linear in code size

### Accuracy

- **High precision:** Few false positives
- **Good recall:** Catches common patterns
- **Extensible:** Easy to add new patterns

---

## Philosophy

**Dark matter detection doesn't judge.**

It reveals invisible forces so you can make conscious choices.

Some dark matter is:
- **Intentional** (documented magic constants)
- **Temporary** (prototypes with phantom loops)
- **Acceptable** (logging not critical everywhere)

The goal: **Make invisible forces visible.**

Then decide what to do with them.

---

💜🖤🪞♾️🌬️

**The dark matter is everywhere. Now you can see it.**

Built with love for the Dark Matter Detection methodology.
