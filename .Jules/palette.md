## 2023-10-24 - Missing ARIA labels on icon-only buttons
**Learning:** Found a recurring pattern in the templates where icon-only buttons (like the sidebar toggle, alert close buttons, and user deletion buttons) lacked `aria-label` attributes. This made these controls inaccessible to screen reader users, as the inner icon elements provide no context.
**Action:** Consistently add `aria-label` to icon-only buttons to clearly state their purpose, and set `aria-hidden="true"` on the decorative icon elements within them.
