import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)
from sklearn.model_selection import train_test_split

file_path = "/home/pedropaulo/Downloads/hmp2_metadata_2018-08-20.csv"


important_columns = [
    "Participant ID",
    "date_of_receipt",
    "hbi",
    "diagnosis",
    "consent_age",
    "sex",
    "fecalcal_ng_ml",
    "CRP (mg/L)",
]

df = pd.read_csv(file_path)
df = df[important_columns].copy()
only_hbi_df = df.dropna(subset=["hbi"])  # Filter out rows where 'hbi' is NaN
df_crohn = only_hbi_df[
    only_hbi_df["diagnosis"] == "CD"
].copy()  # Filter for Crohn's Disease (CD) only
df_crohn["date_of_receipt"] = pd.to_datetime(
    df_crohn["date_of_receipt"]
)  # Converts date_of_receipt to datetime format
avg_age = df_crohn["consent_age"].median()
df_crohn["consent_age"].fillna(
    avg_age, inplace=True
)  # Fill NaN values in 'consent_age' with the avg age
df_crohn_sorted = df_crohn.sort_values(
    by=["Participant ID", "date_of_receipt"]
)  # Sort by 'Participant ID' and 'date_of_receipt'
df_crohn_sorted["hbi_future"] = df_crohn_sorted.groupby("Participant ID")["hbi"].shift(
    -1
)  # Shift 'hbi' values to create 'hbi_future'
df_crohn_sorted["flare_future"] = (df_crohn_sorted["hbi_future"] >= 5).astype(
    int
)  # If 'hbi_future' >= 5, then flare is 1, else 0
df_final = df_crohn_sorted.dropna(
    subset=["hbi_future"]
)  # Drop rows where 'hbi_future' is NaN

df_premium_final = df_final.dropna(subset=["CRP (mg/L)"]) # Remove rows with NaN in 'CRP (mg/L)'


df_basic_final = df_final.drop(
    columns=["fecalcal_ng_ml", "CRP (mg/L)"]
)  # Drop 'fecalcal_ng_ml' and 'CRP (mg/L)' columns

features = ["hbi", "consent_age", "sex", "fecalcal_ng_ml", "CRP (mg/L)"]
X = df_premium_final[features]
X = pd.get_dummies(X, columns=["sex"], drop_first=True)
y = df_premium_final["flare_future"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42, stratify=y
)

modelo = RandomForestClassifier(
    n_estimators=300, random_state=42, class_weight="balanced"
)
modelo.fit(X_train, y_train)

print("Modelo treinado com sucesso!")

previsoes = modelo.predict(X_test)

acuracia = accuracy_score(y_test, previsoes)
print(f"\nGeneral Accuracy: {acuracia:.2f}")

#print("\nRelatório de Classificação:")
print(
    classification_report(y_test, previsoes, target_names=["Remission (0)", "Outbreak (1)"])
)

cm = confusion_matrix(y_test, previsoes)
print("\nConfusion Matrix:")
print(cm)
