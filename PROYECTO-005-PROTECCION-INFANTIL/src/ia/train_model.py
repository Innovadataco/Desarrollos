#!/usr/bin/env python3
"""
Entrena el modelo de triage de riesgo para reportes de protección infantil.
Genera dataset sintético, entrena pipeline TF-IDF + LogisticRegression/RandomForest,
y guarda artefactos en src/ia/models/risk-v1.0.0/.
"""

import json
import os
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
MODEL_DIR = ROOT / "models" / "risk-v1.0.0"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

random.seed(42)
np.random.seed(42)


TEMPLATES = {
    "contacto_inapropiado": [
        "Un desconocido contactó a mi hijo por {plataforma} diciendo que quería ser su amigo.",
        "Recibimos mensajes de un número desconocido haciendo preguntas personales a mi hija.",
        "Alguien se comunicó con mi hijo por {plataforma} de forma extraña y persistente.",
    ],
    "solicitud_material": [
        "Le pidieron fotos a mi hija de 12 años por {plataforma}, diciendo que era para un juego.",
        "Un contacto solicitó videos íntimos a cambio de dinero y regalos.",
        "Le dijeron a mi hijo que enviara fotos sin ropa para demostrar confianza.",
    ],
    "grooming": [
        "Este usuario se hace pasar por compañero de colegio para ganar confianza y luego pide fotos.",
        "Le dijo a mi hija 'no le cuentes a tus papás, es nuestro secreto'.",
        "Primero fue amable, luego empezó a decirle que sus padres no la entendían.",
    ],
    "cita_persona": [
        "Propuso encontrarse con mi hijo en un parque después de clases.",
        "Quedó en ver a mi hija en un centro comercial sin nuestro permiso.",
        "Insistió en reunirse a solas con mi hijo en su casa.",
    ],
    "extorsion": [
        "Amenazó con difundir fotos si no enviaba más contenido.",
        "Dijo que si no le enviaba dinero, publicaría conversaciones privadas.",
        "Obligó a mi hija a seguir enviando fotos con amenazas.",
    ],
    "desconocido": [
        "Hay un contacto que no reconozco pero no sé si es peligroso.",
        "Mi hijo recibió mensajes que no entiendo bien.",
        "Un número desconocido llamó varias veces pero no dijo nada.",
    ],
}

PLATAFORMAS = ["WhatsApp", "Instagram", "Discord", "TikTok", "Facebook"]


def generate_example(category: str, severity: float) -> dict:
    template = random.choice(TEMPLATES[category])
    plataforma = random.choice(PLATAFORMAS)
    description = template.format(plataforma=plataforma)
    if severity > 0.7 and category != "desconocido":
        description += " Fue muy insistente y usó frases de secreto y confianza."
    if severity < 0.3 and category != "desconocido":
        description += " Solo fue una vez y no volvió a escribir."
    return {
        "description": description,
        "category": category,
        "risk_score": severity,
    }


def build_dataset(n: int = 1800) -> pd.DataFrame:
    distribution = {
        "contacto_inapropiado": (0.30, 0.35, 0.65),
        "solicitud_material": (0.20, 0.70, 0.90),
        "grooming": (0.25, 0.75, 0.92),
        "cita_persona": (0.15, 0.80, 0.95),
        "extorsion": (0.10, 0.85, 0.93),
        "desconocido": (0.05, 0.10, 0.30),
    }
    rows = []
    for category, (weight, min_s, max_s) in distribution.items():
        count = int(n * weight)
        for _ in range(count):
            severity = random.uniform(min_s, max_s)
            rows.append(generate_example(category, severity))
    df = pd.DataFrame(rows)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df["is_high_risk"] = (df["risk_score"] >= 0.5).astype(int)
    return df


def _level_from_score(score: float) -> str:
    if score >= 0.85:
        return "severe"
    if score >= 0.7:
        return "critical"
    if score >= 0.5:
        return "high"
    if score >= 0.3:
        return "medium"
    return "low"


def main():
    df = build_dataset(1800)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_DIR / "synthetic_train_v1.csv", index=False)

    X = df["description"]
    y_score = df["risk_score"]
    y_binary = df["is_high_risk"]
    y_category = df["category"]

    (
        X_train,
        X_test,
        ys_train,
        ys_test,
        yb_train,
        yb_test,
        yc_train,
        yc_test,
    ) = train_test_split(
        X, y_score, y_binary, y_category, test_size=0.15, random_state=42
    )
    (
        X_train,
        X_val,
        ys_train,
        ys_val,
        yb_train,
        yb_val,
        yc_train,
        yc_val,
    ) = train_test_split(
        X_train, ys_train, yb_train, yc_train, test_size=0.15, random_state=42
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=5000,
        stop_words="english",
        lowercase=True,
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)
    X_test_vec = vectorizer.transform(X_test)

    lr = CalibratedClassifierCV(
        LogisticRegression(max_iter=1000, C=0.5, class_weight="balanced"),
        cv=5,
    )
    rf = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
    )
    rf_category = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=42,
    )

    lr.fit(X_train_vec, yb_train)
    rf.fit(X_train_vec, yb_train)
    rf_category.fit(X_train_vec, yc_train)

    # Score = probabilidad promedio del ensemble
    preds_lr = lr.predict_proba(X_test_vec)[:, 1]
    preds_rf = rf.predict_proba(X_test_vec)[:, 1]
    preds_ens = (preds_lr + preds_rf) / 2.0

    auc = roc_auc_score(yb_test, preds_ens)
    f1 = f1_score(yb_test, (preds_ens >= 0.5).astype(int))

    # Calibrate severe threshold using validation set
    X_val_vec = vectorizer.transform(X_val)
    val_lr = lr.predict_proba(X_val_vec)[:, 1]
    val_rf = rf.predict_proba(X_val_vec)[:, 1]
    val_ens = (val_lr + val_rf) / 2.0
    val_levels = [_level_from_score(s) for s in val_ens]
    severe_rate = sum(1 for l in val_levels if l == "severe") / len(val_levels)

    print(f"AUC-ROC: {auc:.4f}")
    print(f"F1: {f1:.4f}")
    print(f"Severe rate en validación: {severe_rate:.4f}")

    joblib.dump(lr, MODEL_DIR / "model_lr.joblib")
    joblib.dump(rf, MODEL_DIR / "model_rf.joblib")
    joblib.dump(rf_category, MODEL_DIR / "model_category.joblib")
    joblib.dump(vectorizer, MODEL_DIR / "vectorizer.joblib")

    metadata = {
        "version": "risk-v1.0.0",
        "model": "ensemble_lr_rf",
        "dataset": "synthetic_train_v1.csv",
        "n_examples": len(df),
        "auc_roc": float(auc),
        "f1": float(f1),
        "threshold_high": 0.5,
        "threshold_severe": 0.85,
        "categories": sorted(df["category"].unique().tolist()),
    }
    with open(MODEL_DIR / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"Modelo guardado en {MODEL_DIR}")


if __name__ == "__main__":
    main()
