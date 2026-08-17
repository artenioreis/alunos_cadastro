## 2024-05-14 - Contextual ARIA labels on Icon-only buttons
**Learning:** Screen readers need context for actions in data tables. A button that just says 'Edit' isn't helpful when there are 10 rows. Using Jinja templating to inject the row's entity name (e.g., `aluno.nome_completo`) into the `aria-label` makes the action unambiguous (e.g., 'Edit aluno John Doe').
**Action:** Always check data tables for icon-only action columns and ensure their ARIA labels are dynamically generated with the row's primary identifier.
