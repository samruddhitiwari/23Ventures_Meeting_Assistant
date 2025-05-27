from datetime import datetime
import spacy
import dateparser
from typing import Optional, Dict, List, Tuple
import logging

nlp = spacy.load("en_core_web_sm")

def parse_query(query: str) -> Dict[str, List[Tuple[datetime, datetime]]]:
    """
    Extracts structured date ranges, actions (verbs), and topics (ORG, GPE, etc.) from a query.
    """
    doc = nlp(query)
    results = {
        "date_ranges": [],
        "actions": [],
        "topics": []
    }

    # Extract date expressions
    date_expressions = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    if not date_expressions:
        date_expressions = [query]  # fallback

    for expr in date_expressions:
        try:
            parsed = dateparser.parse(expr, settings={'PREFER_DATES_FROM': 'future', 'RETURN_AS_TIMEZONE_AWARE': False})
            if parsed:
                if " to " in expr or "-" in expr:
                    parts = expr.split(" to ") if " to " in expr else expr.split("-")
                    start_end = [dateparser.parse(p.strip()) for p in parts]
                    if len(start_end) == 2 and all(start_end):
                        results["date_ranges"].append((start_end[0], start_end[1]))
                else:
                    results["date_ranges"].append((parsed, parsed))
        except Exception as e:
            logging.error(f"Date parsing error: {e}")

    results["actions"] = [tok.lemma_ for tok in doc if tok.pos_ == "VERB"]
    results["topics"] = [ent.text for ent in doc.ents if ent.label_ in {"ORG", "PRODUCT", "GPE", "EVENT"}]

    return results
