## 2026-08-25 - Bootstrap 5 alert close buttons
**Learning:** Bootstrap 5 uses `data-bs-dismiss="alert"` for closing alerts, not `data-bs-alert="alert"`. Also, icon-only buttons need an `aria-label` for screen readers (e.g. `aria-label="Fechar"` for pt-BR localized apps).
**Action:** When adding or fixing Bootstrap 5 alert components, ensure the dismiss attribute is correct and the close button has an appropriate ARIA label translated to the application's locale.
