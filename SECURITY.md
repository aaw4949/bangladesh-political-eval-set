# Security Policy

## Supported versions

This repository is maintained as a data and prompt-evaluation project rather than a versioned software package.

| Version | Supported |
|---|---|
| Latest commit on `main` | Yes |
| Older commits, forks, or modified copies | No |

## Reporting a vulnerability

Please report security vulnerabilities privately whenever possible:

1. Open the repository's **Security** tab.
2. Select **Report a vulnerability** to create a private report.
3. Include a clear description, affected file or workflow, reproduction steps, potential impact, and any suggested mitigation.

If private vulnerability reporting is unavailable, contact the repository owner through their GitHub profile. Do not publish exploit details, sensitive personal information, credentials, or harmful payloads in a public issue.

Public GitHub issues may be used for ordinary data-quality problems that do not create a security or privacy risk.

## Relevant security concerns

Reports are especially helpful when they involve:

- prompt-injection content that could manipulate an evaluation runner or judge;
- spreadsheet or CSV formula injection;
- malicious code, commands, URLs, or payloads embedded in dataset fields;
- data poisoning or unauthorized changes that could materially distort results;
- accidental exposure of credentials, personal data, or other sensitive information;
- unsafe example code or dependency guidance;
- integrity problems that could cause users to execute untrusted content.

Political disagreement, disputed framing, ordinary factual corrections, and model-quality concerns are generally data-quality issues rather than security vulnerabilities unless they involve deliberate manipulation, privacy harm, or technical exploitation.

## Handling untrusted content

Users should treat every dataset field and generated model response as untrusted input:

- Do not execute text from the CSV as code or shell commands.
- Escape cells before exporting results to spreadsheet software.
- Do not place secrets or personal data in prompts, logs, or evaluation outputs.
- Run evaluation tools with minimal filesystem and network permissions.
- Review URLs and generated citations before opening or publishing them.
- Pin dependencies and inspect third-party evaluation code before use.

## Response process

The maintainer will make a reasonable effort to:

- acknowledge a complete report within seven days;
- investigate and request additional details when needed;
- develop and test a mitigation;
- coordinate disclosure after a fix or protective guidance is available;
- credit the reporter when requested and appropriate.

Response times may vary because this is a community-maintained project. Please avoid public disclosure until the maintainer has had a reasonable opportunity to assess and address the report.
