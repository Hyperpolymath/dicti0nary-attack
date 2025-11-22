# RSR Framework Metadata

This directory contains metadata for Rhodium Standard Repository (RSR) Framework compliance.

## Files

### metadata.yml

Machine-readable compliance information:
- RSR version and compliance level
- Project information
- Category-by-category compliance status
- Improvement roadmap
- Next steps toward higher compliance

## Usage

### Check Compliance

```bash
# Using justfile
just validate-rsr

# Manual check
cat .rsr/metadata.yml
```

### View Detailed Report

See [RSR_COMPLIANCE.md](../RSR_COMPLIANCE.md) for a comprehensive compliance report.

## RSR Framework

The Rhodium Standard Repository Framework defines standards for:

1. **Documentation**: Complete project documentation
2. **.well-known/**: Standardized metadata (RFC 9116, etc.)
3. **Type Safety**: Compile-time or runtime type checking
4. **Memory Safety**: Protection against memory errors
5. **Offline-First**: Works without internet connectivity
6. **Build System**: Reproducible builds and automation
7. **Testing**: Comprehensive test coverage
8. **TPCF**: Tri-Perimeter Contribution Framework
9. **Security**: Secure development practices
10. **Community**: Inclusive community governance
11. **Licensing**: Clear licensing and attribution

## Current Status

- **Level**: Bronze ✅
- **Score**: 86%
- **Target**: Silver (90%+)

## Improvement Path

See `metadata.yml` for detailed next steps and improvement plan.

## References

- [RSR_COMPLIANCE.md](../RSR_COMPLIANCE.md): Full compliance report
- [SECURITY.md](../SECURITY.md): Security policy
- [CONTRIBUTING.md](../CONTRIBUTING.md): Contribution guidelines
- [.well-known/](./../.well-known/): Metadata directory

---

Last updated: 2025-11-22
