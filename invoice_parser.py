import re

DATE_PATTERNS = [
    r"[A-Za-z]+\s+\d{1,2},\s*\d{4}",     
    r"\d{1,2}/\d{1,2}/\d{4}",             
    r"\d{4}-\d{2}-\d{2}"                    
]


def extract_matching_date(text):
    for p in DATE_PATTERNS:
        m = re.search(p, text)
        if m:
            return m.group(0)
    return None


def extract_field_block(lines, label):
    for i, line in enumerate(lines):
        if label in line.lower():
            return " ".join(lines[i+1:i+4]).strip()
    return None


def extract_invoice_number(lines):
    for l in lines:
        m = re.search(r"INV[- ]?\d+", l, re.IGNORECASE)
        if m:
            return m.group(0)
    return extract_field_block(lines, "invoice number")


def extract_dates(lines):
    invoice_date = None
    due_date = None

    for line in lines:
        if "invoice date" in line.lower():
            invoice_date = extract_matching_date(line)
        if "due date" in line.lower():
            due_date = extract_matching_date(line)
            
    if not invoice_date:
        for l in lines:
            d = extract_matching_date(l)
            if d:
                invoice_date = d
                break

    return invoice_date, due_date


def extract_total(lines):
    for l in reversed(lines):
        m = re.search(r"\$?(\d+\.\d{2})", l)
        if "total" in l.lower() and m:
            return float(m.group(1))
    return None


def extract_items(lines):
    items = []
    in_table = False
    current = {}

    for l in lines:
        if "hrs" in l.lower() or "qty" in l.lower():
            in_table = True
            continue

        if not in_table:
            continue


        if re.fullmatch(r"\d+(\.\d+)?", l):
            if current:
                items.append(current)
            current = {"quantity": float(l)}
            continue

        price_match = re.search(r"\$?(\d+\.\d{2})", l)
        if price_match:
            val = float(price_match.group(1))
            if "price" not in current:
                current["price"] = val
            else:
                current["amount"] = val
            continue


        if any(c.isalpha() for c in l):
            current["item"] = l

    if current:
        items.append(current)
    return items


def parse_invoice(lines):
    lines = [l.strip() for l in lines if l.strip()]

    invoice_number = extract_invoice_number(lines)
    invoice_date, due_date = extract_dates(lines)
    bill_to = extract_field_block(lines, "to:")
    items = extract_items(lines)
    total = extract_total(lines)
    terms = next((l for l in lines if "payment" in l.lower()), None)

    return {
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "due_date": due_date,
        "bill_to": bill_to,
        "items": items,
        "total": total,
        "terms": terms
    }
