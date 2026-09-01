## 2026-09-01 - Fix Bootstrap 5 alert dismiss and ARIA label
**Learning:** Bootstrap 5 requires `data-bs-dismiss` instead of `data-bs-alert` (or the older `data-dismiss`) for closing alerts. Additionally, default ARIA labels like 'Close' provided by screen readers should be explicitly overridden in localized applications (e.g., to 'Fechar' in Portuguese) to ensure correct accessibility.
**Action:** Always verify Bootstrap 5 data attributes (`data-bs-*`) and explicitly provide localized ARIA labels for icon-only interactive elements like `.btn-close`.
