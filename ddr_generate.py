

def generate_ddr_report(document_data):

    report = "\n===== DDR REPORT =====\n"

    report += "\n1. Property Issue Summary\n"
    report += f"Total areas found: {len(document_data.area_wise_observations)}\n"

    report += "\n2. Area-wise Observations\n"

    for area in document_data.area_wise_observations:
        report += f"\n➤ {area.area}\n"

        for issue in area.issues:
            report += f"- Issue: {issue.description}\n"
            report += f"- Severity: {issue.severity}\n"
            if issue.image and issue.image != "Not Available":
                report += f"![Image]({issue.image})\n"
            else:
                report += "Image Not Available\n"

    report += "\n3. Probable Root Cause\n"
    report += document_data.probable_root_cause

    report += "\n4. Severity Assessment\n"
    report += document_data.severity_assessment

    report += "\n5. Recommended Actions\n"
    for action in document_data.recommended_actions:
        report += f"- {action}\n"

    report += "\n6. Missing Information\n"
    for item in document_data.missing_or_unclear_information:
        report += f"- {item}\n"

    return report