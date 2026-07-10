# Enterprise Guardrails Platform

A lightweight reference implementation demonstrating how configurable AI guardrails can be managed as reusable, versioned policies for enterprise Generative AI applications.

The objective of this project is not to provide a production ready guardrail solution. Instead, it demonstrates an architectural approach for building a centralized guardrails platform that supports multiple business teams while enabling governance, runtime configuration and controlled policy deployment.

Policies are versioned, centrally managed and evaluated independently of application code.

Find guardrail implementation references at [My git existing project - genai-security-owasp](https://github.com/shrawanika-w/genai-security-owasp "Shrawanika's git repo genai-security-owasp")

---

# Motivation

As organizations adopt Generative AI across multiple business units, individual teams often implement their own prompt validation, safety rules and content filtering. This often results in duplicated logic, inconsistent governance and difficult operational management.

A centralized guardrails platform provides:

- Common enterprise guardrails
- Team specific customizations
- Version controlled policies
- Runtime configuration without application deployment
- Controlled rollout and rollback
- Governance and auditability

---

# Problem Statement

Enterprise AI platforms require configurable guardrails that evolve independently from application code.

Typical requirements include:

- Different business teams require different policies.
- Security teams review and approve policy changes.
- Policy updates should not require application redeployment.
- Every request should be traceable to the policy version used for evaluation.
- New policies should be validated before production rollout.
- Failed policy releases should be rolled back immediately.

This repository demonstrates one possible implementation of these requirements.

---

# Architecture

```text
                        Git Repository
                (Version controlled YAML policies)
                              │
                              ▼
                    +------------------+
                    | Policy Registry  |   Tracks lifecycle and active versions
                    +------------------+
                              │
                              ▼
                    +------------------+
                    |  Policy Loader   |   Loads and validates YAML policies
                    +------------------+
                              │
                              ▼
                    +------------------+
                    | Policy Evaluator |   Applies configured guardrails
                    +------------------+
                              │
                              ▼
                    +------------------+
                    | Evaluation Result|   Decision and evaluation details
                    +------------------+
                              │
                              ▼
                         AI Application
```

---

# Repository Structure

```text
enterprise-guardrails-platform/
│
├── README.md
├── docs/
│   └── ARCHITECTURE.md
│
├── app/
│   ├── main.py
│   ├── policy/
│   │   ├── policy_manager.py
│   │   ├── registry.py
│   │   ├── loader.py
│   │   ├── evaluator.py
│   │   ├── rollout.py
│   │   ├── metrics.py
│   │   └── audit.py
│   └── models/
│       ├── policy.py
│       └── evaluation_result.py
│
└── policies/
    └── global/
        ├── metadata.yaml
        ├── v1/
        │   └── safety.yaml
        └── v2/
            └── safety.yaml
    └── payments/
        ├── metadata.yaml
        ├── v1/
        │   └── safety.yaml
```

---

# Component Responsibilities

### Policy Registry

Responsible for policy lifecycle management.

- Discover available policy versions
- Publish new versions
- Enable canary deployment
- Roll back to previous versions
- Maintain active policy metadata

### Policy Loader

Responsible for loading policy configurations.

- Read YAML policy files
- Load global and team specific policies
- Resolve policy inheritance
- Validate policy schema

### Policy Evaluator

Responsible for runtime guardrail enforcement.

- Evaluate prompts
- Check toxicity thresholds
- Detect prompt injection
- Return allow or block decisions

### Evaluation Result

Represents the outcome of a policy evaluation.

Includes:

- Policy version
- Team
- Decision
- Matched rules
- Confidence score
- Execution time

---

# Key Design Principles

## Separation of Concerns

Application code should never contain hardcoded guardrail rules.

Instead of embedding logic such as:

```python
if toxicity_score > 0.8:
    block_request()
```

the application evaluates externally managed policies.

```yaml
toxicity_threshold: 0.80
block_hate: true
mask_pii: true
```

This allows policies to evolve without redeploying services.

---

# Policy Lifecycle

Every policy progresses through a controlled lifecycle.

```text
Draft
  ↓
Review
  ↓
Security Approval
  ↓
Published
  ↓
Canary
  ↓
Production
  ↓
Deprecated
  ↓
Archived
```

Each lifecycle transition is recorded for governance and audit purposes.

---

# Policy Versioning

Policies are immutable.

New changes create new versions rather than modifying existing policies.

```text
policies/

global/
    metadata.yaml
    v1/
        safety.yaml
    v2/
        safety.yaml
```

Every evaluation records:

- Policy version
- Timestamp
- Team
- Evaluation result

This provides complete traceability and simplifies rollback.

---

# Team Specific Configuration

A common enterprise policy serves as the default configuration.

Business teams inherit the enterprise policy and override only the settings they require.

Example:

Enterprise Policy

```yaml
max_tokens: 8000
```

Payments Team

```yaml
max_tokens: 4000
```

Retail Team

```yaml
max_tokens: 16000
```

This minimizes duplication while allowing controlled customization.

---

# Runtime Configuration

Policies are loaded dynamically.

No application deployment is required after a policy update.

```text
Git Repository
      ↓
Policy Registry
      ↓
Runtime Cache
      ↓
Guardrails Engine
```

---

# Policy Storage Strategy

This implementation separates policy authoring from policy execution.

| Component          | Storage             |
| ------------------ | ------------------- |
| Policy definitions | Git Repository      |
| Runtime cache      | In Memory / Redis   |
| Policy metadata    | Relational Database |

Git provides version control, code review and rollback.

Redis provides low latency runtime access.

The database stores ownership, lifecycle information, deployment history and audit records.

---

# Canary Deployment

Policy updates should be deployed gradually.

```text
Version 2

↓

5%

↓

20%

↓

50%

↓

100%
```

Operational metrics are continuously monitored throughout the rollout.

---

# Rollback Strategy

Rollback does not require application redeployment.

```text
Current Policy

v3

↓

Rollback

↓

v2
```

Changing the active version in the registry restores the previous policy immediately.

---

# Precision and Recall Evaluation

Every policy release should be validated using a representative evaluation dataset.

Example:

| Metric    | Previous | Candidate |
| --------- | -------: | --------: |
| Precision |      95% |       86% |
| Recall    |      73% |       92% |

A higher recall detects more unsafe requests, while lower precision may increase false positives.

Instead of immediately promoting the new policy, the recommended approach is to:

- Deploy using a canary rollout.
- Measure false positives and false negatives.
- Monitor customer impact.
- Compare operational metrics.
- Promote only if business objectives are achieved.

This balances technical quality with business outcomes.

---

# API Overview

```text
GET  /policy/current
GET  /policy/version
POST /policy/evaluate
POST /policy/publish
POST /policy/rollback
GET  /metrics
```

---

# Future Enhancements

- Open Policy Agent (OPA) integration
- Cedar policy language
- Dynamic feature flags
- GitOps deployment pipeline
- Multi tenant policy inheritance
- LLM based policy recommendations
- Human approval workflow
- Policy simulation before rollout
- Governance dashboard

---

# Disclaimer

This project is intended as a reference implementation demonstrating architectural concepts for enterprise AI governance and configurable guardrails.

Production concerns such as distributed caching, authentication, authorization, observability, resilience and high availability have been intentionally simplified to keep the implementation focused on policy lifecycle and management.
