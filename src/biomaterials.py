"""
biomaterials.py
--------------------------------------------------------------------------------
Biomedical material domain models, ISO 10993 assessment logic, and
hydrolytic degradation kinetics modeling for cardiovascular, orthopedic,
and vascular medical devices.

Author: Prince Agyei (agyei2352@icloud.com)
Portfolio Project: Autonomous Biomaterial & Medical Device Evaluation Agent
--------------------------------------------------------------------------------
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import numpy as np


@dataclass
class BiomaterialProfile:
    name: str
    chemical_formula: str
    polymer_family: str
    initial_youngs_modulus_gpa: float
    tensile_strength_mpa: float
    glass_transition_temp_c: float
    melting_temp_c: float
    crystallinity_percent: float
    hydrolytic_deg_rate_k: float  # month^-1
    degradation_half_life_months: float
    fda_device_class: str
    primary_clinical_applications: List[str]
    iso_10993_compliance: Dict[str, str] = field(default_factory=dict)


# Benchmark biomaterial database calibrated from biomaterials literature
BIOMATERIAL_CATALOG: Dict[str, BiomaterialProfile] = {
    "PLLA": BiomaterialProfile(
        name="Poly-L-lactic acid (PLLA)",
        chemical_formula="(C3H4O2)n",
        polymer_family="Biodegradable Aliphatic Polyester",
        initial_youngs_modulus_gpa=3.5,
        tensile_strength_mpa=65.0,
        glass_transition_temp_c=62.0,
        melting_temp_c=175.0,
        crystallinity_percent=37.0,
        hydrolytic_deg_rate_k=0.035,
        degradation_half_life_months=19.8,
        fda_device_class="Class III",
        primary_clinical_applications=[
            "Bioresorbable Vascular Scaffolds (BVS)",
            "Orthopedic Bone Interference Screws",
            "Ligament Reconstruction Pins"
        ],
        iso_10993_compliance={
            "Part 3 (Genotoxicity)": "Pass (Non-mutagenic)",
            "Part 4 (Hemocompatibility)": "Pass (Low thrombogenicity)",
            "Part 5 (In vitro Cytotoxicity)": "Pass (L929 >85% viability)",
            "Part 10 (Irritation & Sensitization)": "Pass (Zero erythema score)",
            "Part 11 (Systemic Toxicity)": "Pass (No acute systemic reaction)"
        }
    ),
    "PDLLA": BiomaterialProfile(
        name="Poly-D,L-lactic acid (PDLLA)",
        chemical_formula="(C3H4O2)n [Amorphous Racemic]",
        polymer_family="Biodegradable Aliphatic Polyester",
        initial_youngs_modulus_gpa=2.1,
        tensile_strength_mpa=45.0,
        glass_transition_temp_c=53.0,
        melting_temp_c=0.0,  # Amorphous
        crystallinity_percent=0.0,
        hydrolytic_deg_rate_k=0.115,
        degradation_half_life_months=6.0,
        fda_device_class="Class III",
        primary_clinical_applications=[
            "Drug-Eluting Stent (DES) Polymer Coatings",
            "Controlled Drug Delivery Microcapsules",
            "Suture Anchors"
        ],
        iso_10993_compliance={
            "Part 3 (Genotoxicity)": "Pass (Non-mutagenic)",
            "Part 4 (Hemocompatibility)": "Pass (Acceptable for DES coatings)",
            "Part 5 (In vitro Cytotoxicity)": "Pass (L929 >80% viability)",
            "Part 10 (Irritation & Sensitization)": "Pass (Zero sensitization)",
            "Part 11 (Systemic Toxicity)": "Pass (No acute systemic reaction)"
        }
    ),
    "PEEK": BiomaterialProfile(
        name="Polyether ether ketone (PEEK)",
        chemical_formula="(C19H12O3)n",
        polymer_family="High-Performance Polyaryletherketone",
        initial_youngs_modulus_gpa=3.8,  # Close to human cortical bone (3-20 GPa)
        tensile_strength_mpa=98.0,
        glass_transition_temp_c=143.0,
        melting_temp_c=343.0,
        crystallinity_percent=33.0,
        hydrolytic_deg_rate_k=0.0001,  # Non-resorbable biostable
        degradation_half_life_months=1200.0,
        fda_device_class="Class III",
        primary_clinical_applications=[
            "Interbody Spinal Fusion Cages",
            "Craniomaxillofacial Implants",
            "Orthopedic Joint Arthroplasty"
        ],
        iso_10993_compliance={
            "Part 3 (Genotoxicity)": "Pass (Ames test negative)",
            "Part 4 (Hemocompatibility)": "Pass (Implant non-hemolytic)",
            "Part 5 (In vitro Cytotoxicity)": "Pass (L929 >95% viability)",
            "Part 10 (Irritation & Sensitization)": "Pass (Zero irritation)",
            "Part 11 (Systemic Toxicity)": "Pass (Biostable non-toxic)"
        }
    ),
    "TPU": BiomaterialProfile(
        name="Thermoplastic Polyurethane (TPU - Polycarbonate-based)",
        chemical_formula="[C25H28N2O7]n",
        polymer_family="Elastomeric Thermoplastic Copolymer",
        initial_youngs_modulus_gpa=0.08,  # Highly compliant
        tensile_strength_mpa=38.0,
        glass_transition_temp_c=-35.0,
        melting_temp_c=190.0,
        crystallinity_percent=12.0,
        hydrolytic_deg_rate_k=0.0012,
        degradation_half_life_months=577.0,
        fda_device_class="Class II/III",
        primary_clinical_applications=[
            "Central Venous Catheters (CVC)",
            "Vascular Access Ports",
            "Cardiac Pacemaker Lead Insulation"
        ],
        iso_10993_compliance={
            "Part 3 (Genotoxicity)": "Pass (Non-mutagenic)",
            "Part 4 (Hemocompatibility)": "Pass (Non-thrombogenic, ISO 10993-4)",
            "Part 5 (In vitro Cytotoxicity)": "Pass (L929 >90% viability)",
            "Part 10 (Irritation & Sensitization)": "Pass (Non-sensitizing)",
            "Part 11 (Systemic Toxicity)": "Pass (Biostable elastomer)"
        }
    )
}


def compute_hydrolytic_degradation_profile(material_key: str, time_months_array: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Computes time-dependent molecular weight loss and mechanical modulus retention:
    M_n(t) = M_{n,0} * exp(-k * t)
    E(t) = E_0 * (M_n(t) / M_{n,0})^1.2
    """
    if material_key not in BIOMATERIAL_CATALOG:
        raise ValueError(f"Unknown biomaterial: {material_key}")

    profile = BIOMATERIAL_CATALOG[material_key]
    k = profile.hydrolytic_deg_rate_k
    E0 = profile.initial_youngs_modulus_gpa

    # Fraction of molecular weight remaining
    molecular_weight_fraction = np.exp(-k * time_months_array)
    # Young's modulus retention curve (mechanics degrade non-linearly with chain scission)
    retained_modulus_gpa = E0 * np.power(molecular_weight_fraction, 1.25)

    return {
        "time_months": time_months_array,
        "mw_fraction_percent": molecular_weight_fraction * 100.0,
        "modulus_gpa": retained_modulus_gpa
    }

