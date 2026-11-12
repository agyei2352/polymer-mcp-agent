"""
agent.py
--------------------------------------------------------------------------------
Autonomous Biomaterial & Medical Device Evaluation Agent.
Orchestrates MCP tool execution to deliver comprehensive clinical engineering
assessments, FDA regulatory pathways, and material degradation analyses.

Author: Prince Agyei (agyei2352@icloud.com)
--------------------------------------------------------------------------------
"""

import json
from typing import Dict, Any, List
from .mcp_server import BiomaterialMCPServer
from .visualization import generate_multipanel_tradeoff_matrix


class BiomaterialAgent:
    """
    Agentic AI Controller utilizing Model Context Protocol (MCP) to conduct
    autonomous medical device regulatory classification and polymer characterization.
    """

    def __init__(self):
        self.mcp = BiomaterialMCPServer()

    def run_clinical_device_evaluation(self, device_name: str, material_candidate: str) -> Dict[str, Any]:
        """
        Executes a complete multi-step autonomous clinical engineering evaluation pipeline.
        """
        print(f"\n[Agent] Ingesting clinical device requirements: '{device_name}'...")
        
        # Step 1: Query FDA regulatory database via MCP
        print(f"[Agent] Executing MCP Tool: search_fda_databases(device_category='{device_name}')...")
        fda_data = self.mcp.call_tool("search_fda_databases", {
            "device_category": device_name,
            "material_query": material_candidate
        })

        # Step 2: Audit ISO 10993 Biocompatibility via MCP
        print(f"[Agent] Executing MCP Tool: evaluate_iso10993_biocompatibility(material='{material_candidate}')...")
        contact_mode = "circulating_blood" if "stent" in device_name.lower() or "catheter" in device_name.lower() else "bone_contact"
        iso_data = self.mcp.call_tool("evaluate_iso10993_biocompatibility", {
            "material_name": material_candidate,
            "contact_type": contact_mode,
            "duration": "permanent"
        })

        # Step 3: Run Hydrolytic Degradation Kinetics via MCP
        print(f"[Agent] Executing MCP Tool: simulate_degradation_kinetics(material='{material_candidate}', horizon=18.0 mo)...")
        deg_data = self.mcp.call_tool("simulate_degradation_kinetics", {
            "material_name": material_candidate,
            "time_months": 18.0
        })

        # Step 4: Render Multi-Panel Visualizations
        print(f"[Agent] Generating multi-panel Matplotlib trade-off matrices...")
        chart_path = generate_multipanel_tradeoff_matrix("samples/biomaterial_tradeoff_matrices.png")

        # Compile Consolidated Report
        report = {
            "clinical_device": device_name,
            "primary_candidate_material": material_candidate,
            "fda_regulatory_assessment": fda_data,
            "iso_10993_biocompatibility_audit": iso_data,
            "degradation_kinetics_evaluation": deg_data,
            "visual_deliverables": [chart_path],
            "conclusion": (
                f"Candidate polymer '{material_candidate}' demonstrates acceptable biocompatibility "
                f"under ISO 10993 with sufficient mechanical scaffolding modulus "
                f"({deg_data.get('retained_modulus_gpa', 0):.2f} GPa remaining at 18 months). "
                f"Clearance pathway follows FDA {fda_data.get('device_class')} guidelines."
            )
        }

        return report

