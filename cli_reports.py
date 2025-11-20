from reports.reporter import generate_csv, generate_pdf

# Generate both reports
generate_csv("connections_report.csv")
generate_pdf("connections_report.pdf")
print("Reports generated successfully!")
