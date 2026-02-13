#!/usr/bin/env python3
"""
dark_matter_scanner.py - Unified dark matter detection tool

Runs all dark matter detectors and generates comprehensive report
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any

# Import all detectors
try:
    from magic_gravity import detect_magic_gravity, calculate_dark_mass_score, MagicConstant
    from phantom_loops import detect_phantom_loops, calculate_phantom_score, PhantomLoop
    from zombie_orbits import detect_zombie_orbits, calculate_zombie_score, ZombieOrbit
    from evidence_voids import detect_evidence_voids, calculate_void_score, EvidenceVoid
except ImportError as e:
    print(f"Error importing detectors: {e}")
    print("Make sure all detector modules are in the same directory")
    sys.exit(1)


class DarkMatterScanner:
    """Unified scanner for all types of code dark matter"""
    
    def __init__(self, source_code: str, filepath: str = "unknown"):
        self.source_code = source_code
        self.filepath = filepath
        self.results = {}
        
    def scan_all(self) -> Dict[str, Any]:
        """Run all detectors and collect results"""
        
        print(f"\n🌌 Scanning {self.filepath} for dark matter...")
        print("=" * 70)
        
        # Magic Gravity
        print("\n🌑 Running Magic Gravity detector...")
        magic_constants = detect_magic_gravity(self.source_code)
        magic_score = calculate_dark_mass_score(magic_constants)
        self.results['magic_gravity'] = {
            'findings': magic_constants,
            'score': magic_score,
            'count': len(magic_constants)
        }
        print(f"   Found {len(magic_constants)} magic constants (score: {magic_score:.1f})")
        
        # Phantom Loops
        print("\n♾️  Running Phantom Loops detector...")
        phantoms = detect_phantom_loops(self.source_code)
        phantom_score = calculate_phantom_score(phantoms)
        self.results['phantom_loops'] = {
            'findings': phantoms,
            'score': phantom_score,
            'count': len(phantoms)
        }
        print(f"   Found {len(phantoms)} phantom loops (score: {phantom_score:.1f})")
        
        # Zombie Orbits
        print("\n🧟 Running Zombie Orbits detector...")
        zombies = detect_zombie_orbits(self.source_code)
        zombie_score = calculate_zombie_score(zombies)
        self.results['zombie_orbits'] = {
            'findings': zombies,
            'score': zombie_score,
            'count': len(zombies)
        }
        print(f"   Found {len(zombies)} zombie orbits (score: {zombie_score:.1f})")
        
        # Evidence Voids
        print("\n📊 Running Evidence Voids detector...")
        voids = detect_evidence_voids(self.source_code)
        void_score = calculate_void_score(voids)
        self.results['evidence_voids'] = {
            'findings': voids,
            'score': void_score,
            'count': len(voids)
        }
        print(f"   Found {len(voids)} evidence voids (score: {void_score:.1f})")
        
        # Calculate overall dark matter score
        total_score = magic_score + phantom_score + zombie_score + void_score
        total_findings = (len(magic_constants) + len(phantoms) + 
                         len(zombies) + len(voids))
        
        self.results['summary'] = {
            'total_score': total_score,
            'total_findings': total_findings,
            'filepath': self.filepath
        }
        
        print("\n" + "=" * 70)
        print(f"\n🌌 TOTAL DARK MATTER SCORE: {total_score:.1f}")
        print(f"   Total findings: {total_findings}")
        
        return self.results
    
    def generate_report(self, format: str = 'text') -> str:
        """Generate formatted report"""
        if format == 'json':
            return self._generate_json_report()
        else:
            return self._generate_text_report()
    
    def _generate_text_report(self) -> str:
        """Generate human-readable text report"""
        lines = []
        
        lines.append("\n" + "=" * 70)
        lines.append("🌌 DARK MATTER DETECTION REPORT")
        lines.append("=" * 70)
        
        summary = self.results.get('summary', {})
        lines.append(f"\nFile: {summary.get('filepath', 'unknown')}")
        lines.append(f"Total Dark Matter Score: {summary.get('total_score', 0):.1f}")
        lines.append(f"Total Findings: {summary.get('total_findings', 0)}")
        
        # Magic Gravity section
        magic = self.results.get('magic_gravity', {})
        if magic.get('count', 0) > 0:
            lines.append("\n" + "-" * 70)
            lines.append(f"🌑 MAGIC GRAVITY ({magic['count']} findings, score: {magic['score']:.1f})")
            lines.append("-" * 70)
            for const in magic['findings'][:5]:  # Show first 5
                lines.append(f"\nLine {const.line} | {const.context}")
                lines.append(f"  Value: {const.value}")
                lines.append(f"  Type: {const.gravity_type.value}")
                lines.append(f"  Severity: {const.severity}")
        
        # Phantom Loops section
        phantom = self.results.get('phantom_loops', {})
        if phantom.get('count', 0) > 0:
            lines.append("\n" + "-" * 70)
            lines.append(f"♾️  PHANTOM LOOPS ({phantom['count']} findings, score: {phantom['score']:.1f})")
            lines.append("-" * 70)
            for loop in phantom['findings'][:5]:
                lines.append(f"\nLine {loop.line} | {loop.context}")
                lines.append(f"  Type: {loop.phantom_type.value}")
                lines.append(f"  Issue: {loop.description}")
                lines.append(f"  Severity: {loop.severity}")
        
        # Zombie Orbits section
        zombie = self.results.get('zombie_orbits', {})
        if zombie.get('count', 0) > 0:
            lines.append("\n" + "-" * 70)
            lines.append(f"🧟 ZOMBIE ORBITS ({zombie['count']} findings, score: {zombie['score']:.1f})")
            lines.append("-" * 70)
            for z in zombie['findings'][:5]:
                lines.append(f"\nLine {z.line} | {z.context}")
                lines.append(f"  Type: {z.zombie_type.value}")
                lines.append(f"  Issue: {z.description}")
                lines.append(f"  Severity: {z.severity}")
        
        # Evidence Voids section  
        void = self.results.get('evidence_voids', {})
        if void.get('count', 0) > 0:
            lines.append("\n" + "-" * 70)
            lines.append(f"📊 EVIDENCE VOIDS ({void['count']} findings, score: {void['score']:.1f})")
            lines.append("-" * 70)
            for v in void['findings'][:5]:
                lines.append(f"\nLine {v.line} | {v.context}")
                lines.append(f"  Type: {v.void_type.value}")
                lines.append(f"  Issue: {v.description}")
                lines.append(f"  Severity: {v.severity}")
        
        lines.append("\n" + "=" * 70)
        lines.append("\n💡 RECOMMENDATIONS:")
        lines.append("  • Document or remove magic constants")
        lines.append("  • Fix phantom loops claiming false infinity")
        lines.append("  • Eliminate zombie code running without purpose")
        lines.append("  • Add logging/monitoring to evidence voids")
        lines.append("\n  Dark matter isn't always bad - but it should be intentional.")
        lines.append("  Make invisible forces visible through documentation and design.")
        
        return "\n".join(lines)
    
    def _generate_json_report(self) -> str:
        """Generate JSON report"""
        # Convert dataclass objects to dicts for JSON serialization
        json_results = {
            'summary': self.results.get('summary', {}),
            'magic_gravity': {
                'score': self.results['magic_gravity']['score'],
                'count': self.results['magic_gravity']['count'],
                'findings': [
                    {
                        'line': c.line,
                        'value': c.value,
                        'type': c.gravity_type.value,
                        'severity': c.severity,
                        'context': c.context
                    }
                    for c in self.results['magic_gravity']['findings']
                ]
            },
            'phantom_loops': {
                'score': self.results['phantom_loops']['score'],
                'count': self.results['phantom_loops']['count'],
                'findings': [
                    {
                        'line': p.line,
                        'type': p.phantom_type.value,
                        'description': p.description,
                        'severity': p.severity,
                        'context': p.context
                    }
                    for p in self.results['phantom_loops']['findings']
                ]
            },
            'zombie_orbits': {
                'score': self.results['zombie_orbits']['score'],
                'count': self.results['zombie_orbits']['count'],
                'findings': [
                    {
                        'line': z.line,
                        'type': z.zombie_type.value,
                        'description': z.description,
                        'severity': z.severity,
                        'context': z.context
                    }
                    for z in self.results['zombie_orbits']['findings']
                ]
            },
            'evidence_voids': {
                'score': self.results['evidence_voids']['score'],
                'count': self.results['evidence_voids']['count'],
                'findings': [
                    {
                        'line': v.line,
                        'type': v.void_type.value,
                        'description': v.description,
                        'severity': v.severity,
                        'context': v.context
                    }
                    for v in self.results['evidence_voids']['findings']
                ]
            }
        }
        
        return json.dumps(json_results, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description='Dark Matter Scanner - Find invisible forces in code'
    )
    parser.add_argument('file', help='Python file to scan')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    # Read source file
    try:
        filepath = Path(args.file)
        source_code = filepath.read_text()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Run scanner
    scanner = DarkMatterScanner(source_code, str(filepath))
    scanner.scan_all()
    
    # Generate report
    report = scanner.generate_report(format=args.format)
    
    # Output
    if args.output:
        Path(args.output).write_text(report)
        print(f"\n📄 Report saved to: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
