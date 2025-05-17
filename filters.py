def filter_profiles(profiles, headline_keywords=[], min_mutual=0):
    result = []
    for p in profiles:
        headline = p.get('headline', '').lower()
        # OR logic: if any keyword is found in the headline
        if any(kw.strip().lower() in headline for kw in headline_keywords if kw.strip()) and int(p['mutual_connections'].split()[0]) >= min_mutual:
            result.append(p)
    return result