
## 2023-10-25 - Translating Bootstrap ARIA labels in localized apps
**Learning:** Bootstrap's default interactive components often rely on implicit or English ARIA labels. In non-English (e.g. Portuguese) applications, these need explicit override to maintain accessibility. Also, copying Bootstrap 4 attributes like `data-dismiss` to Bootstrap 5's `data-bs-dismiss` can be prone to errors like `data-bs-alert`.
**Action:** Always check default Bootstrap interactive elements (like `.btn-close`) in localized projects for explicit, correctly translated `aria-label` attributes and proper BS5 `data-bs-*` attributes.
