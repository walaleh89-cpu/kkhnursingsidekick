# gastro.py

gastro_data = {
    "Omeprazole": [
        {
            "route": "PO",
            "unit": "mg",
            "usual": [0.8, 0.8],
            "max_dose": 40,
            "notes": "Give 30 minutes before meals for best effect."
        },
        {
            "route": "IV / IM",
            "unit": "mg",
            "usual": [1, 1],
            "max_dose": 40
        }
    ],

    "Lansoprazole": [
        {
            "route": "PO",
            "unit": "mg",
            "age_group": ">=1 year old",
            "weight_range": "<=30kg",
            "usual": [15, 15],
            "frequency": "OM",
            "max_day": 30,
            "notes": "Take 30 minutes before meals for best effect."
        },
        {
            "route": "PO",
            "unit": "mg",
            "age_group": ">=1 year old",
            "weight_range": ">30kg",
            "usual": [30, 30],
            "frequency": "OM",
            "max_day": 60,
            "notes": "Take 30 minutes before meals for best effect."
        }
    ],

    "Antacid with Simethicone Tablet": [
        {
            "route": "PO",
            "unit": "tabs",
            "usual": [1, 2],
            "frequency": "TDS",
            "notes": "Separate from other medications by 2 hours."
        }
    ],

    "Simethicone Drops": [
        {
            "route": "PO",
            "unit": "mL",
            "age_group": "<2 years old",
            "usual": [0.2, 0.2],
            "frequency": "Q2-6H",
            "max_doses_day": 12
        },
        {
            "route": "PO",
            "unit": "mL",
            "age_group": "2-11 years old",
            "usual": [0.4, 0.4],
            "frequency": "Q2-6H",
            "max_doses_day": 12
        }
    ],

    "Domperidone": [
        {
            "route": "PO",
            "unit": "mg",
            "usual": [0.2, 0.4],
            "frequency": "Q8H",
            "max_dose": 10,
            "notes": "Contraindicated in patients with cardiac disease."
        },
        {
            "route": "Per Rectal",
            "unit": "mg",
            "usual": [0.75, 0.75],
            "frequency": "Q12H",
            "max_dose": 30,
            "notes": "Contraindicated in patients with cardiac disease."
        }
    ],

    "Eviline Forte Suspension": [
        {
            "route": "PO",
            "unit": "mL",
            "age_group": "2-5 years",
            "usual": [2.5, 2.5],
            "frequency": "Q8H",
            "notes": "Separate from other medications by 2 hours."
        },
        {
            "route": "PO",
            "unit": "mL",
            "age_group": "5-12 years",
            "usual": [2.5, 5],
            "frequency": "Q6-8H",
            "notes": "Separate from other medications by 2 hours."
        },
        {
            "route": "PO",
            "unit": "mL",
            "age_group": ">=12 years",
            "usual": [5, 10],
            "frequency": "Q6-8H",
            "max_day": 40,
            "notes": "Separate from other medications by 2 hours."
        }
    ]
}