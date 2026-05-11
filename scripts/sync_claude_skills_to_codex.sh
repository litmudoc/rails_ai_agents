#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

SOURCE_DIR="${1:-${REPO_ROOT}/.claude/skills}"
TARGET_DIR="${2:-${REPO_ROOT}/.agents/skills}"
MANIFEST_PATH="${TARGET_DIR}/.claude-sync-manifest"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Source directory does not exist: ${SOURCE_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"

tmp_manifest="$(mktemp)"
trap 'rm -f "${tmp_manifest}"' EXIT

copied_count=0

while IFS= read -r -d '' skill_dir; do
  skill_name="$(basename "${skill_dir}")"

  # Ignore hidden entries like .DS_Store and only sync valid skill folders.
  if [[ "${skill_name}" == .* ]] || [[ ! -f "${skill_dir}/SKILL.md" ]]; then
    continue
  fi

  printf '%s\n' "${skill_name}" >> "${tmp_manifest}"
  rm -rf "${TARGET_DIR:?}/${skill_name}"
  mkdir -p "${TARGET_DIR}/${skill_name}"
  cp -R "${skill_dir}/." "${TARGET_DIR}/${skill_name}/"
  copied_count=$((copied_count + 1))
done < <(find "${SOURCE_DIR}" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)

if [[ -f "${MANIFEST_PATH}" ]]; then
  while IFS= read -r previous_skill; do
    [[ -n "${previous_skill}" ]] || continue
    if ! grep -Fqx "${previous_skill}" "${tmp_manifest}"; then
      rm -rf "${TARGET_DIR:?}/${previous_skill}"
    fi
  done < "${MANIFEST_PATH}"
fi

mv "${tmp_manifest}" "${MANIFEST_PATH}"
trap - EXIT

echo "Synced ${copied_count} Claude skill(s) from ${SOURCE_DIR} to ${TARGET_DIR}"
