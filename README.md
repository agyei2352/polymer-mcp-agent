# Autonomous Biomaterial & Medical Device Evaluation Agent

> [!NOTE]
> ### Engineering Portfolio & Technical Archive Notice
> **Development Context:** This project was engineered and validated as an academic and R&D milestone in Biomedical Engineering and Agentic AI at the University of North Texas.  
> **Toolchain:** Primary agent logic, Model Context Protocol (MCP) servers, and scientific plotting pipelines were developed locally in **Python / VS Code**, integrating real-world FDA device regulatory standards and ISO 10993 biocompatibility specifications.  
> **Repository Purpose:** This repository serves as an **external public portfolio and verification archive** for engineering recruiters, hiring managers, and interviewers to inspect the architecture, source code, mathematical kinetics models, and clinical evaluation deliverables.

---

## System Overview

Medical device engineers evaluating new candidate polymers for implantable devices face complex multi-objective optimization challenges: balancing **mechanical load-bearing capacity**, **in vivo hydrolytic degradation kinetics**, **ISO 10993 biological safety**, and **FDA regulatory clearance pathways**.

This autonomous agent leverages the **Model Context Protocol (MCP)** to orchestrate specialized biomedical tools:
1. **Regulatory Intelligence:** Ingests FDA PMA / 510(k) predicate classifications for Class II and Class III implants.
2. **Biocompatibility Auditing:** Assesses ISO 10993 requirements (cytotoxicity, hemocompatibility, genotoxicity, systemic toxicity).
3. **Degradation Modeling:** Simulates in vivo polymer chain scission ($M_n(t)$) and time-dependent Young's modulus retention ($E(t)$).
4. **Clinical Trade-Off Visualization:** Automatically renders multi-panel **Matplotlib** matrices comparing structural performance against bioresorption lifespans.

```
+-------------------------------------------------------------------------------------------------+
|                                 SYSTEM ARCHITECTURE FLOWCHART                                   |
+-------------------------------------------------------------------------------------------------+
|                                                                                                 |
|   +---------------------------------------+                                                     |
|   |   Clinical Query / Device Request     |                                                     |
|   |   (e.g., "Coronary Stent with PLLA")  |                                                     |
|   +---------------------------------------+                                                     |
|                       |                                                                         |
|                       v                                                                         |
|   +---------------------------------------+                                                     |
|   |         Biomaterial Agent             |  <--- Orchestrator (src/agent.py)                   |
|   +---------------------------------------+                                                     |
|                       |                                                                         |
|        +--------------+--------------+-------------------+                                      |
|        | (MCP Tool Call)             | (MCP Tool Call)   | (MCP Tool Call)                      |
|        v                             v                   v                                      |
|   +----------------------+    +--------------------+    +----------------------------------+    |
|   | search_fda_databases |    | evaluate_iso10993  |    | simulate_degradation_kinetics    |    |
|   | (PMA/510k Guidance)  |    | (Biological Safety)|    | (Hydrolysis & Modulus Loss)      |    |
|   +----------------------+    +--------------------+    +----------------------------------+    |
|        |                             |                   |                                      |
|        +--------------+--------------+-------------------+                                      |
|                       |                                                                         |
|                       v                                                                         |
|   +-----------------------------------------------------------------------------------------+   |
|   |                              Multi-Panel Trade-Off Engine                               |   |
|   |                 (Matplotlib Kinetics, Modulus, Bubble Matrix, Viability)                |   |
|   +-----------------------------------------------------------------------------------------+   |
|                       |                                                                         |
|                       v                                                                         |
|   +-----------------------------------------------------------------------------------------+   |
|   |                   Templated Clinical Engineering Evaluation Report                      |   |
|   |                   (samples/stent_evaluation_report.json & visuals)                      |   |
|   +-----------------------------------------------------------------------------------------+   |
+-------------------------------------------------------------------------------------------------+
```

---

## Evaluated Biomaterials Library

The agent analyzes key engineering polymers across three primary clinical device classes:

| Polymer | Full Name | Polymer Family | Initial Modulus ($E_0$) | Tensile Strength | Degradation Half-Life | Primary Clinical Target |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PLLA** | Poly-L-lactic acid | Aliphatic Polyester | $3.5\text{ GPa}$ | $65.0\text{ MPa}$ | $19.8\text{ months}$ | FDA Class III Bioresorbable Vascular Stents (BVS) |
| **PDLLA** | Poly-D,L-lactic acid | Amorphous Polyester | $2.1\text{ GPa}$ | $45.0\text{ MPa}$ | $6.0\text{ months}$ | Drug-Eluting Stent (DES) Antiproliferative Coatings |
| **PEEK** | Polyether ether ketone | Polyaryletherketone | $3.8\text{ GPa}$ | $98.0\text{ MPa}$ | $>100\text{ years}$ (Biostable) | FDA Class III Interbody Spinal Fusion Cages |
| **TPU** | Thermoplastic Polyurethane | Polycarbonate-Urethane | $0.08\text{ GPa}$ | $38.0\text{ MPa}$ | $>40\text{ years}$ (Biostable) | FDA Class II/III Central Venous Access Catheters |

---

## Mathematical Kinetics & Mechanics Modeling

Hydrolytic chain scission of aliphatic polyesters (PLLA/PDLLA) in saline aqueous environments ($\text{pH } 7.4$, $37^\circ\text{C}$) is modeled via first-order ester cleavage kinetics:

$$M_n(t) = M_{n,0} \cdot e^{-k_{\text{deg}} \cdot t}$$

As polymer molecular weight degrades, mechanical load-bearing capacity decays non-linearly:

$$E(t) = E_0 \cdot \left(\frac{M_n(t)}{M_{n,0}}\right)^{1.25}$$

Where:
- $M_{n,0}$ = Initial number-average molecular weight
- $k_{\text{deg}}$ = Hydrolytic degradation rate constant ($\text{month}^{-1}$)
- $E_0$ = Initial Young's modulus ($\text{GPa}$)
- $E(t)$ = Retained modulus maintaining vessel lumen scaffolding during neointimal healing

---

## Repository Directory Structure

```text
polymer-mcp-agent/
├── .gitignore                     # Ignores __pycache__, venvs, logs
├── LICENSE                        # All Rights Reserved (Portfolio Inspection Only)
├── README.md                      # Master architecture & evaluation documentation
├── requirements.txt               # Dependencies (mcp, matplotlib, pandas, numpy)
├── main.py                        # Executable CLI demonstrating the evaluation pipeline
├── src/
│   ├── __init__.py                # Package exports
│   ├── agent.py                   # High-level agentic orchestration controller
│   ├── mcp_server.py              # Model Context Protocol tools & schemas
│   ├── biomaterials.py            # Material catalog, kinetics equations & ISO 10993 rules
│   └── visualization.py           # Multi-panel Matplotlib trade-off generator
└── samples/                       # Generated evaluation outputs
    ├── stent_evaluation_report.json       # PLLA coronary stent assessment
    ├── spinal_cage_evaluation_report.json # PEEK orthopedic cage assessment
    └── biomaterial_tradeoff_matrices.png  # Multi-panel kinetics & trade-off figure
```

---

## How to Review & Execute

### 1. Inspect Sample Deliverables
- **Review Sample Clinical Report:** Open [`samples/stent_evaluation_report.json`](samples/stent_evaluation_report.json) to inspect the structured FDA classification and ISO 10993 audit output.
- **Inspect MCP Server Implementation:** View [`src/mcp_server.py`](src/mcp_server.py) to review how MCP tools (`search_fda_databases`, `evaluate_iso10993_biocompatibility`, `simulate_degradation_kinetics`) are registered and called.

### 2. Local Execution
To run the automated agent pipeline locally:
```bash
# Clone the repository
git clone https://github.com/princeagyei/polymer-mcp-agent.git
cd polymer-mcp-agent

# Install dependencies
pip install -r requirements.txt

# Execute the agent
python main.py
```

---

## License & Intellectual Property

Copyright &copy; 2026 Prince Agyei. All Rights Reserved.  
This software and associated clinical models are published strictly for recruiter portfolio review and academic verification. Unauthorized copying, modification, commercial distribution, or deployment is strictly prohibited. See [`LICENSE`](LICENSE) for complete terms.

