from app.models.user import UserProfile
from app.models.gov_support import GovSupportProgram


WEIGHTS = {
    "region": 25,
    "industry": 25,
    "business_size": 20,
    "interests": 20,
    "status": 10,
}


def _score_region(profile: UserProfile, program: GovSupportProgram) -> float:
    if not profile.region or not program.region:
        return 0.5
    if program.region == "전국":
        return 0.8
    if profile.region == program.region:
        return 1.0
    return 0.0


def _score_industry(profile: UserProfile, program: GovSupportProgram) -> float:
    if not profile.industry or not program.industry:
        return 0.5
    profile_industries = set(i.strip() for i in profile.industry.split(","))
    program_industries = set(i.strip() for i in program.industry.split(","))
    if profile_industries & program_industries:
        return 1.0
    return 0.0


def _score_size(profile: UserProfile, program: GovSupportProgram) -> float:
    if not profile.business_size or not program.business_size:
        return 0.5
    if profile.business_size == program.business_size:
        return 1.0
    return 0.2


def _score_interests(profile: UserProfile, program: GovSupportProgram) -> float:
    if not profile.interests or not program.keywords:
        return 0.5
    user_interests = set(i.strip().lower() for i in profile.interests.split(","))
    program_keywords = set(k.strip().lower() for k in program.keywords.split(","))
    overlap = user_interests & program_keywords
    if not overlap:
        return 0.0
    return min(len(overlap) / max(len(user_interests), 1), 1.0)


def _score_status(program: GovSupportProgram) -> float:
    if program.status == "모집중":
        return 1.0
    if program.status == "상시":
        return 0.8
    return 0.0


def calculate_match_score(profile: UserProfile, program: GovSupportProgram) -> int:
    raw = (
        WEIGHTS["region"] * _score_region(profile, program)
        + WEIGHTS["industry"] * _score_industry(profile, program)
        + WEIGHTS["business_size"] * _score_size(profile, program)
        + WEIGHTS["interests"] * _score_interests(profile, program)
        + WEIGHTS["status"] * _score_status(program)
    )
    return min(int(raw), 100)


def calculate_matches(profile: UserProfile, programs: list) -> list:
    results = []
    for program in programs:
        score = calculate_match_score(profile, program)
        results.append({"program": program, "score": score})
    results.sort(key=lambda x: x["score"], reverse=True)
    return results
