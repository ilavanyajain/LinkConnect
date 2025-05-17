# filters.py

def filter_profiles(profiles, headline_keywords=[], min_mutual=0):
    result = []
    for p in profiles:
        if any(kw.lower() in p['headline'].lower() for kw in headline_keywords) and int(p['mutual_connections'].split()[0]) >= min_mutual:
            result.append(p)
    return result