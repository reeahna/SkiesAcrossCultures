#!/usr/bin/env python3
"""
generate_data.py
----------------
Run this script to generate the data files needed for the visualizations.

Usage:
    python generate_data.py

Input files (must be in the same folder as this script):
    output.csv          - constellation data from Dr. Bucur
    star_metadata.ecsv  - star coordinate/magnitude data from Dr. Bucur

Output files (written to the same folder):
    geo_data.json       - used by skies_across_cultures.html
    star_map_data.json  - used by skies_star_map.html
"""

import json
import ast
import math
import pandas as pd

# ── Load raw data ─────────────────────────────────────────────────────────────
df = pd.read_csv("output.csv")

meta = pd.read_csv("star_metadata.ecsv", comment="#", sep=" ")
meta["MAIN_ID"] = meta["MAIN_ID"].str.strip()

# ── Culture coordinates (geographic) ─────────────────────────────────────────
COORDS = {
    "Ahtna":           (63.39, -148.95),
    "Anuta":           (-11.61, 169.86),
    "Ava Guaraní":     (-19.0, -63.0),
    "Banjara":         (21.15, 79.09),
    "Blackfoot":       (49.0, -113.0),
    "Bororo":          (-15.9, -52.3),
    "Bugis":           (-4.5, 120.0),
    "Dien":            (46.0, 0.5),
    "Gond":            (21.15, 79.09),
    "Gwich'in":       (66.56, -145.27),
    "Huave":           (16.19, -94.89),
    "IAU":             (50.5, 10.0),
    "Iroquois":        (43.0, -76.0),
    "Java":            (-7.5, 110.0),
    "K'iche'":       (15.0, -91.3),
    "Kalina":          (4.0, -57.0),
    "Kolam":           (19.5, 79.5),
    "Korku":           (21.5, 76.5),
    "Koyukon":         (65.7, -156.4),
    "Lower Tanana":    (64.9, -149.4),
    "Madura":          (-7.0, 113.3),
    "Malay":           (6.12, 100.37),
    "Mandar":          (-3.35, 119.1),
    "Maricopa":        (33.06, -112.04),
    "Mi'kmaq":        (44.65, -63.57),
    "Mocoví":          (-29.0, -60.5),
    "Nicobars":        (8.0, 93.5),
    "Pardhi":          (20.93, 77.75),
    "Pawnee":          (41.5, -98.0),
    "Romania":         (45.94, 24.97),
    "Ruelle":          (48.86, 2.35),
    "Sahtúot'įnę":    (65.18, -123.52),
    "Tewa":            (35.88, -106.08),
    "Thai":            (13.75, 100.52),
    "Toba":            (-24.0, -61.0),
    "Tutchone":        (60.72, -135.05),
    "Tzotzil":         (16.75, -92.67),
    "Wichí":           (-23.0, -63.5),
    "Yellowknives":    (62.46, -114.35),
    "Zuni":            (35.07, -108.85),
}

# ── Semantic category grouping ────────────────────────────────────────────────
GROUP_MAP = {
    "mammal": "Animal", "bird": "Animal", "fish": "Animal",
    "reptile": "Animal", "arthropod": "Animal",
    "humanoid": "Human", "body part": "Human",
    "man-made object": "Object", "architecture": "Object",
    "landscape": "Nature", "plant": "Nature",
    "abstract": "Abstract", "geometric": "Abstract", "group": "Abstract",
    "none": "Uncategorized", "other": "Uncategorized",
}

def parse_first_cat(val):
    if pd.isna(val) or val == "none":
        return "none"
    try:
        return ast.literal_eval(val)[0]
    except:
        return str(val)

# ── Build geo_data.json ───────────────────────────────────────────────────────
print("Building geo_data.json...")

df["raw_cat"] = df["con_category"].apply(parse_first_cat)
df["group"] = df["raw_cat"].apply(lambda x: GROUP_MAP.get(x.strip(), "Uncategorized"))
df["lat"] = df["cul_name"].map(lambda x: COORDS.get(x, (None, None))[0])
df["lon"] = df["cul_name"].map(lambda x: COORDS.get(x, (None, None))[1])

culture_summary = df.groupby("cul_name").agg(
    count=("con_id", "count"),
    region=("region", "first"),
    lat=("lat", "first"),
    lon=("lon", "first"),
    place=("place", "first"),
).reset_index().dropna(subset=["lat", "lon"])

# Grouped bars
bd = df.groupby(["cul_name", "group"]).size().reset_index(name="n")
totals = bd.groupby("cul_name")["n"].sum()
bd["total"] = bd["cul_name"].map(totals)
bd["pct"] = (bd["n"] / bd["total"] * 100).round(2)

# Raw category bars
rd = df.groupby(["cul_name", "raw_cat"]).size().reset_index(name="n")
rtotals = rd.groupby("cul_name")["n"].sum()
rd["total"] = rd["cul_name"].map(rtotals)
rd["pct"] = (rd["n"] / rd["total"] * 100).round(2)

geo_data = {
    "cultures": culture_summary.to_dict(orient="records"),
    "bars": bd.to_dict(orient="records"),
    "raw_bars": rd.to_dict(orient="records"),
    "totals": totals.to_dict(),
}

with open("geo_data.json", "w", encoding="utf-8") as f:
    json.dump(geo_data, f)
print(f"  -> geo_data.json written ({len(culture_summary)} cultures, {len(bd)} bar rows)")

# ── Build star_map_data.json ──────────────────────────────────────────────────
print("Building star_map_data.json...")

# Star lookup from metadata
star_lookup = {}
for _, row in meta.iterrows():
    mag = row["FLUX_V"]
    star_lookup[row["MAIN_ID"]] = {
        "ra":  float(row["RA_d"]),
        "dec": float(row["DEC_d"]),
        "mag": float(mag) if str(mag) not in ("", "nan") else None,
    }

# Build per-culture star sets, constellation lines with names
culture_stars = {}
culture_constellations = {}

for _, row in df.iterrows():
    culture = row["cul_name"]
    if pd.isna(row["con_lines"]) or pd.isna(row["con_name"]):
        continue
    try:
        lines = ast.literal_eval(row["con_lines"])
        names = ast.literal_eval(row["con_name"])
    except:
        continue

    english = names[0].get("english", "") if names else ""
    native  = names[0].get("native",  "") if names else ""

    if culture not in culture_stars:
        culture_stars[culture] = set()
        culture_constellations[culture] = []

    segments = []
    for line in lines:
        for i in range(len(line) - 1):
            s1, s2 = line[i].strip(), line[i+1].strip()
            if s1 in star_lookup and s2 in star_lookup:
                culture_stars[culture].add(s1)
                culture_stars[culture].add(s2)
                segments.append({
                    "x": [star_lookup[s1]["ra"],  star_lookup[s2]["ra"],  None],
                    "y": [star_lookup[s1]["dec"], star_lookup[s2]["dec"], None],
                })

    if segments:
        culture_constellations[culture].append({
            "english":  english,
            "native":   native,
            "segments": segments,
        })

# All unique stars
all_star_ids = set()
for stars in culture_stars.values():
    all_star_ids.update(stars)

stars_data = []
for sid in all_star_ids:
    if sid in star_lookup:
        s = star_lookup[sid]
        stars_data.append({
            "id":  sid,
            "ra":  s["ra"],
            "dec": s["dec"],
            "mag": s["mag"],
        })

# Build star -> list of constellations it appears in
star_coords = {s["id"]: (s["ra"], s["dec"]) for s in stars_data}

star_to_cons = {}
for culture, constellations in culture_constellations.items():
    for con in constellations:
        stars_in_con = set()
        for seg in con["segments"]:
            for i in range(len(seg["x"])):
                if seg["x"][i] is None:
                    continue
                # Match by coordinate with small tolerance
                for sid, (sra, sdec) in star_coords.items():
                    if abs(sra - seg["x"][i]) < 0.0001 and abs(sdec - seg["y"][i]) < 0.0001:
                        stars_in_con.add(sid)
                        break
        for sid in stars_in_con:
            if sid not in star_to_cons:
                star_to_cons[sid] = []
            star_to_cons[sid].append({
                "culture": culture,
                "english": con["english"],
                "native":  con["native"],
            })

star_map_data = {
    "stars":                stars_data,
    "culture_stars":        {c: list(s) for c, s in culture_stars.items()},
    "culture_constellations": culture_constellations,
    "star_to_cons":         star_to_cons,
}

with open("star_map_data.json", "w", encoding="utf-8") as f:
    json.dump(star_map_data, f)
print(f"  -> star_map_data.json written ({len(stars_data)} stars, {len(culture_stars)} cultures)")
