#!/usr/bin/env bash
# Genera certificados TLS autofirmados para entorno de staging local.
# NO usar en producción. En producción usar Let's Encrypt u otra CA válida.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CERTS_DIR="${SCRIPT_DIR}/../nginx/certs"

mkdir -p "${CERTS_DIR}"

if [ -f "${CERTS_DIR}/cert.pem" ] && [ -f "${CERTS_DIR}/key.pem" ]; then
  echo "Certificados ya existen en ${CERTS_DIR}. Usa --force para regenerarlos."
  exit 0
fi

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout "${CERTS_DIR}/key.pem" \
  -out "${CERTS_DIR}/cert.pem" \
  -subj "/C=CO/O=Innovadataco Staging/CN=localhost" \
  -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"

chmod 600 "${CERTS_DIR}/key.pem"
chmod 644 "${CERTS_DIR}/cert.pem"

echo "Certificados de staging generados en ${CERTS_DIR}:"
ls -l "${CERTS_DIR}"
