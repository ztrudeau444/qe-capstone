

# Manual keyboard-only pass: /login

Date: 2026-10-14 · Tester: Zoe Trudeau · Browser: Firefox · No mouse used

| Check | Result | Evidence |
|---|---|---|
| Focus visible on every item | Pass. A clear outline shows where I am (blue ring on the inputs) | keyboard-back-to-form.png |
| Logical Tab order | Pass. Skip → Talks → Submit a talk → Reviewer sign-in → Email → Password → Sign in | login-page-rendered.png |
| Skip link | Pass. Enter on "Skip to main content", then Tab lands on Email, past the menu | |
| Fill and submit by keyboard | Pass. Typed both fields, pressed Enter, the form submitted | |
| Result after submit | **Fail.** A raw 422 JSON error page; no readable message and no link back (gap #17) | keyboard-login-submit-422.png |
| Keyboard traps | None. Alt+← returns to the form | keyboard-back-to-form.png |

Notes: going back clears both fields, so the user must retype everything.
The real fix is gap #17: the form sends form data but /api/login expects JSON.
