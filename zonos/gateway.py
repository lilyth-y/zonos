"""
게이트웨이: LLM 대화 스크립트 및 사용자 입력을 zonos TTS 파라미터로 자동 변환
"""

from typing import List, Dict

# 감정/톤/속도 등 키워드 → zonos 파라미터 매핑 예시
default_emotion_map = {
    "기쁨": {"emotion": "happy", "tone": 1.2},
    "슬픔": {"emotion": "sad", "tone": 0.8},
    "분노": {"emotion": "angry", "tone": 1.5},
    # 필요에 따라 추가
}

def decide_tts_params(
    script: List[Dict],
    default_speaker: str = "default",
    emotion_map: Dict = None
) -> List[Dict]:
    """
    script: [{"text": "안녕하세요.", "speaker": "A", "emotion": "기쁨"}, ...]
    return: [{"text": ..., "speaker": ..., "emotion": ..., "tone": ..., ...}, ...]
    """
    if emotion_map is None:
        emotion_map = default_emotion_map
    results = []
    for line in script:
        params = {
            "text": line["text"],
            "speaker": line.get("speaker", default_speaker),
            "emotion": None,
            "tone": 1.0,
            "speed": 1.0,
        }
        # 감정 매핑
        if "emotion" in line and line["emotion"] in emotion_map:
            params.update(emotion_map[line["emotion"]])
        # 추가 파라미터 처리(속도 등)
        if "speed" in line:
            params["speed"] = line["speed"]
        results.append(params)
    return results

# 사용 예시
if __name__ == "__main__":
    sample_script = [
        {"text": "안녕하세요.", "speaker": "A", "emotion": "기쁨"},
        {"text": "무엇을 도와드릴까요?", "speaker": "B", "emotion": "기쁨"},
        {"text": "오늘은 기분이 좋아요.", "speaker": "A", "emotion": "기쁨"},
    ]
    tts_params = decide_tts_params(sample_script)
    for p in tts_params:
        print(p) 