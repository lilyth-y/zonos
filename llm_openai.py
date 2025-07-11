import os
import openai

# OpenAI API 키는 환경변수(OPENAI_API_KEY)로 관리
openai.api_key = os.getenv("OPENAI_API_KEY")

# 멀티화자 대화 지원: 화자 이름 리스트를 받아 각 문장별 speaker 필드 포함

def generate_dialogue_with_metadata(
    topic: str,
    speaker_profile: dict,
    num_utterances: int = 2,
    speaker_names: list = None
):
    """
    topic: 대화 주제(예: '오늘 날씨에 대해 대화해줘')
    speaker_profile: 대표 화자 정보(예: {'이름': '민수', ...})
    num_utterances: 생성할 대화 문장 수
    speaker_names: 대화에 참여할 화자 이름 리스트(예: ['민수', '지수'])
    반환: [{speaker, text, emotion, style, rate, pitch, ...} ...] 형태의 리스트
    """
    # 화자 정보 프롬프트 구성
    speaker_desc = f"이름: {speaker_profile.get('이름', '화자')}, 나이: {speaker_profile.get('나이', '미상')}, " \
                  f"성향: {speaker_profile.get('성향', '미상')}, 배경: {speaker_profile.get('배경', '미상')}"
    # 멀티화자 안내
    if speaker_names and len(speaker_names) > 1:
        speaker_list_str = ', '.join(speaker_names)
        speaker_guide = f"아래 화자들({speaker_list_str})이 번갈아가며 대화하도록 해줘. 각 문장마다 누가 말하는지 'speaker' 필드에 화자 이름을 꼭 넣어줘."
    else:
        speaker_guide = ""
    # 프롬프트 예시 (감정별 톤 변화 강조, 멀티화자 안내 포함)
    prompt = f"""
너는 감정 표현이 매우 풍부한 AI 음성 합성 에이전트야.
아래 화자 정보를 참고해서, '{topic}'라는 주제로 자연스러운 대화 스크립트 {num_utterances}문장을 만들어줘.
{speaker_guide}
각 문장마다 speaker(화자 이름), 감정(emotion), 말투(style), 말의 빠르기(rate), 목소리의 높낮이(pitch) 등 메타데이터도 함께 JSON 형식으로 출력해.
특히 감정이 바뀔 때 목소리의 톤, 속도, 높낮이가 확연히 달라지도록 의도적으로 표현해줘.

[화자 정보]
{speaker_desc}

[출력 예시]
[
  {{"speaker": "민수", "text": "안녕하세요! 오늘 날씨가 참 좋네요.", "emotion": "happy", "style": "fast", "rate": 1.2, "pitch": 1.1}},
  {{"speaker": "지수", "text": "비가 오면 기분이 조금 가라앉아요.", "emotion": "sad", "style": "slow", "rate": 0.9, "pitch": 0.9}}
]

[응답]
"""
    # OpenAI GPT-3.5/4 API 호출
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.8,
        max_tokens=512,
        n=1,
    )
    # 응답에서 JSON 부분만 추출
    import re, json
    match = re.search(r'\[.*\]', response.choices[0].message['content'], re.DOTALL)
    if match:
        try:
            dialogue = json.loads(match.group(0))
            return dialogue
        except Exception as e:
            print("[파싱 오류]", e)
            print("원본 응답:", response.choices[0].message['content'])
            return []
    else:
        print("[응답 파싱 실패]", response.choices[0].message['content'])
        return []

# 사용 예시 (직접 실행 시)
if __name__ == "__main__":
    topic = "오늘 날씨에 대해 대화해줘. 감정 변화가 확실하게 드러나게 해줘."
    speaker_profile = {"이름": "민수", "나이": 25, "성향": "밝고 긍정적", "배경": "대학생"}
    speaker_names = ["민수", "지수"]
    dialogue = generate_dialogue_with_metadata(topic, speaker_profile, num_utterances=4, speaker_names=speaker_names)
    for utt in dialogue:
        print(utt) 