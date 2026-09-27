# Artifact Model

An **artifact family** has one authoritative producer, a schema or version declaration when applicable, a required population rule, a publication surface, and one or more consumers. A **reference** links a record to another file or version in the same candidate. A **candidate** consists of eight kit trees, the generated site and static export, release archives, and the staged checksummed release directory. A **finding** records its classification, source-to-consumer trace, reproduction status, and disposition.

The matrix in [contracts/coverage-matrix.md](contracts/coverage-matrix.md) is the reviewed family inventory. It groups files by semantic contract rather than repeating the same row for every brand or platform variant. Each row applies to all eight production brands unless it explicitly says optional.
