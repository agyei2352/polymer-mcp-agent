#!/usr/bin/env python3
"""
main.py
--------------------------------------------------------------------------------
CLI Demonstration of the Autonomous Biomaterial & Medical Device Evaluation Agent.
Ingests clinical targets, routes queries through MCP tools, and exports
clinical engineering assessment reports and trade-off visualizations.

Author: Prince Agyei (agyei2352@icloud.com)
Portfolio Project: Autonomous Biomaterial & Medical Device Evaluation Agent
--------------------------------------------------------------------------------
"""

import os
import json
import sys
from src.agent import BiomaterialAgent
from src.visualization import generate_multipanel_tradeoff_matrix


def main():
    print("=" * 80)
    print(" AUTONOMOUS BIOMATERIAL & MEDICAL DEVICE EVALUATION AGENT")
    print(" Built with Python, Model Context Protocol (MCP) & Matplotlib")
    print(" Author: Prince Agyei | University of North Texas")
    print("=" * 80)

    agent = BiomaterialAgent()

    # Benchmark Target 1: FDA Class III Bioresorbable Vascular Scaffold
    stent_report = agent.run_clinical_device_evaluation(
        device_name="Bioresorbable Vascular Coronary Scaffold",
        material_candidate="PLLA"
    )

    # Save Sample Report to disk
    sample_json_path = os.path.join("samples", "stent_evaluation_report.json")
    with open(sample_json_path, "w") as f:
        json.dump(stent_report, f, indent=2)
    print(f"\n[Success] Clinical assessment exported to: {sample_json_path}")

    # Generate Full Multi-Panel Trade-Off Matrices
    chart_path = generate_multipanel_tradeoff_matrix(os.path.join("samples", "biomaterial_tradeoff_matrices.png"))
    print(f"[Success] Matplotlib 4-panel trade-off matrix generated: {chart_path}")

    # Print Executive Assessment
    print("\n" + "-" * 80)
    print(" EXECUTIVE CLINICAL ENGINEERING SUMMARY")
    print("-" * 80)
    print(f"Device Target:           {stent_report['clinical_device']}")
    print(f"Evaluated Polymer:       {stent_report['primary_candidate_material']}")
    print(f"FDA Regulatory Panel:    {stent_report['fda_regulatory_assessment']['fda_panel']}")
    print(f"Device Classification:   {stent_report['fda_regulatory_assessment']['device_class']}")
    print(f"ISO 10993 Contact:       {stent_report['iso_10993_biocompatibility_audit']['iso_10993_1_categorization']}")
    print(f"18-Month Modulus Ret.:   {stent_report['degradation_kinetics_evaluation']['retained_modulus_gpa']:.2f} GPa")
    print(f"Conclusion:              {stent_report['conclusion']}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()

