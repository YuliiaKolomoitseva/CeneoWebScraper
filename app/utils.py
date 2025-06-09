from deep_translator import GoogleTranslator
import os
import json
import pandas as pd

def extract_data(ancestor, selector=None, attribute=None, multiple=False):
    if selector:
        if multiple:
            if attribute:
                return [tag[attribute].strip() for tag in ancestor.select(selector)]
            return [tag.get_text().strip() for tag in ancestor.select(selector)]
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute].strip()
            except TypeError:
                return None
        try:
            return ancestor.select_one(selector).get_text().strip()
        except AttributeError:
            return None
    try:
        return ancestor[attribute].strip()
    except (TypeError, KeyError):
        return None

def translate_data(text, source="pl", target="en"):
    return GoogleTranslator(source, target).translate(text=text)

def get_product_summaries():
    product_summaries = []
    opinions_dir = "app/static/opinions"

    for filename in os.listdir(opinions_dir):
        if filename.endswith(".json"):
            product_id = filename.replace(".json", "")
            with open(os.path.join(opinions_dir, filename), "r", encoding="utf-8") as f:
                opinions = json.load(f)
                if not opinions:
                    continue
                df = pd.DataFrame(opinions)

                summary = {
                    "product_id": product_id,
                    "name": df["product_name"][0] if "product_name" in df.columns and not df["product_name"].isnull().all() else product_id,
                    "opinions_count": len(df),
                    "pros_count": df["pros"].apply(lambda x: bool(x and str(x).strip())).sum() if "pros" in df.columns else 0,
                    "cons_count": df["cons"].apply(lambda x: bool(x and str(x).strip())).sum() if "cons" in df.columns else 0,
                    "avg_score": round(df["score"].mean(), 2) if "score" in df.columns and not df["score"].dropna().empty else 0
                }
                product_summaries.append(summary)

    return product_summaries
