# Compliance Mappings

Framework-specific compliance mappings that trace each configuration in this
repository to the specific control requirement it satisfies.

## Mappings

| File | Framework | Focus |
|------|-----------|-------|
| `pci-dss-req10-mapping.md` | PCI-DSS 4.0 | Req. 10 — Log and monitor all access |
| `soc2-cc7-mapping.md` | SOC 2 Type II | CC7 — System Operations |
| `gdpr-art30-32-mapping.md` | GDPR | Art. 30/32 — Records and security of processing |
| `iso27001-a5-mapping.md` | ISO 27001:2022 | A.5.24/A.5.25/A.8.15 — Logging and monitoring |

## How to Use

Each mapping traces a control requirement to the specific file(s) in this
repository that implement it. An auditor can:

1. Start with the framework requirement (e.g., PCI-DSS 10.5.1)
2. Read the mapping to find which config files implement it
3. Verify the configuration satisfies the requirement
4. Run the verification scripts to confirm compliance

## Cross-Reference with jolarca-control

The audit checklists in `jolarca-control/audit/` reference this repository
for logging and monitoring controls. The mappings here provide the detail
that the checklists summarize.
