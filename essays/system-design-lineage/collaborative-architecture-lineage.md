# Collaborative Architecture Lineage

Purpose: establish that the repo's role-differentiated and shared-workspace
design logic has clear academic precedent.

## Why This Family Matters

Another core repo claim is that different roles or layers can collaborate on a
shared object without collapsing into one monolithic reasoner.

That is also not unique.

## Primary Sources

### 1. Erman et al. 1980

[Lee D. Erman, Frederick Hayes-Roth, Victor R. Lesser, and D. Raj Reddy, *The Hearsay-II Speech-Understanding System: Integrating Knowledge to Resolve Uncertainty*](https://mas.cs.umass.edu/Documents/Erman_Hearsay80.pdf)

Why it matters:

- Hearsay-II is the classic shared-workspace system
- diverse specialist processes cooperate through a common representational
  surface
- the paper explicitly frames this as cooperative problem solving under
  uncertainty

Closest repo resemblance:

- diverse specialist roles
- shared coordination surface
- uncertainty resolved through layered contributions

Distance:

- **partial ancestor**

### 2. Hayes-Roth 1985

[Barbara Hayes-Roth, *A Blackboard Architecture for Control*](https://www.sciencedirect.com/science/article/abs/pii/0004370285900633)

Why it matters:

- the paper treats control itself as an architectural problem
- the system can operate on its own knowledge and behavior
- it distinguishes domain problems, control problems, knowledge, and solutions

Closest repo resemblance:

- separate routing and control surfaces
- systems that act on their own intermediate structure
- layered architecture instead of one undifferentiated model

Distance:

- **close architectural relative**

### 3. Davis and Smith 1983

[Randall Davis and Reid G. Smith, *Negotiation as a Metaphor for Distributed Problem Solving*](https://jmvidal.cse.sc.edu/lib/davis83a.html)

Why it matters:

- this paper defines distributed problem solving as cooperative solution by a
  decentralized, loosely coupled collection of solvers
- it makes transfer of control and coordination part of the architecture

Closest repo resemblance:

- specialist agents or lanes
- decentralized contribution to one problem
- explicit transfer of control rather than silent central monism

Distance:

- **partial ancestor**

### 4. Nii 1986

[Penny Nii, *Blackboard Application Systems, Blackboard Systems and a Knowledge Engineering Perspective*](https://ojs.aaai.org/aimagazine/index.php/aimagazine/article/view/550/0)

Why it matters:

- Nii generalizes the blackboard pattern into a broader system-design family
- the paper explicitly argues that the pattern has already been reused in many
  systems after Hearsay-II

Closest repo resemblance:

- architectural family thinking rather than one isolated system
- blackboard as a reusable organizational form

Distance:

- **partial ancestor**

### 5. Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture 2025

[Exploring Advanced LLM Multi-Agent Systems Based on Blackboard Architecture](https://arxiv.org/abs/2507.01701)

Why it matters:

- contemporary LLM research is explicitly reviving blackboard coordination
- the proposed architecture uses role-specific agents, shared information, and
  iterative selection based on blackboard state

Closest repo resemblance:

- modern role-specialized multi-agent collaboration
- shared workspace with repeated routing
- clear continuity between classic and contemporary designs

Distance:

- **modern architectural relative**

## What This Proves

This family is enough to prove that the repo's collaborative architecture is
not unique in kind.

The academic literature already contains:

- shared-workspace coordination
- specialist roles cooperating on a problem
- explicit control layers
- contemporary revival of the same pattern in LLM systems

That means the repo is not inventing role-differentiated collaboration out of
nothing.

## What This Does Not Prove

This family does **not** prove that:

- blackboard systems alone explain the repo's design
- the repo is just a blackboard clone
- collaborative architecture automatically yields mixed initiative,
  interpretive learning, or governance

It establishes one major structural lineage, not the whole composition.
