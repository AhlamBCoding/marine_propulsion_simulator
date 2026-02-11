# Security Architecture

This marine propulsion simulator is designed with cloud security best practices, demonstrating secure-by-design principles applicable to enterprise cloud platforms.

## Security Features

### 1. Secure Development Pipeline (DevSecOps)

**Automated Security Scanning:**
- **Static Application Security Testing (SAST)**: Bandit scans Python code for security issues
- **Software Composition Analysis (SCA)**: Safety checks dependencies for known vulnerabilities
- **Secret Detection**: Gitleaks prevents credential exposure in commits
- **Container Scanning**: Trivy identifies vulnerabilities in Docker images

**CI/CD Security Gates:**
- All security scans run automatically on every commit
- Pull requests require passing security checks
- Failed scans block deployment

### 2. Infrastructure Security

**Encryption:**
- TLS 1.2+ for data in transit
- AES-256 for data at rest
- Encrypted container environment variables

**Network Isolation:**
- Private endpoints for database access
- Deny-by-default network rules
- IP allowlisting for administrative access
- No public internet exposure by default

**Identity & Access Management:**
- Azure AD integration
- Multi-factor authentication (MFA) enforcement
- Role-based access control (RBAC)
- Managed identities (no hardcoded credentials)

**Secrets Management:**
- Azure Key Vault for sensitive data
- No credentials in code or environment files
- Automatic secret rotation

### 3. Container Security

**Image Hardening:**
- Minimal base image (Python 3.13.12-slim)
- Non-root user execution (UID 1000)
- Multi-stage builds for size reduction
- Layer optimization to reduce attack surface

**Runtime Security:**
- No privilege escalation
- Read-only root filesystem where possible
- Resource limits (CPU, memory)
- Security context constraints

### 4. Compliance & Governance

**CIS Benchmarks:**
Infrastructure aligned with CIS Azure Foundations v1.4.0:
- CIS 3.1: Storage encryption enabled
- CIS 4.3: Default network access denied
- CIS 5.1.1: Diagnostic settings enabled
- CIS 9.1: Azure AD authentication enforced

**Data Classification:**
- Engine specifications: Internal
- Simulation results: Internal
- Customer configurations: Confidential
- Audit logs: Restricted

**Retention Policies:**
- Simulation results: 90 days
- Audit logs: 365 days
- Backup data: 30 days

### 5. Monitoring & Logging

**Audit Events:**
- Authentication attempts (success/failure)
- Authorization decisions
- Data access operations
- Configuration changes
- Security scan results

**Alerting:**
- Failed authentication threshold: 5 attempts in 5 minutes
- Unauthorized access attempts
- Critical vulnerability detection
- Configuration drift from baseline

**Log Management:**
- Centralized logging to Azure Monitor
- Log integrity protection
- SIEM integration ready

## Threat Model

### Common Threats & Mitigations

| Threat | Risk Level | Mitigation |
|--------|-----------|------------|
| **Data Exposure** | High | Encryption at rest/transit, access controls |
| **Unauthorized Access** | High | Azure AD + MFA, RBAC, network isolation |
| **Credential Theft** | Medium | Key Vault, no hardcoded secrets, MFA |
| **Supply Chain Attack** | Medium | Dependency scanning, container scanning |
| **Container Breakout** | Medium | Non-root user, security contexts |
| **Code Injection** | Low | Input validation, static code analysis |

### Attack Surface

**Reduced Attack Surface:**
- Minimal exposed ports (only HTTPS if web interface added)
- Private network endpoints
- Minimal installed packages
- Regular vulnerability patching

## Security Testing

### Local Security Scanning

```bash
pip install bandit safety

# Run static code analysis
bandit -r src/ -f json -o bandit-report.json

# Check dependency vulnerabilities
safety check --json

# Scan for secrets (requires gitleaks installation)
gitleaks detect --source . --report-path gitleaks-report.json

docker build -t marine-simulator:latest .
docker run --rm aquasec/trivy image marine-simulator:latest
```

### Infrastructure Security Validation

```bash
# tfsec for Terraform scanning
https://github.com/aquasecurity/tfsec

# for scanning Terraform configurations
tfsec terraform/

# Validate Terraform compliance
terraform validate
terraform plan
```

## Security Best Practices documented and implemented

### Code Security
- No hardcoded credentials
- Input validation on all external data
- SQL parameterized queries (prevents injection)
- Error handling without sensitive data exposure
- Secure random number generation where needed

### Container Security
- Non-root user execution
- Minimal base image
- No unnecessary packages
- Explicit port exposure
- Health checks implemented

### Infrastructure Security
- Encryption enabled everywhere
- Network segmentation
- Least privilege access
- Audit logging enabled
- Compliance tagging

## Incident Response

### Response Procedures

1. **Detection**: Automated alerts via Azure Monitor
2. **Containment**: 
   - Isolate affected resources
   - Revoke compromised credentials
   - Block suspicious IP addresses
3. **Investigation**: Review audit logs and security scan results
4. **Remediation**: 
   - Apply security patches
   - Update security configurations
   - Rotate credentials
5. **Recovery**: Restore from clean backups if needed
6. **Lessons Learned**: Update threat model and controls

### Contact
**Security Issues**: Report via GitHub Security Advisories or email
**Vulnerability Disclosure**: Responsible disclosure appreciated - 90 day disclosure timeline

## Compliance Frameworks

### Applicable Standards
- CIS Azure Foundations Benchmark v1.4.0
- ISO 27001:2013 (Information Security Management)
- SOC 2 Type II (Security, Availability, Confidentiality)
- NIST Cybersecurity Framework

### Compliance Evidence
- Infrastructure-as-Code in Git (audit trail)
- Automated compliance scanning
- Security control documentation
- Audit logs retained for 365 days

## References

- [CIS Azure Foundations Benchmark](https://www.cisecurity.org/benchmark/azure)
- [Azure Security Best Practices](https://docs.microsoft.com/azure/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Container Security Best Practices](https://kubernetes.io/docs/concepts/security/)