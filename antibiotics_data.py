antibiotics_data = {
    "Neonates": {
        "Ampicillin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [300, 300],
                "max_day": None,
                "notes": "Starter placeholder for neonatal workflows."
            }
        ],
        "Gentamicin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [5, 7.5],
                "notes": "Starter placeholder for neonatal workflows."
            }
        ],
        "Acyclovir": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [30, 60],
                "notes": "Starter placeholder. Neonatal dosing depends on age and indication."
            }
        ]
    },

    "Neuro": {
        "Ceftriaxone": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [100, 100],
                "max_dose": 2000,
                "max_day": 4000,
                "notes": "CNS use."
            }
        ],
        "Metronidazole": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [30, 30],
                "max_day": 4000,
                "notes": "CNS use."
            }
        ],
        "Cloxacillin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [200, 200],
                "max_dose": 2000,
                "max_day": 12000,
                "notes": "Neuro use."
            }
        ],
        "Vancomycin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [30, 60],
                "max_dose": 500,
                "max_day": 2000,
                "notes": "<12yo: 15mg/kg/dose Q6H; ≥12yo: 20mg/kg/dose Q8H."
            }
        ],
        "Acyclovir": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [30, 45],
                "notes": "Age-specific CNS dosing varies."
            }
        ]
    },

    "Dental / ENT": {
        "Amoxicillin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [50, 50],
                "high": [80, 90],
                "max_day": 4000
            }
        ],
        "Amoxicillin-Clavulanate (Augmentin)": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [50, 50],
                "high": [80, 90],
                "max_day": 4000
            }
        ],
        "Cephalexin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [25, 50],
                "severe": [100, 150],
                "max_day": 6000
            }
        ],
        "Clarithromycin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [15, 15],
                "max_dose": 500,
                "max_day": 1000
            }
        ]
    },

    "Gastrointestinal": {
        "Ceftriaxone": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [50, 50],
                "max_dose": 2000,
                "max_day": 4000
            }
        ],
        "Metronidazole": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [20, 50],
                "max_day": 2250
            },
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [22.5, 40],
                "max_day": 4000
            }
        ],
        "Gentamicin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [5, 7.5]
            }
        ]
    },

    "Genitourinary": {
        "Gentamicin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [5, 7.5]
            }
        ],
        "Ceftriaxone": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [50, 75],
                "max_dose": 2000,
                "max_day": 4000
            }
        ]
    },

    "Respiratory": {
        "Oseltamivir": [
            {
                "route": "PO",
                "unit": "mg",
                "notes": (
                    "Respiratory/influenza use. PMA >40 weeks: 3 mg/kg/DOSE Q12H. "
                    "If age >=1 year, per dose Q12H: <=15 kg: 30 mg; >15 to 23 kg: 45 mg; "
                    ">23 to 40 kg: 60 mg; >40 kg or adult: 75 mg. "
                    "Use particularly in high-risk, severe, complicated, or progressive influenza; "
                    "preferably within 48 hours of illness onset."
                )
            }
        ],

        "Amoxicillin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [80, 90],
                "max_day": 4000,
                "notes": (
                    "Community-acquired pneumonia, age 3 months to 5 years, non-toxic/mild-moderate; "
                    "if suspect S. pneumoniae. Guideline frequency: Q8-12H. "
                    "Also used in age >5 years if suspect S. pneumoniae or if not better after 48-72 hours "
                    "of prior macrolide therapy."
                )
            }
        ],

        "Clarithromycin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [15, 15],
                "max_dose": 500,
                "max_day": 1000,
                "notes": (
                    "CAP age 3 months to 5 years, non-toxic/mild-moderate, if suspect Mycoplasma or H. influenzae; "
                    "Q12H. Also first-line for CAP age >5 years, non-toxic/mild-moderate, if suspect Mycoplasma; Q12H."
                )
            },
            {
                "route": "PO",
                "unit": "mg",
                "usual": [15, 15],
                "max_dose": 500,
                "max_day": 1000,
                "notes": (
                    "Specific organism: Mycoplasma pneumoniae PCR positive or serology >=320. "
                    "Preferred regimen. Guideline frequency: Q12H. Typical duration 7-10 days."
                )
            }
        ],

        "Azithromycin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [10, 10],
                "notes": (
                    "CAP age 3 months to 5 years, non-toxic/mild-moderate, if suspect Mycoplasma or H. influenzae; "
                    "Q24H; typical duration 3 days. Also alternative for age >5 years non-toxic/mild-moderate "
                    "if suspect Mycoplasma."
                )
            },
            {
                "route": "PO",
                "unit": "mg",
                "usual": [10, 10],
                "notes": (
                    "Specific organism: Mycoplasma pneumoniae. Alternative to clarithromycin. "
                    "Guideline frequency: Q24H. Typical duration 3 days."
                )
            }
        ],

        "Cefuroxime": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [30, 30],
                "notes": (
                    "CAP age 3 months to 5 years, non-toxic/mild-moderate, if penicillin allergy suspected "
                    "but non-anaphylactic/non-severe and suspect S. pneumoniae; Q12H. "
                    "Also listed for age >5 years non-toxic/mild-moderate."
                )
            }
        ],

        "Ampicillin": [
            {
                "route": "IV",
                "unit": "mg",
                "usual": [200, 300],
                "notes": (
                    "CAP age >5 years, severe (non-HD/ICU) or cannot tolerate PO; use with PO clarithromycin. "
                    "Guideline frequency: Q6H. If complicated pneumonia, longer duration may be needed."
                )
            },
            {
                "route": "IV",
                "unit": "mg",
                "usual": [300, 300],
                "notes": (
                    "CAP age >5 years, severe (HD/ICU); use with IV erythromycin. "
                    "Guideline frequency: Q6H."
                )
            }
        ],

        "Ceftriaxone": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [100, 100],
                "max_dose": 2000,
                "max_day": 4000,
                "notes": (
                    "CAP age >5 years, severe (non-HD/ICU) or cannot tolerate PO; "
                    "use if not better after 48 hours of prior ampicillin therapy, or in selected alternative regimens. "
                    "Guideline frequency: Q12-24H."
                )
            },
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [100, 100],
                "max_dose": 2000,
                "max_day": 4000,
                "notes": (
                    "CAP age >5 years, severe (HD/ICU); use with IV erythromycin. "
                    "Guideline frequency: Q12-24H."
                )
            }
        ],

        "Erythromycin": [
            {
                "route": "IV",
                "unit": "mg",
                "usual": [50, 50],
                "notes": (
                    "CAP age >5 years, severe (HD/ICU); use with IV ampicillin or IV/IM ceftriaxone. "
                    "Guideline frequency: Q6H. Typical duration 14 days."
                )
            }
        ],

        "Levofloxacin": [
            {
                "route": "IV / PO",
                "unit": "mg",
                "notes": (
                    "Respiratory alternative regimen, ID-guided. "
                    "<5 years: 20 mg/kg/day Q12H; >=5 years: 10 mg/kg/day Q24H. "
                    "Listed for severe CAP and specific Mycoplasma pneumoniae."
                )
            }
        ],

        "Doxycycline": [
            {
                "route": "PO / IV",
                "unit": "mg",
                "usual": [4, 4],
                "notes": (
                    "Respiratory alternative in selected cases, including Mycoplasma pneumoniae; "
                    "guideline frequency: Q12H, noted if G6PD deficient in specific-organism row."
                )
            }
        ],

        "Clindamycin": [
            {
                "route": "IV / PO",
                "unit": "mg",
                "notes": (
                    "Add-on therapy in severe/complicated CAP if lung necrosis suspected "
                    "or documented risk of MRSA. Respiratory/ID discussion recommended."
                )
            }
        ]
},
    "Skin / Skeletal": {
        "Cefazolin": [
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [25, 50],
                "severe": [100, 150],
                "max_day": 12000
            }
        ],
        "Cloxacillin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [50, 100],
                "max_dose": 1000,
                "max_day": 6000
            },
            {
                "route": "IV / IM",
                "unit": "mg",
                "usual": [100, 100],
                "severe": [200, 300],
                "max_dose": 2000,
                "max_day": 12000
            }
        ],
        "Cephalexin": [
            {
                "route": "PO",
                "unit": "mg",
                "usual": [25, 50],
                "severe": [100, 150],
                "max_day": 6000
            }
        ]
    }
}