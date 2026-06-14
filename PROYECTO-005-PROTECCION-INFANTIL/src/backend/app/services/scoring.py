import json
import re
from pathlib import Path

import joblib
import numpy as np

# scoring.py está en src/backend/app/services/, por tanto el proyecto raíz es parents[4].
_ROOT = Path(__file__).resolve().parents[4]
_MODEL_DIR = _ROOT / "ia" / "models" / "risk-v1.0.0"

_GROOMING_KEYWORDS = [
    "secreto",
    "no le cuentes",
    "no le digas",
    "tus papás",
    "tus padres",
    "no entienden",
    "yo sí te entiendo",
    "confianza",
    "amigo especial",
    "juego",
    "foto",
    "desnudo",
    "sin ropa",
    "insistente",
    "quedar",
    "encontrarnos",
    "reunirnos",
    "dinero",
    "amenaz",
    "difundir",
    "ropa interior",
    "chantaje",
    "extorsion",
]

_models = {}


def _remove_accents(text: str) -> str:
    mapping = str.maketrans("áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU")
    return text.translate(mapping)


def _preprocess(text: str) -> str:
    """Limpieza ligera compatible con el vectorizador entrenado."""
    text = text.lower()
    text = _remove_accents(text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _load_models():
    if _models:
        return _models
    try:
        _models["lr"] = joblib.load(_MODEL_DIR / "model_lr.joblib")
        _models["rf"] = joblib.load(_MODEL_DIR / "model_rf.joblib")
        _models["category"] = joblib.load(_MODEL_DIR / "model_category.joblib")
        _models["vectorizer"] = joblib.load(_MODEL_DIR / "vectorizer.joblib")
        with open(_MODEL_DIR / "metadata.json", encoding="utf-8") as f:
            _models["metadata"] = json.load(f)
    except Exception as exc:
        raise RuntimeError(f"No se pudieron cargar los modelos de IA: {exc}")
    return _models


def _detect_grooming_indicators(text: str) -> list[str]:
    lowered = text.lower()
    found = []
    for keyword in _GROOMING_KEYWORDS:
        if keyword in lowered and keyword not in found:
            found.append(keyword)
    return found[:5]


def _extract_lr_estimator(lr):
    """Obtiene el estimador base de LR, ya sea calibrado o no."""
    if hasattr(lr, "calibrated_classifiers_") and lr.calibrated_classifiers_:
        return lr.calibrated_classifiers_[0].estimator
    if hasattr(lr, "coef_"):
        return lr
    return None


def _top_tokens(text: str, lr, vectorizer, top_n: int = 5) -> list[dict]:
    processed = _preprocess(text)
    vec = vectorizer.transform([processed])
    feature_names = np.array(vectorizer.get_feature_names_out())

    estimator = _extract_lr_estimator(lr)
    if estimator is None:
        return []

    try:
        weights = estimator.coef_[0]
    except Exception:
        return []

    scores = np.asarray(vec.toarray()[0]) * weights
    top_idx = np.argsort(scores)[-top_n:][::-1]
    return [
        {"token": feature_names[i], "weight": round(float(scores[i]), 4)}
        for i in top_idx
        if scores[i] > 0
    ]


def score_text(text: str, explain: bool = True) -> dict:
    models = _load_models()
    processed = _preprocess(text)
    vec = models["vectorizer"].transform([processed])

    # Texto sin tokens reconocidos: no se puede inferir riesgo, se asigna nivel bajo.
    if vec.nnz == 0:
        return {
            "score": 0.0,
            "level": "low",
            "category": "desconocido",
            "category_confidence": 1.0,
            "model_version": models["metadata"].get("version", "risk-v1.0.0"),
            "grooming_indicators": [],
            "explanation": [],
        }

    prob_lr = models["lr"].predict_proba(vec)[0, 1]
    prob_rf = models["rf"].predict_proba(vec)[0, 1]
    score = float((prob_lr + prob_rf) / 2.0)

    category = str(models["category"].predict(vec)[0])
    category_confidence = float(np.max(models["category"].predict_proba(vec)))

    level = "low"
    if score >= 0.85:
        level = "severe"
    elif score >= 0.7:
        level = "critical"
    elif score >= 0.5:
        level = "high"
    elif score >= 0.3:
        level = "medium"

    grooming_indicators = _detect_grooming_indicators(text)
    explanation = (
        _top_tokens(text, models["lr"], models["vectorizer"])
        if explain and score > 0.7
        else []
    )

    return {
        "score": round(score, 4),
        "level": level,
        "category": category,
        "category_confidence": round(category_confidence, 4),
        "model_version": models["metadata"].get("version", "risk-v1.0.0"),
        "grooming_indicators": grooming_indicators,
        "explanation": explanation,
    }


def model_metadata() -> dict:
    models = _load_models()
    return models["metadata"]
