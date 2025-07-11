# 게이트웨이: LLM 메타데이터 → Zonos TTS 파라미터 변환 함수
# 감정별로 rate, pitch, quality 등 추가 조정(톤 변화 강조)

def decide_tts_params(utter):
    """
    utter: LLM에서 받은 문장 및 메타데이터 dict
      예시: {"text": "...", "emotion": "happy", "style": "fast", "rate": 1.2, "pitch": 1.1}
    반환: Zonos TTS에 넣을 파라미터 dict
    """
    # 기본값
    params = {
        "rate": 1.0,      # 말 빠르기
        "pitch": 1.0,     # 목소리 높이
        "emotion": "neutral", # 감정
        "quality": 1.0    # 음질
    }
    # 감정별 추가 조정(톤 변화 강조)
    emotion_map = {
        "happy":    {"emotion": "happy",    "rate": 1.15, "pitch": 1.1,  "quality": 1.1},
        "sad":      {"emotion": "sad",      "rate": 0.9,  "pitch": 0.9,  "quality": 1.0},
        "angry":    {"emotion": "angry",    "rate": 1.2,  "pitch": 1.05, "quality": 1.1},
        "fearful":  {"emotion": "fearful",  "rate": 1.05, "pitch": 1.2,  "quality": 1.0},
        "neutral":  {"emotion": "neutral",  "rate": 1.0,  "pitch": 1.0,  "quality": 1.0}
    }
    # LLM에서 감정이 명시된 경우 우선 적용
    emo = utter.get("emotion", "neutral").lower()
    if emo in emotion_map:
        params.update(emotion_map[emo])
    # LLM에서 스타일/속도/톤 등 추가 메타데이터가 있으면 덮어쓰기
    if "rate" in utter:
        params["rate"] = float(utter["rate"])
    if "pitch" in utter:
        params["pitch"] = float(utter["pitch"])
    if "quality" in utter:
        params["quality"] = float(utter["quality"])
    if "style" in utter:
        # 스타일 fast/slow/normal 등은 rate에 반영
        style_map = {"fast": 1.2, "slow": 0.8, "normal": 1.0}
        if utter["style"] in style_map:
            params["rate"] = style_map[utter["style"]]
    return params

# 사용 예시
if __name__ == "__main__":
    test_utter = {"text": "기분이 정말 좋아요!", "emotion": "happy", "style": "fast"}
    print(decide_tts_params(test_utter)) 