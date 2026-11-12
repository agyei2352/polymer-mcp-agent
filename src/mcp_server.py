"""
mcp_server.py
--------------------------------------------------------------------------------
Model Context Protocol (MCP) Server for Medical Device & Biomaterial Analysis.
Exposes standardized MCP Tools and Resources to LLM agents for automated
regulatory classification, ISO 10993 assessment, and degradation modeling.

Author: Prince Agyei (agyei2352@icloud.com)
--------------------------------------------------------------------------------
"""

import json
from typing import Dict, Any, List
from .biomaterials import BIOMATERIAL_CATALOG, compute_hydrolytic_degradation_profile


class BiomaterialMCPServer:
    """
    Standard Model Context Protocol (MCP) compliant server providing 
    biomaterial engineering and FDA regulatory intelligence tools.
    """

    def __init__(self):
        self.name = "biomaterial-device-evaluator"
        self.version = "1.0.0"

    def list_tools(self) -> List[Dict[str, Any]]:
        """Returns the list of available MCP tools and JSON schemas."""
        return [
            {
                "name": "search_fda_databases",
                "description": "Searches FDA PMA/510(k) databases for predicate Class II/III medical devices and biomaterial classifications.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "device_category": {
                            "type": "string",
                            "description": "Clinical device category (e.g., 'cardiovascular stent', 'spinal fusion cage', 'catheter')"
                        },
                        "material_query": {
                            "type": "string",
                            "description": "Polymer or biomaterial (e.g., 'PLLA', 'PEEK', 'TPU')"
                        }
                    },
                    "required": ["device_category"]
                }
            },
            {
                "name": "evaluate_iso10993_biocompatibility",
                "description": "Performs an ISO 10993 regulatory compliance audit for medical devices based on patient contact duration and tissue category.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "material_name": {
                            "type": "string",
                            "description": "Polymer key: 'PLLA', 'PDLLA', 'PEEK', or 'TPU'"
                        },
                        "contact_type": {
                            "type": "string",
                            "description": "Tissue contact: 'circulating_blood', 'bone_contact', 'mucosal_membrane'"
                        },
                        "duration": {
                            "type": "string",
                            "description": "Contact duration: 'limited' (<24h), 'prolonged' (24h-30d), 'permanent' (>30d)"
                        }
                    },
                    "required": ["material_name", "contact_type"]
                }
            },
            {
                "name": "simulate_degradation_kinetics",
                "description": "Models in vivo hydrolytic degradation kinetics and structural mechanical modulus retention over time.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "material_name": {"type": "string"},
                        "time_months": {"type": "number", "description": "Simulation horizon in months"}
                    },
                    "required": ["material_name"]
                }
            }
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches an MCP tool call to the appropriate internal routine."""
        if name == "search_fda_databases":
            return self._search_fda(arguments.get("device_category", ""), arguments.get("material_query", ""))
        elif name == "evaluate_iso10993_biocompatibility":
            return self._evaluate_biocompatibility(
                arguments.get("material_name", ""),
                arguments.get("contact_type", ""),
                arguments.get("duration", "permanent")
            )
        elif name == "simulate_degradation_kinetics":
            return self._simulate_degradation(
                arguments.get("material_name", ""),
                float(arguments.get("time_months", 24.0))
            )
        else:
            raise ValueError(f"Tool '{name}' not found on MCP Server '{self.name}'.")

    def _search_fda(self, device_category: str, material_query: str) -> Dict[str, Any]:
        """Simulated FDA database retrieval based on historical PMA/510(k) clearances."""
        category = device_category.lower()
        if "stent" in category or "cardio" in category:
            return {
                "fda_panel": "Cardiovascular (CV)",
                "device_class": "Class III (PMA Required)",
                "predicate_devices": [
                    {"product_name": "Abbott Absorb GT1 BVS", "pma_number": "P150023", "material": "PLLA backbone with PDLLA/everolimus coating"},
                    {"product_name": "Biotronik Magmaris", "clearance": "CE Mark predicate", "material": "Magnesium/PLLA hybrid"}
                ],
                "regulatory_guidance": "FDA Non-Clinical Engineering Tests for Bioresorbable Vascular Scaffolds (2020 Guidance)",
                "key_concerns": ["Late scaffold thrombosis", "Recoil resistance", "Radial force maintenance during vascular remodeling"]
            }
        elif "spinal" in category or "ortho" in category:
            return {
                "fda_panel": "Orthopedic and Physical Medicine (OR)",
                "device_class": "Class II / III (510(k) or PMA)",
                "predicate_devices": [
                    {"product_name": "Medtronic Capstone PEEK", "k_number": "K072995", "material": "PEEK (ASTM F2026)"},
                    {"product_name": "Stryker AVS PEEK Spacer", "k_number": "K090623", "material": "Radiolucent PEEK-OPTIMA"}
                ],
                "regulatory_guidance": "Class II Special Controls Guidance: Intervertebral Body Fusion Device",
                "key_concerns": ["Subsidence into vertebral endplates", "Modulus mismatch (stress shielding)", "Osseointegration"]
            }
        else:
            return {
                "fda_panel": "General Hospital / Vascular Access",
                "device_class": "Class II (510(k))",
                "predicate_devices": [
                    {"product_name": "BD PowerPICC Catheter", "k_number": "K063628", "material": "Aromatic Polycarbonate-Polyurethane (TPU)"}
                ],
                "regulatory_guidance": "Guidance on Premarket Notification [510(k)] Submissions for Short-Term and Long-Term Intravascular Catheters",
                "key_concerns": ["Hemolysis", "Thrombosis", "Flex fatigue resistance"]
            }

    def _evaluate_biocompatibility(self, material_name: str, contact_type: str, duration: str) -> Dict[str, Any]:
        """Evaluates ISO 10993 biological safety requirements."""
        key = material_name.upper()
        if key not in BIOMATERIAL_CATALOG:
            return {"error": f"Material '{material_name}' not cataloged."}

        profile = BIOMATERIAL_CATALOG[key]
        return {
            "material": profile.name,
            "iso_10993_1_categorization": f"{contact_type.title()} - {duration.title()} Contact (>30 days)",
            "compliance_summary": profile.iso_10993_compliance,
            "required_standard_tests": [
                "ISO 10993-3: Genotoxicity, Carcinogenicity, and Reproductive Toxicity",
                "ISO 10993-4: Hemocompatibility Interactions with Blood",
                "ISO 10993-5: In Vitro Cytotoxicity Assays",
                "ISO 10993-10: Tests for Skin Sensitization and Irritation",
                "ISO 10993-11: Systemic Toxicity Evaluations",
                "ISO 10993-13/15: Identification and Quantification of Degradation Products"
            ],
            "recommendation": "Complies with biological evaluation safety parameters for FDA premarket notification."
        }

    def _simulate_degradation(self, material_name: str, time_months: float) -> Dict[str, Any]:
        """Calculates degradation metrics at a specific time point."""
        key = material_name.upper()
        if key not in BIOMATERIAL_CATALOG:
            return {"error": f"Material '{material_name}' not cataloged."}

        import numpy as np
        t_arr = np.array([time_months])
        res = compute_hydrolytic_degradation_profile(key, t_arr)

        return {
            "material": BIOMATERIAL_CATALOG[key].name,
            "time_horizon_months": time_months,
            "remaining_mw_percent": float(res["mw_fraction_percent"][0]),
            "retained_modulus_gpa": float(res["modulus_gpa"][0]),
            "initial_modulus_gpa": BIOMATERIAL_CATALOG[key].initial_youngs_modulus_gpa,
            "status": "Resorbing" if BIOMATERIAL_CATALOG[key].hydrolytic_deg_rate_k > 0.005 else "Biostable"
        }

