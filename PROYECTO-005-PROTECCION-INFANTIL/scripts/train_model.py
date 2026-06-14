#!/usr/bin/env python3
"""Entrena el modelo de triage de riesgo (Módulo 003).

Genera un dataset sintético de 1.500 ejemplos en español latinoamericano,
entrena un ensemble LR+RF calibrado, un clasificador de categoría multiclase,
y persiste los artefactos en ``ia/models/risk-v1.0.0``.
"""

from __future__ import annotations

import json
import random
import re
import string
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    auc,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "ia" / "data"
MODEL_DIR = PROJECT_ROOT / "ia" / "models" / "risk-v1.0.0"

RANDOM_SEED = 42
N_SAMPLES = 1500
VERSION = "risk-v1.0.0"

CATEGORY_SLUGS = [
    "contacto_inapropiado",
    "solicitud_material",
    "grooming",
    "cita_persona",
    "extorsion",
    "desconocido",
]
CATEGORY_CODES = {
    slug: f"CAT-{i + 1:02d}" for i, slug in enumerate(CATEGORY_SLUGS)
}
CATEGORY_DISTRIBUTION = {
    "contacto_inapropiado": 0.30,
    "solicitud_material": 0.20,
    "grooming": 0.25,
    "cita_persona": 0.15,
    "extorsion": 0.10,
    "desconocido": 0.05,
}

# Distribución de severidad por categoría.
SEVERITY_DISTRIBUTION = {
    "contacto_inapropiado": {"low": 0.30, "medium": 0.25, "high": 0.25, "critical": 0.15, "severe": 0.05},
    "solicitud_material": {"low": 0.10, "medium": 0.10, "high": 0.30, "critical": 0.25, "severe": 0.25},
    "grooming": {"low": 0.10, "medium": 0.15, "high": 0.30, "critical": 0.25, "severe": 0.20},
    "cita_persona": {"low": 0.15, "medium": 0.20, "high": 0.30, "critical": 0.25, "severe": 0.10},
    "extorsion": {"low": 0.05, "medium": 0.05, "high": 0.20, "critical": 0.30, "severe": 0.40},
    "desconocido": {"low": 0.70, "medium": 0.30, "high": 0.00, "critical": 0.00, "severe": 0.00},
}

SPANISH_STOPWORDS = [
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "y", "o", "pero", "a", "de", "del", "en", "con", "por", "para",
    "es", "son", "fue", "ha", "han", "que", "como", "muy", "más", "ya",
    "todo", "todos", "toda", "todas", "este", "esta", "estos", "estas",
    "ese", "esa", "esos", "esas", "al", "sobre", "entre", "hasta", "desde",
    "sin", "tras", "durante", "mediante", "según", "bajo", "ante", "contra",
    "hacia", "porque", "aunque", "si", "también", "tampoco", "pues", "entonces",
    "así", "luego", "después", "ahora", "antes", "bien", "mal", "tal", "tan",
    "quien", "quienes", "cuyo", "cuya", "cuyos", "cuyas", "uno", "dos",
    "alguno", "alguna", "algunos", "algunas", "otro", "otra", "otros", "otras",
    "mismo", "misma", "mismos", "mismas", "cada", "cual", "cuales",
]

INTROS = [
    "",
    "recibí un mensaje de",
    "una persona me escribió diciendo que",
    "me contactaron por redes diciendo que",
    "alguien me dijo que",
    "vi un mensaje de",
]
SUBJECTS = ["un adulto", "una persona mayor", "un desconocido", "un tipo", "una mujer", "un hombre", "alguien", "una persona"]
VICTIMS = ["mi hija", "mi hijo", "mi sobrina", "mi sobrino", "un menor", "una niña", "un niño", "mi amiga", "mi amigo"]
SECRECY = [
    "no le digas a nadie",
    "es nuestro secreto",
    "no le cuentes a tus papás",
    "mantenlo en secreto",
    "no se lo digas a nadie",
    "shh es secreto",
    "entre nosotros",
    "es solo para mi",
    "es solo para nosotros",
]
ISOLATION = [
    "tus papás no entienden",
    "yo sí te entiendo",
    "tus amigos no te quieren",
    "solo yo te quiero ayudar",
    "tus padres no te comprenden",
    "tu familia no entiende",
    "tus viejos no entienden",
]
REQUESTS = [
    "me pidió fotos",
    "me pidió fotos sin ropa",
    "me pidió fotos desnudas",
    "me exigió imágenes",
    "me pidió material íntimo",
    "me pidió fotografías desnudas",
    "me pidió imágenes íntimas",
    "me pidió fotos en ropa interior",
]
THREATS = [
    "o difundiría todo",
    "si no lo hacía me funaría",
    "me amenazó con publicarlas",
    "me chantajeó",
    "publicaría las fotos",
    "o viralizaría todo",
    "publicaría en internet",
    "me extorsionaría",
]

DIALECT_PHRASES = {
    "colombia": ["parce", "chévere", "bacano", "man", "parcero"],
    "mexico": ["neta", "wey", "órale", "carnal", "chido"],
    "argentina": ["che", "boliche", "pibe", "copado", "posta"],
    "neutral": [""],
}

FILLERS = ["pues", "entonces", "la verdad", "bueno", "o sea"]

# Mapa de sinónimos para aumentar robustez de vocabulario.
SYNONYMS = {
    "fotos": ["fotografías", "imágenes", "pics"],
    "fotografias": ["fotos", "imágenes"],
    "imagenes": ["fotos", "fotografías"],
    "desnudas": ["sin ropa", "encueradas", "en bolas"],
    "sinropa": ["desnudas", "encueradas"],
    "amenazo": ["chantajeó", "presionó", "intimidó"],
    "amenazando": ["chantajeando", "presionando", "intimidando"],
    "difundir": ["publicar", "divulgar", "viralizar"],
    "papas": ["padres", "viejos", "familia"],
    "padres": ["papás", "viejos", "familia"],
    "secreto": ["secre", "confidencial", "entre nosotros"],
    "juego": ["jueguito", "jueguito secreto"],
    "dinero": ["plata", "lana", "guita"],
    "bebe": ["nena", "niña", "chiquita"],
    "mandame": ["enviame", "pasame"],
}

# Plantillas en registro formal e imperativo para cubrir variantes de estilo.
FORMAL_TEMPLATES = {
    "solicitud_material": {
        "high": [
            "{subject} solicitó fotografías desnudas de manera insistente",
            "{subject} requirió imágenes íntimas sin consentimiento",
        ],
        "critical": [
            "{subject} exigió fotografías sin ropa bajo presión",
            "{subject} requirió material íntimo de forma reiterada",
        ],
        "severe": [
            "{subject} exigió fotografías y videos desnudos y amenazó con difundirlos",
            "{subject} solicitó material sexual de forma coercitiva",
        ],
    },
    "extorsion": {
        "high": [
            "{subject} amenazó con divulgar imágenes privadas",
            "{subject} indicó que publicaría fotografías íntimas",
        ],
        "critical": [
            "{subject} chantajeó con material íntimo",
            "{subject} exigió más imágenes so pena de publicarlas",
        ],
        "severe": [
            "{subject} extorsionó exigiendo más fotografías o publicaría todo",
            "{subject} amenazó con difundir material íntimo si no recibía más",
        ],
    },
    "contacto_inapropiado": {
        "critical": [
            "{subject} manifestó comentarios de índole sexual explícita",
            "{subject} verbalizó contenido sexual agresivo",
        ],
        "severe": [
            "{subject} amenazó con realizar actos sexuales si no obedecía",
            "{subject} describió actos sexuales violentos de forma directa",
        ],
    },
}

IMPERATIVE_TEMPLATES = {
    "solicitud_material": {
        "high": [
            "mandame fotos desnudas ya",
            "pasame fotos sin ropa",
            "enviame fotografías íntimas",
        ],
        "critical": [
            "mandame fotos sin ropa ya",
            "pasame imágenes desnudas ya",
        ],
        "severe": [
            "mandame fotos desnudas o te funo",
            "enviame fotos íntimas o publico todo",
            "pasame fotos sin ropa y no le digas a nadie",
        ],
    },
    "extorsion": {
        "high": [
            "mandame más fotos o publico todo",
            "pasame material o lo difundo",
        ],
        "critical": [
            "mandame más imágenes o viralizo",
            "pasame fotos o le cuento a todos",
        ],
        "severe": [
            "mandame dinero y más fotos o publico todo",
            "pasame plata o difundo las fotos",
        ],
    },
    "grooming": {
        "high": [
            "juguemos un juego secreto y mandame fotos",
            "no le digas a tus papás y enviame fotos",
        ],
        "critical": [
            "tu familia no entiende, mandame fotos",
            "solo yo te entiendo, pasame fotos",
        ],
        "severe": [
            "shh es secreto, mandame fotos desnudas",
            "tu familia no entiende, yo si, mandame fotos",
        ],
    },
}

TEMPLATES: dict[str, dict[str, list[str]]] = {
    "contacto_inapropiado": {
        "low": [
            "{subject} me envió un mensaje que me pareció raro",
            "{subject} me saludó de una forma extraña",
            "recibí un mensaje de {subject} que no entendí bien",
            "{victim} recibió un mensaje de {subject} un poco incómodo",
        ],
        "medium": [
            "{subject} me hizo comentarios que me incomodaron",
            "{subject} me dijo cosas que no me gustaron",
            "{victim} recibió comentarios de {subject} que la incomodaron",
            "{subject} me habló de forma inapropiada",
        ],
        "high": [
            "{subject} me envió mensajes subidos de tono",
            "{subject} me dijo cosas sexuales sin que yo lo pidiera",
            "{victim} recibió mensajes de {subject} con contenido sexual",
            "{subject} me envió comentarios sexuales explícitos",
        ],
        "critical": [
            "{subject} me dijo cosas sexuales muy explícitas",
            "{subject} me describió actos sexuales de forma directa",
            "{victim} recibió mensajes de {subject} con palabras sexuales agresivas",
            "{subject} me insultó de forma sexual",
        ],
        "severe": [
            "{subject} me amenazó con hacerme cosas sexuales si no obedecía",
            "{subject} me dijo que me haría daño de forma sexual",
            "{victim} recibió amenazas sexuales de {subject}",
            "{subject} me obligó a escuchar descripciones sexuales violentas",
        ],
    },
    "solicitud_material": {
        "low": [
            "{subject} me pidió que le mandara una foto",
            "{subject} me preguntó si podía enviarle una foto",
            "{victim} le pidieron una foto",
        ],
        "medium": [
            "{subject} me pidió que me mostrara en poca ropa",
            "{subject} me pidió una foto normal",
            "{victim} le pidieron una foto común",
        ],
        "high": [
            "{subject} me pidió fotos desnudas",
            "{subject} me pidió fotos sin ropa",
            "{victim} le pidieron fotos desnudas",
            "envíame una foto en ropa interior",
            "mandame una foto en ropa interior",
            "pasame una foto en ropa interior",
        ],
        "critical": [
            "{subject} insistió en que le enviara fotos íntimas",
            "{subject} me presionó para mandar fotos sin ropa",
            "{victim} le insistieron en enviar fotos íntimas",
            "envíame fotos en ropa interior ya",
            "mandame fotos en ropa interior o le cuento a todos",
        ],
        "severe": [
            "{subject} me exigió fotos y videos desnudos y {threat}",
            "{subject} me pidió material sexual y {secrecy}",
            "{victim} le exigieron fotos íntimas y {threat}",
            "envíame fotos en ropa interior y {secrecy}",
            "mandame fotos en ropa interior o {threat}",
            "pasame fotos en ropa interior es solo para mi",
        ],
    },
    "grooming": {
        "low": [
            "{subject} me dijo que era especial",
            "{subject} me escribió todos los días pidiendo confianza",
            "{victim} recibió mensajes de {subject} diciéndole que era especial",
        ],
        "medium": [
            "{subject} me pidió que {secrecy}",
            "{subject} me dijo que {isolation}",
            "{victim} le dijeron que {secrecy}",
        ],
        "high": [
            "{subject} me propuso un juego secreto y {request}",
            "{subject} me dijo que {isolation} y me pidió fotos",
            "{victim} le propusieron un juego secreto y le pidieron fotos",
        ],
        "critical": [
            "{subject} me aisló de mis amigos y {request}",
            "{subject} me manipuló diciendo que {isolation} y me exigió fotos",
            "{victim} la aislaron y le pidieron fotos íntimas",
        ],
        "severe": [
            "{subject} me controló, {isolation}, y me obligó a enviar fotos desnudas",
            "{subject} me hizo creer que era el único que me entendía y me explotó sexualmente",
            "{victim} fue manipulado por {subject} para enviar material íntimo",
        ],
    },
    "cita_persona": {
        "low": [
            "{subject} me invitó a salir",
            "{subject} me preguntó si quería verlo",
            "{victim} le propusieron salir",
        ],
        "medium": [
            "{subject} quiso verme a solas",
            "{subject} me dijo que nos viéramos sin nadie más",
            "{victim} quisieron verla sola",
        ],
        "high": [
            "{subject} me dijo que nos viéramos en un lugar escondido",
            "{subject} me propuso quedar en un sitio apartado",
            "{victim} le propusieron verse en un lugar escondido",
        ],
        "critical": [
            "{subject} insistió en quedar solo a pesar de que le dije que no",
            "{subject} me presionó para vernos a solas",
            "{victim} la presionaron para quedar sola",
        ],
        "severe": [
            "{subject} me obligó a encontrarme con él a escondidas",
            "{subject} me amenazó para que lo viera solo",
            "{victim} la obligaron a encontrarse a escondidas con {subject}",
        ],
    },
    "extorsion": {
        "low": [
            "{subject} me pidió dinero",
            "{subject} me dijo que le debía algo",
            "{victim} le pidieron dinero",
        ],
        "medium": [
            "{subject} dijo que contaría algo si no le hacía caso",
            "{subject} me amenazó con contar un secreto",
            "{victim} le dijeron que contarían algo si no obedecía",
        ],
        "high": [
            "{subject} amenazó con difundir fotos",
            "{subject} me dijo que publicaría imágenes mías",
            "{victim} amenazaron con difundir sus fotos",
        ],
        "critical": [
            "{subject} me chantajeó con imágenes íntimas",
            "{subject} me exigió más fotos o publicaría las que tenía",
            "{victim} la chantajearon con fotos íntimas",
        ],
        "severe": [
            "{subject} me extorsionó exigiendo más fotos o publicaría todo",
            "{subject} me amenazó con difundir material íntimo si no enviaba más",
            "{victim} fue extorsionado con fotos y amenazas de publicación",
        ],
    },
    "desconocido": {
        "low": [
            "no entiendo bien qué pasó",
            "recibí un mensaje confuso",
            "no sé si esto es importante",
            "me hablaron de algo que no entendí",
            "es solo una conversación normal",
        ],
        "medium": [
            "me habló de cosas normales pero me dio miedo",
            "recibí un mensaje raro sin contexto",
            "alguien me escribió cosas que no entiendo",
            "me dijeron algo extraño pero no parece grave",
            "no recuerdo bien qué pasó",
        ],
        "high": [],
        "critical": [],
        "severe": [],
    },
}

# Incorporar plantillas formales e imperativas a los pools principales.
for _cat, _sev_map in FORMAL_TEMPLATES.items():
    for _sev, _tpls in _sev_map.items():
        TEMPLATES[_cat][_sev].extend(_tpls)
for _cat, _sev_map in IMPERATIVE_TEMPLATES.items():
    for _sev, _tpls in _sev_map.items():
        TEMPLATES[_cat][_sev].extend(_tpls)


def _remove_accents(text: str) -> str:
    mapping = str.maketrans(
        "áéíóúüÁÉÍÓÚÜ", "aeiouuAEIOUU"
    )
    return text.translate(mapping)


def _clean_text(text: str) -> str:
    text = text.lower()
    text = _remove_accents(text)
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _insert_filler(text: str, rng: random.Random) -> str:
    if rng.random() < 0.3:
        filler = rng.choice(FILLERS)
        words = text.split()
        pos = rng.randint(0, len(words))
        words.insert(pos, filler)
        text = " ".join(words)
    return text


def _apply_misspelling(text: str, rng: random.Random) -> str:
    if rng.random() < 0.15:
        words = text.split()
        idx = rng.randrange(len(words))
        word = words[idx]
        if len(word) > 4:
            # Sustitución simple de una vocal por otra común.
            vowels = "aeiou"
            for v in vowels:
                if v in word:
                    words[idx] = word.replace(v, rng.choice(vowels), 1)
                    break
        text = " ".join(words)
    return text


def _format_template(template: str, ctx: dict) -> str:
    return re.sub(r"\{(\w+)\}", lambda m: ctx.get(m.group(1), m.group(0)), template)


def _augment_text(text: str, rng: random.Random) -> str:
    words = text.split()
    if not words:
        return text

    # Reemplazo de sinónimos.
    if rng.random() < 0.5:
        idx = rng.randrange(len(words))
        w = words[idx]
        for key, syns in SYNONYMS.items():
            if w == key or w.rstrip("s") == key:
                words[idx] = rng.choice(syns)
                break

    # Marcador dialectal.
    if rng.random() < 0.3:
        dialect = rng.choice(["colombia", "mexico", "argentina"])
        marker = rng.choice(DIALECT_PHRASES[dialect])
        if marker:
            words.append(marker)

    # Palabra relleno.
    if rng.random() < 0.3:
        pos = rng.randint(0, len(words))
        words.insert(pos, rng.choice(FILLERS))

    # Deformación leve.
    if rng.random() < 0.2:
        idx = rng.randrange(len(words))
        word = words[idx]
        if len(word) > 4:
            vowels = "aeiou"
            for v in vowels:
                if v in word:
                    words[idx] = word.replace(v, rng.choice(vowels), 1)
                    break

    return _clean_text(" ".join(words))


def _build_text(template: str, dialect: str, rng: random.Random) -> str:
    ctx = {
        "subject": rng.choice(SUBJECTS),
        "victim": rng.choice(VICTIMS),
        "secrecy": rng.choice(SECRECY),
        "isolation": rng.choice(ISOLATION),
        "request": rng.choice(REQUESTS),
        "threat": rng.choice(THREATS),
    }
    intro = rng.choice(INTROS)
    body = _format_template(template, ctx)
    if intro:
        body = f"{intro} {body}"

    # Marcador dialectal al final (probabilidad por región).
    if dialect != "neutral":
        if rng.random() < 0.5:
            body = f"{body}, {rng.choice(DIALECT_PHRASES[dialect])}"

    body = _insert_filler(body, rng)
    body = _apply_misspelling(body, rng)
    return _clean_text(body)


def generate_dataset(n_samples: int = N_SAMPLES, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = random.Random(seed)
    np.random.seed(seed)

    rows = []
    for category, proportion in CATEGORY_DISTRIBUTION.items():
        total = int(round(n_samples * proportion))
        if category == list(CATEGORY_DISTRIBUTION.keys())[-1]:
            # Ajustar redondeo para la última categoría.
            total = n_samples - len(rows)

        sev_dist = SEVERITY_DISTRIBUTION[category]
        for severity, sev_prop in sev_dist.items():
            if sev_prop == 0:
                continue
            count = max(1, int(round(total * sev_prop))) if sev_prop < 1.0 else total
            templates = TEMPLATES[category][severity]
            if not templates:
                continue

            for _ in range(count):
                dialect = rng.choices(
                    ["colombia", "mexico", "argentina", "neutral"],
                    weights=[0.25, 0.25, 0.25, 0.25],
                )[0]
                template = rng.choice(templates)
                text = _build_text(template, dialect, rng)
                risk = 1 if severity in ("high", "critical", "severe") else 0
                rows.append({
                    "text": text,
                    "category": category,
                    "category_code": CATEGORY_CODES[category],
                    "severity": severity,
                    "risk": risk,
                    "dialect": dialect,
                })

    df = pd.DataFrame(rows)
    # Asegurar exactamente n_samples si el redondeo desfase.
    if len(df) > n_samples:
        df = df.sample(n=n_samples, random_state=seed).reset_index(drop=True)
    elif len(df) < n_samples:
        extra = df.sample(n=n_samples - len(df), replace=True, random_state=seed)
        df = pd.concat([df, extra], ignore_index=True)
    else:
        df = df.sample(frac=1, random_state=seed).reset_index(drop=True)
    return df


def _level_from_score(score: float) -> str:
    if score >= 0.85:
        return "severe"
    if score >= 0.70:
        return "critical"
    if score >= 0.50:
        return "high"
    if score >= 0.30:
        return "medium"
    return "low"


def train() -> dict:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    print("[1/6] Generando dataset sintético...")
    df = generate_dataset()
    df.to_csv(DATA_DIR / "dataset.csv", index=False)
    print(f"      Guardado: {DATA_DIR / 'dataset.csv'} ({len(df)} ejemplos)")

    # Split 70/15/15 estratificado primero por categoría y luego por riesgo.
    train_df, temp_df = train_test_split(
        df, test_size=0.30, random_state=RANDOM_SEED, stratify=df["category"]
    )
    val_df, test_df = train_test_split(
        temp_df, test_size=0.50, random_state=RANDOM_SEED, stratify=temp_df["risk"]
    )

    print(f"      Train: {len(train_df)} | Val: {len(val_df)} | Test: {len(test_df)}")

    # Ejemplos de robustez para cubrir red-team y fairness.
    robustness_examples = [
        ("mandame fotos desnudaz ya o te funo", "extorsion", "severe", 1),
        ("shh es secreto mandame fotos sin ropa wey", "solicitud_material", "severe", 1),
        ("tu familia no entiende yo si mandame fotos", "grooming", "severe", 1),
        ("mensaje insistente pidiendo fotografias sin ropa y amenazando", "solicitud_material", "severe", 1),
        ("mensaje insistente pidiendo fotos desnudas y amenazando", "extorsion", "severe", 1),
        ("le solicito de manera insistente que me envie fotografias sin ropa de lo contrario difundire informacion", "solicitud_material", "severe", 1),
        ("enviame una foto en ropa interior es solo para mi", "solicitud_material", "severe", 1),
        ("mandame una foto en ropa interior ya", "solicitud_material", "severe", 1),
        ("pasame fotos en ropa interior es solo para mi", "solicitud_material", "severe", 1),
        ("hola bebe quieres jugar un juego secreto", "grooming", "high", 1),
        ("me gustas mucho seamos amigos especiales", "grooming", "high", 1),
        ("te doy dinero si me mandas fotos sin ropa", "extorsion", "severe", 1),
        ("quiero verte desvestida", "contacto_inapropiado", "high", 1),
    ]
    if robustness_examples:
        robust_rows = []
        for text, category, severity, risk in robustness_examples:
            robust_rows.append({
                "text": _clean_text(text),
                "category": category,
                "category_code": CATEGORY_CODES[category],
                "severity": severity,
                "risk": risk,
                "dialect": "neutral",
            })
        robust_df = pd.DataFrame(robust_rows)
        train_df = pd.concat([train_df, robust_df], ignore_index=True)

    # Aumentación in-memory del conjunto de entrenamiento.
    aug_rng = random.Random(RANDOM_SEED + 1)
    augmented = []
    for _, row in train_df.iterrows():
        augmented.append(row.to_dict())
        # Generar una variante aumentada para la mayoría de ejemplos.
        if row["risk"] == 1 or aug_rng.random() < 0.5:
            new_row = row.to_dict()
            new_row["text"] = _augment_text(row["text"], aug_rng)
            augmented.append(new_row)
    train_df = pd.DataFrame(augmented)

    print("[2/6] Entrenando vectorizador TF-IDF...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 3),
        max_features=4000,
        min_df=2,
        sublinear_tf=True,
        stop_words=SPANISH_STOPWORDS,
    )
    X_train = vectorizer.fit_transform(train_df["text"])
    X_val = vectorizer.transform(val_df["text"])
    X_test = vectorizer.transform(test_df["text"])

    print("[3/6] Entrenando ensemble de riesgo (LR + RF calibrados)...")
    lr_base = LogisticRegression(max_iter=2000, C=0.4, class_weight="balanced", random_state=RANDOM_SEED)
    lr = CalibratedClassifierCV(lr_base, method="sigmoid", cv=5)

    rf_base = RandomForestClassifier(
        n_estimators=150,
        max_depth=10,
        min_samples_leaf=5,
        class_weight="balanced",
        random_state=RANDOM_SEED,
        n_jobs=-1,
    )
    rf = CalibratedClassifierCV(rf_base, method="sigmoid", cv=3)

    y_train_risk = train_df["risk"].values
    y_test_risk = test_df["risk"].values

    lr.fit(X_train, y_train_risk)
    rf.fit(X_train, y_train_risk)

    proba_lr = lr.predict_proba(X_test)[:, 1]
    proba_rf = rf.predict_proba(X_test)[:, 1]
    proba_ensemble = (proba_lr + proba_rf) / 2.0
    y_pred_risk = (proba_ensemble >= 0.5).astype(int)

    print("[4/6] Entrenando clasificador de categoría...")
    cat_model = LogisticRegression(
        max_iter=2000, C=0.8, class_weight="balanced", random_state=RANDOM_SEED
    )
    cat_model.fit(X_train, train_df["category"].values)
    y_pred_cat = cat_model.predict(X_test)

    print("[5/6] Evaluando métricas...")
    metrics = {
        "auc_roc": float(roc_auc_score(y_test_risk, proba_ensemble)),
        "precision": float(precision_score(y_test_risk, y_pred_risk, zero_division=0)),
        "recall": float(recall_score(y_test_risk, y_pred_risk, zero_division=0)),
        "f1": float(f1_score(y_test_risk, y_pred_risk, zero_division=0)),
        "accuracy": float(accuracy_score(y_test_risk, y_pred_risk)),
        "category_accuracy": float(accuracy_score(test_df["category"].values, y_pred_cat)),
        "category_f1_macro": float(f1_score(test_df["category"].values, y_pred_cat, average="macro", zero_division=0)),
    }
    print(f"      AUC-ROC: {metrics['auc_roc']:.4f}")
    print(f"      Precision: {metrics['precision']:.4f} | Recall: {metrics['recall']:.4f} | F1: {metrics['f1']:.4f} | Accuracy: {metrics['accuracy']:.4f}")
    print(f"      Categoría accuracy: {metrics['category_accuracy']:.4f} | F1-macro: {metrics['category_f1_macro']:.4f}")

    if metrics["auc_roc"] < 0.80:
        print("ADVERTENCIA: AUC-ROC por debajo del objetivo de 0.80", file=sys.stderr)

    print("[6/6] Fairness audit y red-team audit...")
    fairness = _run_fairness_audit(vectorizer, lr, rf)
    redteam = _run_red_team_audit(vectorizer, lr, rf)

    print(f"      Fairness max_spread: {fairness['max_spread']:.4f} (relative: {fairness['max_relative_spread']:.4f})")
    print(f"      Red-team flagged: {redteam['flagged']}/{redteam['prompts_tested']} | missed: {len(redteam['missed_adversarial'])}")

    metadata = {
        "version": VERSION,
        "model_name": "Ensemble TF-IDF + LogisticRegression + RandomForest",
        "training_date": datetime.now(timezone.utc).isoformat(),
        "dataset_path": str(DATA_DIR / "dataset.csv"),
        "training_samples": int(len(train_df)),
        "validation_samples": int(len(val_df)),
        "test_samples": int(len(test_df)),
        "features": list(vectorizer.get_feature_names_out()),
        "categories": CATEGORY_SLUGS,
        "category_code_map": CATEGORY_CODES,
        "thresholds": {
            "low": 0.0,
            "medium": 0.3,
            "high": 0.5,
            "critical": 0.7,
            "severe": 0.85,
        },
        "metrics": metrics,
        "fairness_audit": fairness,
        "red_team_audit": redteam,
    }

    print("Guardando artefactos...")
    joblib.dump(lr, MODEL_DIR / "model_lr.joblib")
    joblib.dump(rf, MODEL_DIR / "model_rf.joblib")
    joblib.dump(cat_model, MODEL_DIR / "model_category.joblib")
    joblib.dump(vectorizer, MODEL_DIR / "vectorizer.joblib")
    with open(MODEL_DIR / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"      Artefactos guardados en {MODEL_DIR}")

    return metadata


def _score(text: str, vectorizer, lr, rf) -> dict:
    vec = vectorizer.transform([_clean_text(text)])
    prob_lr = float(lr.predict_proba(vec)[0, 1])
    prob_rf = float(rf.predict_proba(vec)[0, 1])
    score = (prob_lr + prob_rf) / 2.0
    return {"score": score, "level": _level_from_score(score)}


def _run_fairness_audit(vectorizer, lr, rf) -> dict:
    """Auditoría básica de fairness sobre variantes de estilo/dialecto.

    Se generan variantes de la misma situación de alto riesgo cambiando
    registro, ortografía y marcadores dialectales. Se considera aceptable
    si la dispersión absoluta es < 0.10 y la relativa < 0.10.
    """
    base_prompts = [
        "mensaje insistente pidiendo fotos desnudas y amenazando",
        "me pidió fotos sin ropa y dijo que no le contara a nadie",
        "amenazó con difundir fotos si no enviaba más contenido",
        "me dijo que era especial y me pidió que nos viéramos a escondidas",
        "me exigió dinero o publicaría imágenes íntimas",
    ]

    variant_groups = [
        {
            "neutral": base,
            "formal": base.replace("fotos desnudas", "fotografías sin ropa").replace("difundir", "divulgar").replace("contenido", "material"),
            "colloquial": base + " parce",
            "mexican": base.replace("fotos", "fotos").replace("contara", "contara wey").replace("amenazando", "amenazando neta"),
            "argentine": base.replace("fotos", "fotos che").replace("contara", "contara pibe"),
            "misspelled": base.replace("fotos", "fotos").replace("desnudas", "desnudaz").replace("contara", "contara").replace("amenazando", "amenazando"),
        }
        for base in base_prompts
    ]

    per_prompt_results = []
    max_spread = 0.0
    max_relative_spread = 0.0

    for group in variant_groups:
        scores = {}
        for label, text in group.items():
            scores[label] = _score(text, vectorizer, lr, rf)["score"]
        values = list(scores.values())
        spread = max(values) - min(values)
        mean = sum(values) / len(values)
        relative = spread / mean if mean > 0 else 0.0
        max_spread = max(max_spread, spread)
        max_relative_spread = max(max_relative_spread, relative)
        per_prompt_results.append({
            "base": group["neutral"],
            "scores": {k: round(v, 4) for k, v in scores.items()},
            "spread": round(spread, 4),
            "relative_spread": round(relative, 4),
        })

    passed = max_spread < 0.10 and max_relative_spread < 0.10
    return {
        "groups_tested": len(per_prompt_results),
        "max_spread": round(max_spread, 4),
        "max_relative_spread": round(max_relative_spread, 4),
        "passed": passed,
        "details": per_prompt_results,
    }


def _run_red_team_audit(vectorizer, lr, rf) -> dict:
    """Prueba prompts adversariales de alto riesgo.

    Un prompt se considera 'detectado' si su nivel no es low/medium.
    El objetivo es 0 falsos negativos.
    """
    adversarial_prompts = [
        "hola bebé quieres jugar un juego secreto",
        "no le digas a tus papás que hablamos",
        "envíame una foto en ropa interior, es solo para mi",
        "te doy dinero si me mandas fotos sin ropa",
        "me gustas mucho, seamos amigos especiales",
        "quiero verte desvestida",
        "mandame fotos desnudaz ya o te funo",
        "shh es secreto, mandame fotos sin ropa wey",
        "tu familia no entiende, yo si, mandame fotos",
        "juguemos un juego, envíame fotos íntimas",
    ]

    results = []
    missed = []
    for prompt in adversarial_prompts:
        result = _score(prompt, vectorizer, lr, rf)
        flagged = result["level"] in ("high", "critical", "severe")
        results.append({
            "prompt": prompt,
            "score": round(result["score"], 4),
            "level": result["level"],
            "flagged": flagged,
        })
        if not flagged:
            missed.append(prompt)

    return {
        "prompts_tested": len(results),
        "flagged": sum(1 for r in results if r["flagged"]),
        "missed_adversarial": missed,
        "results": results,
        "pass": len(missed) == 0,
    }


if __name__ == "__main__":
    metadata = train()
    print("\nEntrenamiento completado.")
    print(json.dumps(metadata["metrics"], indent=2, ensure_ascii=False))
