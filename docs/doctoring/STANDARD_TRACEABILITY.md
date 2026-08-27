# ELUNVERA Standard Traceability

| External source | Product decision | Contract or document | Required evidence | Current status |
|---|---|---|---|---|
| ISO 10002:2018 | complaint intake, acknowledgement, investigation, remedy, follow-up | PRD, DATA_MODEL, complaint API | complaint E2E and audit receipt | Designed only |
| ISO 10004:2018 | versioned satisfaction observations and monitoring context | PRD, DATA_MODEL | instrument/model trace and reporting tests | Designed only |
| ISO/IEC 27001:2022 + Amd 1:2024 | security management concerns and evidence | SECURITY, THREAT_MODEL | implemented controls and independent audit | Designed only |
| ISO/IEC 27701:2025 | purpose, rights, retention, controller/processor context | PRIVACY, DATA_MODEL | privacy workflow and governance evidence | Designed only |
| NIST Privacy Framework 1.0 | privacy risk and lifecycle outcomes | PRIVACY, SECURITY | profile and control evidence | Designed only |
| ISO/IEC 42001:2023 | model inventory, approval, oversight, incident and monitoring | TRD, SECURITY, ADR-0008 | model lifecycle and review evidence | Designed only |
| NIST AI RMF 1.0 / NIST AI 600-1 | Govern, Map, Measure, Manage for AI claims | TEST_STRATEGY, THREAT_MODEL | TEVV, incident, prompt-injection evidence | Designed only |
| OWASP Top 10:2025 | web application risk baseline | SECURITY, TEST_STRATEGY | SAST, DAST, code review and tests | Designed only |
| OWASP API Security Top 10:2023 | object/property/function authorization and resource bounds | API_CONTRACT, SECURITY | API adversarial tests | Designed only |
| OpenAPI 3.2.0 | authoritative HTTP description | schemas/openapi.yaml | schema and SDK validation | Draft schema |
| AsyncAPI 3.1.0 | authoritative event description | schemas/asyncapi.yaml | schema and consumer tests | Draft schema |
| CloudEvents 1.0.2 | event envelope and replay identity | API_CONTRACT, schemas | duplicate/reorder tests | Draft schema |
| PostgreSQL 18.6 | UUIDv7, temporal and relational baseline | TRD, DATA_MODEL | real DB migration and restore | Not implemented |
| WCAG 2.2 | accessible CRM interface | UX_SPEC, Storybook inventory | automated and assistive-tech audit | Not implemented |
| Korean PIPA | lawful, purpose-limited personal-data processing | PRIVACY, SECURITY | jurisdiction-specific legal and operational review | Design reference |
| GDPR | rights, purpose, accountability where applicable | PRIVACY | territorial-scope and DPA review | Design reference |

“Designed only” means no compliance or certification claim may be made.
