# Reboot.dev Architecture

## Core loop

SCAN → UNDERSTAND → DIAGNOSE → PRIORITIZE → EXPLAIN → TAKE ACTION → RESCAN → PROGRESS

## Analysis pipeline

Repository → Ingestion → Classification → Static Analysis → Context → Diagnosis → Priority → Report → Mentor → Action → Patch → Verification → Rescan

## Design principles

1. Deterministic analysis comes before AI reasoning.
2. Important findings require evidence.
3. Severity and confidence are separate dimensions.
4. Missing evidence remains explicit.
5. No modification is applied without verification.
6. Rescan measures actual change after an action.
