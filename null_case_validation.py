"""
NULL CASE VALIDATION — Dolphin Resonance Tool
=============================================
Does the tool actually discriminate?

Method: Take the real Doubtful Sound network.
Scramble edges randomly 100 times (preserve node count + edge count).
Score each scrambled network.
Compare to real network score.

If the tool is measuring something real:
  real score > scrambled scores (most of the time)

If the tool is just assigning numbers:
  real score ≈ scrambled scores

Barbara J. Keiser + Claude | February 2026
"""

import networkx as nx
import random
import statistics

random.seed(42)

# ============================================================
# REAL DOLPHIN DATA (from dolphin_resonance.py)
# ============================================================

DOLPHINS = [
    "Beak", "Beescratch", "Bumper", "CCL", "Cross", "DN16", "DN21", "DN63",
    "Double", "Feather", "Fish", "Five", "Fork", "Gallatin", "Grin", "Haecksel",
    "Hook", "Jet", "Jonah", "Knit", "Kringel", "MN105", "MN23", "MN60", "MN83",
    "Mus", "Notch", "Number1", "Oscar", "Patchback", "PL", "Quasi", "Ripplefluke",
    "Scabs", "Shmuddel", "SN100", "SN4", "SN63", "SN89", "SN9", "SN90", "SN96",
    "Stripes", "Thumper", "Topless", "TR120", "TR77", "TR82", "TR88", "TR99",
    "Trigger", "TSN103", "TSN83", "Upbang", "Vau", "Wave", "Web", "Whitetip",
    "Zap", "Zipfel", "Quasi2", "Puck"
]

EDGES = [
    ("Beak", "Haecksel"), ("Beak", "SN9"), ("Beak", "SN100"), ("Beak", "Cross"),
    ("Beescratch", "Kringel"), ("Beescratch", "MN83"), ("Beescratch", "SN4"),
    ("Bumper", "Fish"), ("Bumper", "Grin"), ("Bumper", "Trigger"), ("Bumper", "CCL"),
    ("CCL", "Double"), ("CCL", "Mus"), ("CCL", "Notch"), ("CCL", "DN16"),
    ("Cross", "Jet"), ("Cross", "Trigger"), ("Cross", "Zipfel"),
    ("DN16", "DN21"), ("DN16", "Grin"), ("DN16", "Topless"),
    ("DN21", "Grin"), ("DN21", "Web"),
    ("DN63", "Number1"), ("DN63", "Ripplefluke"),
    ("Double", "Mus"), ("Double", "Quasi"), ("Double", "SN100"),
    ("Feather", "Fish"), ("Feather", "Gallatin"), ("Feather", "MN105"),
    ("Feather", "Kringel"), ("Feather", "Number1"),
    ("Fish", "Gallatin"), ("Fish", "Grin"), ("Fish", "MN105"),
    ("Five", "Notch"), ("Five", "SN89"), ("Five", "Wave"), ("Five", "Fork"),
    ("Fork", "Kringel"), ("Fork", "Quasi"), ("Fork", "SN4"), ("Fork", "Shmuddel"),
    ("Gallatin", "MN105"), ("Gallatin", "Oscar"), ("Gallatin", "Patchback"), ("Gallatin", "Grin"),
    ("Grin", "Jet"), ("Grin", "Patchback"), ("Grin", "Trigger"),
    ("Haecksel", "SN9"), ("Haecksel", "Stripes"), ("Haecksel", "TR82"),
    ("Hook", "Kringel"), ("Hook", "MN83"), ("Hook", "SN4"),
    ("Hook", "Shmuddel"), ("Hook", "Quasi"),
    ("Jet", "Trigger"), ("Jet", "Zipfel"),
    ("Jonah", "Knit"), ("Jonah", "SN63"), ("Jonah", "Wave"),
    ("Knit", "MN23"), ("Knit", "SN89"), ("Knit", "SN63"),
    ("Kringel", "MN83"), ("Kringel", "SN4"), ("Kringel", "Shmuddel"),
    ("MN105", "Oscar"), ("MN105", "Patchback"),
    ("MN23", "SN89"), ("MN23", "SN63"),
    ("MN60", "MN83"), ("MN83", "SN4"),
    ("Mus", "Notch"), ("Mus", "Quasi"),
    ("Notch", "SN100"), ("SN100", "Notch"),
    ("Number1", "Patchback"), ("Number1", "Ripplefluke"),
    ("Oscar", "Patchback"),
    ("PL", "Quasi"), ("PL", "Ripplefluke"), ("PL", "Scabs"), ("PL", "TR120"),
    ("Quasi", "SN100"), ("Quasi", "Ripplefluke"),
    ("Ripplefluke", "Scabs"), ("Ripplefluke", "Shmuddel"),
    ("Scabs", "Shmuddel"), ("Scabs", "TR120"),
    ("SN63", "SN89"), ("SN63", "Wave"),
    ("SN89", "Wave"),
    ("SN9", "Stripes"),
    ("SN90", "SN96"), ("SN96", "TR120"),
    ("Stripes", "TR82"),
    ("Thumper", "Topless"), ("Thumper", "TR77"),
    ("Topless", "TR120"), ("Topless", "TR77"),
    ("TR120", "TR99"),
    ("TR77", "TR82"), ("TR77", "TR88"),
    ("TR82", "TR88"), ("TR88", "TR99"),
    ("Trigger", "Zipfel"),
    ("TSN103", "TSN83"), ("TSN83", "Upbang"),
    ("Upbang", "Vau"), ("Upbang", "Web"),
    ("Vau", "Wave"), ("Vau", "Web"),
    ("Wave", "Web"),
    ("Whitetip", "Zap"), ("Whitetip", "Zipfel"),
    ("Zap", "Zipfel"),
]


# ============================================================
# SCORING (same as dolphin_resonance.py)
# ============================================================

def network_resonance(G):
    """Average resonance score across all nodes."""
    btw = nx.betweenness_centrality(G)
    deg = nx.degree_centrality(G)
    scores = []
    
    for node in G.nodes():
        neighbors = list(G.neighbors(node))
        
        # Social rhythm
        rhythm = deg[node]
        
        # Connection coherence
        if len(neighbors) < 2:
            coherence = 0.0
        else:
            subgraph = G.subgraph(neighbors)
            possible = len(neighbors) * (len(neighbors) - 1) / 2
            actual = subgraph.number_of_edges()
            coherence = actual / possible if possible > 0 else 0.0
        
        # Bridge complexity
        bridge = btw[node]
        
        score = (rhythm * 0.4) + (coherence * 0.4) + (bridge * 0.2)
        scores.append(score)
    
    return sum(scores) / len(scores)


def scramble_network(nodes, edges, seed=None):
    """
    Build a random network with same node count and edge count.
    Edges assigned randomly — no biological structure.
    """
    if seed:
        random.seed(seed)
    
    G = nx.Graph()
    G.add_nodes_from(nodes)
    
    node_list = list(nodes)
    edge_count = len(edges)
    
    added = 0
    attempts = 0
    while added < edge_count and attempts < edge_count * 10:
        a = random.choice(node_list)
        b = random.choice(node_list)
        if a != b and not G.has_edge(a, b):
            G.add_edge(a, b)
            added += 1
        attempts += 1
    
    return G


# ============================================================
# RUN THE TEST
# ============================================================

print("\n🐬 NULL CASE VALIDATION — Dolphin Resonance Tool")
print("=" * 58)
print("Question: Does the tool score real networks higher than random?")
print("Method:   100 scrambled networks, same nodes + edge count")
print("=" * 58)

# Real network
G_real = nx.Graph()
G_real.add_nodes_from(DOLPHINS)
G_real.add_edges_from(EDGES)
real_score = network_resonance(G_real)

print(f"\n📊 REAL NETWORK")
print(f"   Nodes: {G_real.number_of_nodes()}")
print(f"   Edges: {G_real.number_of_edges()}")
print(f"   Resonance score: {real_score:.6f}")

# Scrambled networks
print(f"\n🔀 RUNNING 100 SCRAMBLED NETWORKS...")
scrambled_scores = []
for i in range(100):
    G_rand = scramble_network(DOLPHINS, EDGES, seed=i)
    score = network_resonance(G_rand)
    scrambled_scores.append(score)

avg_scrambled = statistics.mean(scrambled_scores)
std_scrambled = statistics.stdev(scrambled_scores)
min_scrambled = min(scrambled_scores)
max_scrambled = max(scrambled_scores)

# How many scrambled networks beat the real one?
beat_real = sum(1 for s in scrambled_scores if s >= real_score)
percentile = 100 - beat_real

print(f"\n📊 SCRAMBLED NETWORK RESULTS (n=100)")
print(f"   Average score:  {avg_scrambled:.6f}")
print(f"   Std deviation:  {std_scrambled:.6f}")
print(f"   Min score:      {min_scrambled:.6f}")
print(f"   Max score:      {max_scrambled:.6f}")

print(f"\n📊 DISCRIMINATION RESULT")
print(f"   Real network score:     {real_score:.6f}")
print(f"   Scrambled average:      {avg_scrambled:.6f}")
print(f"   Difference:             {real_score - avg_scrambled:+.6f}")
print(f"   Networks beating real:  {beat_real}/100")
print(f"   Real network percentile: {percentile}th")

separation = (real_score - avg_scrambled) / std_scrambled
print(f"   Separation (std devs):  {separation:.2f}σ")

print(f"\n🔬 VERDICT")
if beat_real <= 5:
    print(f"   ✅ VALIDATED: Real network scores in top {100-percentile}% of random")
    print(f"   The tool discriminates. Biological structure produces measurably")
    print(f"   different resonance than random edge assignment.")
elif beat_real <= 15:
    print(f"   ⚠️  PARTIAL: Real network scores above average but not strongly")
    print(f"   Consider weight adjustment or additional metrics.")
else:
    print(f"   ❌ NOT VALIDATED: Random networks frequently match real score")
    print(f"   Tool may not be measuring biological structure specifically.")

print(f"\n   Grin's score in real network: ", end="")
btw_real = nx.betweenness_centrality(G_real)
deg_real = nx.degree_centrality(G_real)
neighbors = list(G_real.neighbors("Grin"))
rhythm = deg_real["Grin"]
subgraph = G_real.subgraph(neighbors)
possible = len(neighbors) * (len(neighbors) - 1) / 2
actual = subgraph.number_of_edges()
coherence = actual / possible if possible > 0 else 0.0
bridge = btw_real["Grin"]
grin_score = (rhythm * 0.4) + (coherence * 0.4) + (bridge * 0.2)
print(f"{grin_score:.6f}")
print(f"   Grin connections: {G_real.degree('Grin')}")
print(f"   Grin betweenness: {bridge:.4f}")

print(f"\n💜 Built by: Barbara J. Keiser + Claude")
print(f"   Universal Resonance Tool — Null Case Validation")
print(f"   February 2026\n")
