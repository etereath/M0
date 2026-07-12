# Changelog

All notable changes to this project are documented in this file.

The format is based on Keep a Changelog, and this project follows Semantic Versioning.

## [0.2.0] - Unreleased

### Added

- Added a server-generated `project_create` request schema.
- Added the `CONTRACT_HEADER_BODY_MISMATCH` transport error and cross-channel envelope rules.
- Added schema-driven generation and bidirectional synchronization checks for Python and TypeScript enums.

### Changed

- Release packaging now runs only for pushed `v*` tags.

## [0.1.0] - 2026-07-12

### Added

- Established the automation platform public-contract authority repository.
- Published a platform-neutral M0 v0.1 contract baseline.
- Added OpenAPI, JSON Schema, state machines, permissions, error codes, fixtures, and Python/TypeScript reference types.
- Added repeatable validation, release packaging, and GitHub Actions workflows.

### Changed

- Moved implementation-specific platform, deployment, and business-module mappings to the private `automation-platform-internal-mappings` repository.
- Declared the M0 `v0.1.0` business semantics frozen and documented the fixed-version dependency policy for M1–M5.
