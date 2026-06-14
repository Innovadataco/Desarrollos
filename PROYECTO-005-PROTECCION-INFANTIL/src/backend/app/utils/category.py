"""Mapeo entre códigos de categoría del SPEC-001 y slugs internos."""

CATEGORY_CODE_TO_SLUG = {
    "CAT-01": "contacto_inapropiado",
    "CAT-02": "solicitud_material",
    "CAT-03": "grooming",
    "CAT-04": "cita_persona",
    "CAT-05": "extorsion",
    "CAT-06": "desconocido",
}

CATEGORY_SLUG_TO_CODE = {v: k for k, v in CATEGORY_CODE_TO_SLUG.items()}


def category_code_to_slug(code: str) -> str:
    return CATEGORY_CODE_TO_SLUG.get(code, "desconocido")


def category_slug_to_code(slug: str) -> str:
    return CATEGORY_SLUG_TO_CODE.get(slug, "CAT-06")
