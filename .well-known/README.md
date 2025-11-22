# .well-known Directory

This directory contains standardized metadata files following RFC 9116 and other web standards.

## Files

### security.txt (RFC 9116)

Security contact information and vulnerability reporting instructions.

**Standard**: [RFC 9116](https://www.rfc-editor.org/rfc/rfc9116.html)
**Purpose**: Provide a standard way to report security vulnerabilities
**Format**: Plain text with specific fields

### ai.txt

AI training and usage policy for this repository.

**Purpose**: Specify how AI systems may interact with this code
**Format**: YAML-like key-value pairs
**Coverage**: Training data usage, attribution requirements, ethical constraints

### humans.txt

Information about the humans behind the project.

**Standard**: [humanstxt.org](http://humanstxt.org/)
**Purpose**: Credit the people and technology behind the site
**Format**: Plain text with structured sections

## Usage

These files are typically served at the root of a website:

```
https://example.com/.well-known/security.txt
https://example.com/.well-known/ai.txt
https://example.com/.well-known/humans.txt
```

For this repository, they provide metadata about:
- How to report security issues
- AI training permissions and restrictions
- Project contributors and technology stack

## Standards Compliance

### RFC 9116 (security.txt)

Required fields:
- ✅ Contact: How to reach security team
- ✅ Expires: When this file should be updated
- ✅ Preferred-Languages: Language preferences
- ✅ Canonical: Canonical URL for this file

Optional fields:
- ✅ Policy: Link to security policy
- ✅ Acknowledgments: Security researcher recognition

### humanstxt.org

Recommended sections:
- ✅ TEAM: Project contributors
- ✅ THANKS: Acknowledgments
- ✅ TECHNOLOGY: Tech stack
- ✅ LICENSE: Licensing information
- ✅ SITE: Project links

### ai.txt (Emerging Standard)

Key policies:
- ✅ Training permissions
- ✅ Attribution requirements
- ✅ Ethical use constraints
- ✅ Security context
- ✅ License compliance

## Updating

### security.txt
- Update annually before expiration
- Update contact information as needed
- Keep canonical URL current

### ai.txt
- Review when AI policy changes
- Update for new ethical guidelines
- Sync with license changes

### humans.txt
- Update when contributors change
- Refresh technology stack
- Update statistics periodically

## Validation

### security.txt
Validate at: https://securitytxt.org/validator

### humans.txt
Check format at: http://humanstxt.org/

### ai.txt
No official validator yet (emerging standard)

## References

- [RFC 9116 - security.txt](https://www.rfc-editor.org/rfc/rfc9116.html)
- [humanstxt.org](http://humanstxt.org/)
- [securitytxt.org](https://securitytxt.org/)

---

Last updated: 2025-11-22
