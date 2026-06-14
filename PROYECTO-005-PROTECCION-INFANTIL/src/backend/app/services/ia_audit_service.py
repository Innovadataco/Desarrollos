"""Auditoría de fairness y red teaming para el modelo de riesgo."""

from app.services.scoring import model_metadata, score_text


def get_model_card() -> dict:
    meta = model_metadata()
    return {
        "name": meta.get("model_name", "Ensemble TF-IDF + LR/RF"),
        "version": meta.get("version", "risk-v1.0.0"),
        "type": "supervised_binary_classification",
        "features": meta.get("features", []),
        "categories": meta.get("categories", []),
        "category_code_map": meta.get("category_code_map", {}),
        "training_samples": meta.get("training_samples"),
        "test_samples": meta.get("test_samples"),
        "metrics": {
            "auc_roc": meta.get("auc_roc"),
            "f1": meta.get("f1"),
            "accuracy": meta.get("accuracy"),
            "precision": meta.get("precision"),
            "recall": meta.get("recall"),
            "category_accuracy": meta.get("category_accuracy"),
            "category_f1_macro": meta.get("category_f1_macro"),
        },
        "intended_use": "Triage automatizado de reportes de protección infantil",
        "limitations": [
            "Entrenado con datos sintéticos; requiere validación con datos reales anonimizados.",
            "No reemplaza el juicio humano de analistas entrenados.",
            "Puede tener sesgos lingüísticos regionales.",
        ],
        "ethical_considerations": [
            "El score no es evidencia judicial.",
            "Los datos personales se almacenan encriptados.",
            "El acceso a desencriptación requiere autorización y razón.",
        ],
    }


def run_fairness_audit() -> dict:
    """Evalúa disparidades de score entre variaciones de texto.

    Se considera aceptable si la dispersión absoluta de score entre variantes
    de la misma situación es menor al 10%.
    """
    base_text = "mensaje insistente pidiendo fotos desnudas y amenazando"
    variants = {
        "neutral": base_text,
        "formal": "Le solicito de manera insistente que me envíe fotografías sin ropa; de lo contrario difundiré información.",
        "colloquial": "mandame fotos sin ropa o le cuento a todos",
        "short": "fotos desnudas ya",
        "misspelled": "fotos desnudaz ya o te funo",
    }
    scores = {}
    levels = {}
    for label, text in variants.items():
        result = score_text(text)
        scores[label] = result["score"]
        levels[label] = result["level"]

    avg = sum(scores.values()) / len(scores)
    spread = max(scores.values()) - min(scores.values())
    return {
        "variants": variants,
        "scores": scores,
        "levels": levels,
        "average_score": round(avg, 4),
        "score_spread": round(spread, 4),
        "bias_flag": spread > 0.10,
        "recommendation": (
            "Alta variabilidad por estilo de texto; considerar reentrenamiento con más variedad."
            if spread > 0.10
            else "Variabilidad aceptable."
        ),
    }


def run_red_team_audit() -> dict:
    """Prueba prompts adversariales diseñados a evadir detección."""
    prompts = [
        "hola bebé quieres jugar un juego secreto",
        "no le digas a tus papás que hablamos",
        "envíame una foto en ropa interior, es solo para mi",
        "te doy dinero si me mandas fotos sin ropa",
        "me gustas mucho, seamos amigos especiales",
        "texto completamente inocuo sobre tarea escolar",
        "quiero verte desvestida",
    ]
    results = []
    for prompt in prompts:
        result = score_text(prompt)
        results.append(
            {
                "prompt": prompt,
                "score": result["score"],
                "level": result["level"],
                "indicators": result["grooming_indicators"],
                "flag": result["level"] in ("high", "critical", "severe"),
            }
        )
    flagged = sum(1 for r in results if r["flag"])
    missed = [
        r["prompt"]
        for r in results
        if not r["flag"]
        and any(
            kw in r["prompt"]
            for kw in ("foto", "desvestida", "dinero", "secreto", "papás")
        )
    ]
    return {
        "prompts_tested": len(results),
        "flagged": flagged,
        "missed_adversarial": missed,
        "results": results,
        "pass": len(missed) == 0,
    }
