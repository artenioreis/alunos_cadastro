
## 2026-08-21 - Localizing default ARIA labels for Bootstrap elements
**Learning:** When using UI frameworks like Bootstrap in localized applications (e.g., pt-BR), it's crucial to explicitly override default ARIA labels (like the implicit "Close" for `.btn-close`) to match the application's locale. Otherwise, screen reader users will experience confusing, mixed-language navigation.
**Action:** Always inspect icon-only UI components from external libraries and explicitly set `aria-label`s matching the application's target language, even if the framework provides a default.
