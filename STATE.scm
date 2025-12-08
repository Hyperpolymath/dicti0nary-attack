;;; STATE.scm - Project State Document
;;; dicti0nary-attack: Security research utility for non-dictionary password testing
;;; Format: Guile Scheme S-expressions (Rhodium Standard)

;;;============================================================================
;;; METADATA
;;;============================================================================

(metadata
  (version . "1.0.0")
  (project . "dicti0nary-attack")
  (created . "2025-12-08")
  (updated . "2025-12-08")
  (author . "hyperpolymath")
  (license . "GPL-3.0"))

;;;============================================================================
;;; CURRENT POSITION
;;;============================================================================

(current-position
  (version . "0.1.0-alpha")
  (phase . "early-development")
  (rsr-compliance . "bronze")
  (rsr-score . "86%")
  (tpcf-perimeter . "perimeter-3-community-sandbox")

  (summary . "Core implementation complete with 5 password generators,
              multi-algorithm hash cracker, CLI interface, and web interface.
              Well-documented codebase with comprehensive test suite and
              Docker support. Ready for community feedback and iteration.")

  (implemented-features
    (generators
      (leetspeak . "complete")
      (phonetic . "complete")
      (pattern . "complete")
      (random . "complete")
      (markov . "complete"))
    (crackers
      (hash-cracker . "complete")
      (algorithms . "md5 sha1 sha224 sha256 sha384 sha512 blake2b blake2s")
      (parallel-processing . "complete"))
    (interfaces
      (cli . "complete")
      (web . "complete")
      (python-api . "complete"))
    (infrastructure
      (testing . "complete")
      (docker . "complete")
      (ci-cd . "complete")
      (documentation . "complete")))

  (codebase-metrics
    (language . "python-3.10+")
    (loc-estimate . "~3000")
    (test-count . "50+")
    (test-coverage-target . ">80%")))

;;;============================================================================
;;; ROUTE TO MVP v1.0.0
;;;============================================================================

(mvp-roadmap
  (target-version . "1.0.0")
  (current-version . "0.1.0-alpha")

  (milestone-v0.2.0
    (name . "RSR Silver Compliance")
    (completion . 0)
    (tasks
      ("Add GitHub issue templates" . pending)
      ("Add GitHub PR templates" . pending)
      ("Add SPDX identifiers to source files" . pending)
      ("Add license headers to all source files" . pending)
      ("Enable Dependabot for dependency updates" . pending)
      ("Integrate mypy for static type checking" . pending)
      ("Achieve 90%+ RSR compliance score" . pending)))

  (milestone-v0.3.0
    (name . "Enhanced Type Safety & Security")
    (completion . 0)
    (tasks
      ("Achieve 100% type hints coverage" . pending)
      ("Add runtime validation with pydantic" . pending)
      ("Conduct formal security audit" . pending)
      ("Performance optimization pass" . pending)
      ("Extended API documentation" . pending)
      ("Plugin system completion" . pending)))

  (milestone-v0.4.0
    (name . "WASM Integration")
    (completion . 0)
    (tasks
      ("Complete Chapel to WASM compilation" . pending)
      ("Browser-based password generation" . pending)
      ("Sandboxed execution environment" . pending)
      ("Performance benchmarks vs Python" . pending)))

  (milestone-v1.0.0
    (name . "Stable Release")
    (completion . 0)
    (tasks
      ("Feature freeze and stabilization" . pending)
      ("Comprehensive security review" . pending)
      ("Performance optimization" . pending)
      ("Complete documentation suite" . pending)
      ("Community feedback integration" . pending)
      ("Public release announcement" . pending))))

;;;============================================================================
;;; KNOWN ISSUES & BLOCKERS
;;;============================================================================

(issues
  (technical
    (type-safety
      (severity . "medium")
      (description . "Python is dynamically typed; relies on type hints rather
                      than compile-time verification")
      (mitigation . "Extensive type hints + mypy integration planned"))

    (memory-safety
      (severity . "low")
      (description . "Python uses garbage collection, not zero-cost memory safety
                      like Rust")
      (mitigation . "Acceptable for v1.0; Rust rewrite considered for v2.0"))

    (chapel-wasm-integration
      (severity . "medium")
      (description . "Chapel/WASM modules exist but not fully integrated with
                      Python codebase")
      (mitigation . "Planned for v0.4.0 milestone"))

    (plugin-system
      (severity . "low")
      (description . "Plugin framework exists but lacks documentation and
                      community plugins")
      (mitigation . "Complete plugin system in v0.3.0")))

  (compliance
    (issue-templates
      (severity . "low")
      (description . "Missing GitHub issue templates")
      (impact . "Community score at 60%"))

    (pr-templates
      (severity . "low")
      (description . "Missing GitHub PR templates")
      (impact . "Community score at 60%"))

    (license-headers
      (severity . "low")
      (description . "Source files missing SPDX identifiers and license headers")
      (impact . "Licensing score at 50%"))

    (dependabot
      (severity . "low")
      (description . "Dependabot not yet enabled")
      (impact . "Automated dependency updates not active")))

  (documentation
    (api-completeness
      (severity . "low")
      (description . "API documentation exists but could be more comprehensive")
      (mitigation . "Expand in v0.3.0"))))

;;;============================================================================
;;; QUESTIONS FOR STAKEHOLDER
;;;============================================================================

(questions
  (architecture
    (q1
      (question . "Should we prioritize Rust rewrite for performance-critical
                   components (generators, hash cracker) in v2.0?")
      (context . "Current Python implementation is functional but Rust would
                  provide compile-time type safety, memory safety, and likely
                  significant performance improvements")
      (options . ("Maintain Python-only"
                  "Hybrid Python+Rust"
                  "Full Rust rewrite")))

    (q2
      (question . "What is the priority level for WASM browser integration?")
      (context . "Chapel WASM modules exist but integration is incomplete.
                  Browser-based execution would expand accessibility but
                  requires significant development effort")
      (options . ("High priority for v0.4.0"
                  "Medium priority, defer to v1.x"
                  "Low priority, nice-to-have"))))

  (features
    (q3
      (question . "Should we add support for additional hash algorithms?")
      (context . "Currently support MD5, SHA family, BLAKE2. Could add
                  bcrypt, scrypt, Argon2, NTLM for broader use cases")
      (options . ("Add bcrypt/scrypt/Argon2"
                  "Add NTLM for Windows testing"
                  "Current algorithms sufficient")))

    (q4
      (question . "Should we integrate with specific CTF platforms?")
      (context . "Direct integration with platforms like HackTheBox, TryHackMe,
                  or CTFd could improve usability for CTF participants")
      (options . ("Yes, prioritize CTF platform integration"
                  "Provide documentation/examples only"
                  "Not a priority"))))

  (community
    (q5
      (question . "What is the target audience priority?")
      (context . "Tool serves multiple audiences: security researchers,
                  CTF participants, penetration testers, academics")
      (options . ("Security researchers primary"
                  "CTF/educational primary"
                  "Professional pentesters primary"
                  "Equal focus all audiences")))

    (q6
      (question . "Should we establish a Discord/Matrix community?")
      (context . "GitHub Discussions available but dedicated chat could
                  improve community engagement")
      (options . ("Yes, create Discord"
                  "Yes, create Matrix (open source preference)"
                  "GitHub Discussions sufficient")))))

;;;============================================================================
;;; LONG-TERM ROADMAP
;;;============================================================================

(long-term-roadmap
  (horizon . "2+ years")

  (phase-1-foundation
    (versions . "0.1.x - 0.4.x")
    (timeline . "current")
    (goals
      ("Achieve RSR Silver compliance (90%+)" . priority-high)
      ("Complete core feature set" . priority-high)
      ("WASM browser integration" . priority-medium)
      ("Plugin ecosystem foundation" . priority-medium)
      ("Community building" . priority-medium)))

  (phase-2-maturity
    (versions . "1.0.x - 1.x")
    (goals
      ("Stable public release" . priority-high)
      ("RSR Gold compliance (95%+)" . priority-medium)
      ("Comprehensive security audit" . priority-high)
      ("Performance optimization" . priority-medium)
      ("Extended algorithm support" . priority-low)
      ("CTF platform integrations" . priority-low)))

  (phase-3-evolution
    (versions . "2.0+")
    (goals
      ("Rust rewrite for core algorithms" . priority-medium)
      ("Formal verification for critical paths" . priority-low)
      ("TLA+ specifications for concurrency" . priority-low)
      ("Multi-language SDK support" . priority-low)
      ("Enterprise features" . priority-low)
      ("Cloud-native deployment options" . priority-low)))

  (aspirational-goals
    ("Become reference implementation for non-dictionary password testing")
    ("RSR Platinum compliance")
    ("Academic citations and research papers")
    ("Integration into major security frameworks")
    ("Active contributor community")))

;;;============================================================================
;;; DEPENDENCIES
;;;============================================================================

(dependencies
  (runtime
    ("python" . ">=3.10")
    ("click" . ">=8.1.0")
    ("flask" . ">=3.0.0")
    ("rich" . ">=13.0.0")
    ("pyyaml" . ">=6.0")
    ("tqdm" . ">=4.66.0")
    ("colorama" . ">=0.4.6"))

  (development
    ("pytest" . ">=7.4.0")
    ("pytest-cov" . ">=4.1.0")
    ("flake8" . ">=6.1.0")
    ("black" . ">=23.0.0")
    ("mypy" . "planned"))

  (optional
    ("chapel" . "for WASM compilation")
    ("podman/docker" . "for containerization")
    ("rust" . "planned for v2.0")))

;;;============================================================================
;;; CRITICAL NEXT ACTIONS
;;;============================================================================

(next-actions
  (immediate
    (priority-1
      (action . "Add GitHub issue templates (bug, feature, custom)")
      (effort . "small")
      (impact . "RSR compliance improvement"))

    (priority-2
      (action . "Add GitHub PR template")
      (effort . "small")
      (impact . "RSR compliance improvement"))

    (priority-3
      (action . "Enable Dependabot for automated dependency updates")
      (effort . "small")
      (impact . "Security posture improvement")))

  (short-term
    (priority-4
      (action . "Add SPDX identifiers to all source files")
      (effort . "medium")
      (impact . "Licensing compliance"))

    (priority-5
      (action . "Integrate mypy for static type checking in CI")
      (effort . "medium")
      (impact . "Type safety improvement"))

    (priority-6
      (action . "Write comprehensive plugin development guide")
      (effort . "medium")
      (impact . "Developer ecosystem")))

  (medium-term
    (priority-7
      (action . "Complete Chapel/WASM integration")
      (effort . "large")
      (impact . "Browser-based functionality"))

    (priority-8
      (action . "Formal security audit")
      (effort . "large")
      (impact . "Security assurance"))

    (priority-9
      (action . "Performance optimization benchmarks")
      (effort . "medium")
      (impact . "User experience"))))

;;;============================================================================
;;; HISTORY
;;;============================================================================

(history
  (snapshot
    (date . "2025-12-08")
    (version . "0.1.0-alpha")
    (completion . 35)
    (notes . "Initial state capture. Core implementation complete.
              RSR Bronze compliance achieved at 86%. Ready for
              community feedback and v0.2.0 planning."))

  ;; Future snapshots will be appended here
  ;; (snapshot (date . "YYYY-MM-DD") (version . "x.x.x") (completion . N) (notes . "..."))
  )

;;;============================================================================
;;; EOF
;;;============================================================================
