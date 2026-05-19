def calculate_ats_score(
    resume_text,
    keywords
):

    matched_keywords = []

    for keyword in keywords:

        if keyword in resume_text:
            matched_keywords.append(keyword)

    keyword_score = int(
        (len(matched_keywords) / len(keywords)) * 70
    ) if len(keywords) > 0 else 0

    achievement_words = [
        "improved",
        "increased",
        "developed",
        "managed",
        "led",
        "%"
    ]

    achievement_score = 0

    for word in achievement_words:

        if word in resume_text:
            achievement_score += 5

    if achievement_score > 30:
        achievement_score = 30

    final_score = keyword_score + achievement_score

    missing_keywords = [
        keyword
        for keyword in keywords
        if keyword not in matched_keywords
    ]

    suggestions = []

    if len(missing_keywords) > 0:
        suggestions.append(
            "Add missing job keywords"
        )

    if achievement_score < 10:
        suggestions.append(
            "Add measurable achievements"
        )

    return {
        "score": final_score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }