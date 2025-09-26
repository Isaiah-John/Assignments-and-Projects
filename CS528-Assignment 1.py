import pandas as pd
from collections import defaultdict
import copy


def heuristic_k_anonymize(df, qi_columns, hierarchies, k):
    
    def generalize_value(attr, value, level):
        if value in hierarchies[attr][f"level_{level}"]:
            return hierarchies[attr][f"level_{level}"][value]
        else:
            return "*"
    def group_by_QIs(df, record_levels):
        groups = defaultdict(list)
        for idx, row in df.iterrows():
            key = tuple(
                generalize_value(attr, row[attr], record_levels[idx][attr])
                for attr in qi_columns
            )
            groups[key].append(idx)
        return list(groups.values())
    
    def can_increase_level(attr, level):
        return f"level_{level+1}" in hierarchies[attr]
    
    def simulate_generalize(cls, attr, level):
        return [generalize_value(attr, df.loc[idx][attr], level) for idx in cls]
    
    def compute_utility_loss(cls, generalized_values):
        unique_vals = set(generalized_values)
        return len(unique_vals) 
    
    def apply_generalization(df, record_levels):
        df_copy = df.copy()
        for idx in df.index:
            for attr in qi_columns:
                level = record_levels[idx][attr]
                df_copy.at[idx, attr] = generalize_value(attr, df.at[idx, attr], level)
        return df_copy
    
    record_levels = {i: {qi: 0 for qi in qi_columns} for i in df.index}

    while True:
        eq_classes = group_by_QIs(df, record_levels)
        small_classes = [cls for cls in eq_classes if len(cls) < k]

        if not small_classes:
            break  # Done

        cls = min(small_classes, key=len)
        losses = {}
        for qi in qi_columns:
            current_level = record_levels[cls[0]][qi]
            if can_increase_level(qi, current_level):
                simulated = simulate_generalize(cls, qi, current_level + 1)
                losses[qi] = compute_utility_loss(cls, simulated)

        if not losses:
            break  # Cannot generalize further

        best_qi = min(losses, key=losses.get)

        for idx in df.index:
            record_levels[idx][best_qi] += 1

    return apply_generalization(df, record_levels)



def promblem3():
    


    age_hierarchy = {
    "level_0": {i: i for i in range(17, 91)},  # exact ages
    "level_1": {i: f"{10 * (i // 10)}-{10 * (i // 10) + 9}" for i in range(17, 91)},
    "level_2": {i: f"{20 * (i // 20)}-{20 * (i // 20) + 19}" for i in range(17, 91)},
    "level_3": {i: f"{40 * (i // 40)}-{40 * (i // 40) + 39}" for i in range(17, 91)},
    "level_4": {i: "0-49" if i < 50 else "50-99" for i in range(17, 91)},
    "level_5": {i: "<100" if i < 100 else ">100" for i in range(17, 91)},
    "level_6": {i: "*" for i in range(17, 91)},  # fully hidden
    }

    education_hierarchy = {
    "level_0": {
        "Bachelors": "Bachelors", "Some-college": "Some-college", "11th": "11th", "HS-grad": "HS-grad",
        "Prof-school": "Prof-school", "Assoc-acdm": "Assoc-acdm", "Assoc-voc": "Assoc-voc", "9th": "9th",
        "7th-8th": "7th-8th", "12th": "12th", "Masters": "Masters", "1st-4th": "1st-4th", "10th": "10th",
        "Doctorate": "Doctorate", "5th-6th": "5th-6th", "Preschool": "Preschool"
    },
    "level_1": {
        "Bachelors": "Undergrad", "Some-college": "Undergrad", "11th": "Highschool", "HS-grad": "Highschool",
        "Prof-school": "Grad", "Assoc-acdm": "Undergrad", "Assoc-voc": "Undergrad", "9th": "Middle School",
        "7th-8th": "Middle School", "12th": "Highschool", "Masters": "Grad", "1st-4th": "Elementary",
        "10th": "Middle School", "Doctorate": "Post Grad", "5th-6th": "Elementary", "Preschool": "Elementary"
    },
    "level_2": {
        "Bachelors": "College", "Some-college": "College", "11th": "K-12", "HS-grad": "K-12",
        "Prof-school": "College", "Assoc-acdm": "College", "Assoc-voc": "College", "9th": "K-12",
        "7th-8th": "K-12", "12th": "K-12", "Masters": "College", "1st-4th": "K-12", "10th": "K-12",
        "Doctorate": "Doctorate", "5th-6th": "K-12", "Preschool": "K-12"
    },
    "level_3": {
        "Bachelors": "Educated", "Some-college": "Educated", "11th": "Some Education", "HS-grad": "Educated",
        "Prof-school": "Educated", "Assoc-acdm": "Educated", "Assoc-voc": "Educated", "9th": "Some Education",
        "7th-8th": "Some Education", "12th": "Educated", "Masters": "Educated", "1st-4th": "Not Educated",
        "10th": "Some Education", "Doctorate": "Educated", "5th-6th": "Not Educated", "Preschool": "Not Educated"
    },
    "level_4": {edu: "*" for edu in [
        "Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th",
        "7th-8th", "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool"
    ]}
    }
    
    marital_status_hierarchy = {
    "level_0": {
        "Married-civ-spouse": "Married-civ-spouse", "Divorced": "Divorced", "Never-married": "Never-married",
        "Separated": "Separated", "Widowed": "Widowed", "Married-spouse-absent": "Married-spouse-absent",
        "Married-AF-spouse": "Married-AF-spouse"
    },
    "level_1": {
        "Married-civ-spouse": "Married", "Divorced": "Single", "Never-married": "Single",
        "Separated": "Complicated", "Widowed": "Single", "Married-spouse-absent": "Complicated",
        "Married-AF-spouse": "Married"
    },
    "level_2": {
        "Married-civ-spouse": "Married", "Divorced": "Not Married", "Never-married": "Not Married",
        "Separated": "Not Married", "Widowed": "Not Married", "Married-spouse-absent": "Married",
        "Married-AF-spouse": "Married"
    },
    "level_3": {status: "*" for status in [
        "Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed",
        "Married-spouse-absent", "Married-AF-spouse"
    ]}
    }
    
    race_hierarchy = {
    "level_0": {
        "White": "White", "Asian-Pac-Islander": "Asian-Pac-Islander", "Amer-Indian-Eskimo": "Amer-Indian-Eskimo",
        "Other": "Other", "Black": "Black"
    },
    "level_1": {
        "White": "White", "Asian-Pac-Islander": "Asian", "Amer-Indian-Eskimo": "Other",
        "Other": "Other", "Black": "Black"
    },
    "level_2": {
        "White": "White", "Asian-Pac-Islander": "Non-White", "Amer-Indian-Eskimo": "Non-White",
        "Other": "Non-White", "Black": "Non-White"
    },
    "level_3": {
        "White": "Person", "Asian-Pac-Islander": "Person", "Amer-Indian-Eskimo": "Person",
        "Other": "Person", "Black": "Person"
    },
    "level_4": {race: "*" for race in [
        "White", "Asian-Pac-Islander", "Amer-Indian-Eskimo", "Other", "Black"
    ]}
    }   

    hierarchies = {
    "age": age_hierarchy,
    "education": education_hierarchy,
    "marital_status": marital_status_hierarchy,
    "race": race_hierarchy
    }

    columns = [
    "age", "workclass", "fnlwgt", "education", "education_num",
    "marital_status", "occupation", "relationship", "race", "sex",
    "capital_gain", "capital_loss", "hours_per_week", "native_country", "income"
    ]
    df = pd.read_csv(
        r"C:\Users\isaia\Desktop\Class stuff\CS 528\adult3.0.csv",
        names=columns,
        na_values="?",
        skipinitialspace=True)
    
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    print(df.columns.tolist())  # Check columns
    
    qi_columns = ["age", "education", "marital_status", "race"]  # update as needed based on print output
    df = df.dropna(subset=["age", "education", "marital_status", "race"])

    anonymized_df = heuristic_k_anonymize(
        df,
        qi_columns=["age", "education", "marital_status", "race"],
        hierarchies=hierarchies,
        k=5
    )
    print(anonymized_df.head())
        
  
promblem3()


