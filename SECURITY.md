# Security Policy

## Scope

Security reports are relevant when they involve:

- unsafe URL-fetching or SSRF guidance;
- crawler or WAF rules that expose protected content;
- prompt-injection or hidden-instruction handling;
- secrets, credentials, private observations, or customer data in examples or output contracts;
- instructions that encourage policy circumvention, impersonation, deceptive promotion, or unauthorized access;
- generated patches that weaken authentication, authorization, privacy, or data integrity.

## Reporting

Use GitHub private vulnerability reporting for this repository when available.

When private reporting is unavailable, open a minimal issue requesting a private contact channel. Do **not** include exploit details, customer information, credentials, or reproduction secrets in the public issue.

Include:

- affected file or workflow;
- impact;
- minimal reproduction;
- safe remediation suggestion;
- whether active exploitation is suspected.

## Response principles

- Preserve evidence and affected versions.
- Patch the shared root cause.
- Add one deterministic regression check.
- Do not publish sensitive details until users have a reasonable remediation path.
- Never weaken validation, access control, or disclosure merely to improve search or AI visibility.
