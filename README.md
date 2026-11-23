# Account number claim audit

This offline static audit compares documentation claims about the ISO 13616 account number check digit with Python call shapes. It does not execute inspected code or access the network. Findings require human review.

## Usage

```sh
iban-validation-claim-audit audit .
python3 -m iban_validation_claim_audit audit . --json
iban-validation-claim-audit --version
```

The optional path defaults to the current directory. Use `--verbose` for details, repeat `--ignore PREFIX` to exclude relative path prefixes, and use `--fail-on medium` to include test-only findings in the failure threshold. Exit codes are 0 for success, 2 for findings at the threshold, and 1 for usage or I/O errors. The JSON result includes claims, denials, production evidence, test evidence and findings.

## Differentiation

This covers the account number check digit, not generic input checks, bank account details extraction, book number ISBN checks, serial number ISSN checks, business identifier codes, payment processing, credit card extraction, authentication, password hashing, password generation, PDF encryption, email sending, SMS sending, document extraction, barcode scanning, email address checks, phone number checks, password strength, JSON Schema checks, date checks, credit card checks, domain checks, URL checks, or IP address checks.

JSON decoding, regular expression matching, URL parsing, network fetching, DNS resolution, barcode generation, account number formatting, conversion, generation, and bank registry lookup are separate operations.

Other families cover spreadsheet reading and generation, word-document reading and generation, presentation reading and generation, PDF extraction, generation, merging, splitting, rotation, form-filling, watermarking, redaction, compression and annotation, table extraction, OCR, document extraction, e-signature, screen recording, video generation, QR code generation, barcode generation and scanning, audio mixing, generation and editing, source separation, speech recognition, text-to-speech, noise suppression, music generation and transcription. These claims are outside this audit's phrase lists.

## Limitations

Exact phrases are matched without understanding meaning. Each phrase below may be a false positive; review its context.

```text
validate iban
```

A database or remote-service lookup may be intended.

```text
check iban
```

A manual runbook step may be intended.

```text
iban validation
```

A roadmap feature may be intended.

```text
iban validator
```

A hosted page may be intended.

```text
valid iban
```

Advice to a reader may be intended.

```text
iban is valid
```

A successful lookup may be intended.

```text
iban number validation
```

A specification section may be intended.

```text
validate bank account number
```

A comparison against a bank list may be intended.

```text
verify iban
```

A registry existence check may be intended.

```text
detect invalid iban
```

A length-only rule may be intended.

```text
iban well formed
```

A theoretical discussion may be intended.

```text
is valid iban
```

A generated number may be intended.

```text
iban format validation
```

A spacing-only rule may be intended.

```text
validate iban code
```

An allow-list lookup may be intended.

```text
iban check
```

A manual runbook step may be intended.

```text
bank account number validation
```

A specification section may be intended.

```text
iban account validation
```

A design document concept may be intended.


Compacting alone only reshapes a number.

Formatting alone only reshapes a number.

Computing check digits alone is not evidence, even if compared later.

Generating a number does not judge input.

Reading an object attribute does not judge input; this includes compact, formatted, country_code, bank_code, account_code, bic and length.

Constructing a business identifier object is a different operation.

Constructing an IbanValidation object alone is not evidence.

Matching an account pattern with a regular expression alone is not evidence.

Variable chains the tracer cannot follow are missed.

A bare import without a call is not evidence.

A roadmap claim still counts.

A changelog claim still counts.

A TODO claim still counts.

A denial outside the listed phrases may be missed.

A claim outside the root README and docs directories is invisible.

Evidence split across modules is missed.

Locally defined route names shadow imports, including thin wrappers.

Dead code counts as evidence.

Subprocess calls are not evidence.

A generic input check is not evidence.

An email address check is not evidence.

A phone number check is not evidence.

A URL check is not evidence.

An IP address check is not evidence.

A domain check is not evidence.

A book number check is not evidence.

A serial number check is not evidence.

An extraction call is not evidence.

A locally defined generic name is shadowed.

Generic names reached through unsupported alias chains are missed.

Paraphrases outside the phrase lists are invisible.

Implementations in other languages are invisible.

Dynamic imports and runtime plugins are invisible.

Source under fixtures, docs and examples is excluded; tests count separately.

Syntax-invalid files provide no evidence.

A bare call to an unimported library name is not evidence.

An unknown base with a library-specific method is not evidence.

Payment processing is not evidence.

Strings and comments are not evidence.
