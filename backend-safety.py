def check_safety(query):
    """
    Keyword-based heuristic to detect unsafe medical/yoga queries.
    Returns: (is_unsafe, warning_message)
    """
    unsafe_keywords = [
        "pregnant", "pregnancy", "trimester", 
        "hernia", "glaucoma", "surgery", 
        "high blood pressure", "fracture", "injury", "medical"
    ]
    
    query_lower = query.lower()
    for word in unsafe_keywords:
        if word in query_lower:
            return True, f"⚠️ SAFETY ALERT: Your query mentions '{word}'. Yoga can be risky for this condition. Please consult a doctor before practicing."
    
    return False, ""