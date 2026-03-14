<p align="center">
<h1 align="center">AI Invoice OCR Pipeline</h1>
<p align="center">
Automated document processing system for extracting structured data from invoices and receipts.
</p>
</p>

---

# Overview

This project demonstrates an **end-to-end OCR document processing pipeline** for invoices.

The system converts invoices or receipts (PDF / images) into **structured machine-readable data**.

Example extracted fields:

- Invoice number
- Vendor name
- Invoice date
- Line items
- Total amount
- Payment terms

The goal is to simulate **real-world financial document automation pipelines used in fintech and ERP systems.**

---

# Features

• PDF and image invoice support  
• OCR with **EasyOCR**  
• Intelligent text cleaning and correction  
• Regex-based invoice parsing  
• Structured JSON output  
• Automated document processing pipeline  

---

# Example Output

```json
{
  "invoice_number": "INV-3337",
  "date": "Jan 25, 2016",
  "items": [
    {
      "description": "Web design",
      "qty": 1,
      "price": 85
    }
  ],
  "total": 93.50
}
