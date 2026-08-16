## 2024-05-18 - Ensure icon-only buttons are accessible
**Learning:** Action buttons that contain only icons (e.g., Bootstrap icons) need an explicit `aria-label` attribute on the button element to provide an accessible name for screen readers, and the icon element itself should have `aria-hidden="true"` to prevent redundant or confusing announcements.
**Action:** Always ensure any icon-only button or link includes `aria-label` to describe its action, and use `aria-hidden="true"` on the enclosed icon.
