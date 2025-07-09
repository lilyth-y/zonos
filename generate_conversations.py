import json
import random
from datetime import datetime, timedelta

def generate_conversation_scenarios():
    """15일간의 아버지와 딸의 대화 시나리오를 생성합니다."""
    
    scenarios = []
    
    # 1일~5일: 일상적인 대화 (긍정적, 단조로운 감정)
    daily_conversations = [
        {
            "day": 1,
            "conversations": [
                {"speaker": "father", "text": "딸아, 오늘 날씨가 정말 좋네. 산책하러 갈까?", "emotion": "happy", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "좋아요 아빠! 공원에 가서 벚꽃도 보고 올까요?", "emotion": "excited", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "그래, 벚꽃이 예쁘게 피었을 거야. 카메라도 가져가자.", "emotion": "content", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "아빠 사진 찍는 거 정말 잘하시죠? 저도 배우고 싶어요.", "emotion": "admiring", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "그럼, 아빠가 천천히 가르쳐줄게. 오늘부터 시작해보자.", "emotion": "proud", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 2,
            "conversations": [
                {"speaker": "father", "text": "딸아, 아침에 뭐 먹을까? 토스트랑 계란 후라이 어때?", "emotion": "caring", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "좋아요! 아빠가 만드는 계란 후라이가 제일 맛있어요.", "emotion": "happy", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "그럼 아빠가 특별히 만들어줄게. 우유도 따뜻하게 데워줄까?", "emotion": "loving", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "네! 아빠가 항상 저를 챙겨주셔서 감사해요.", "emotion": "grateful", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 건강하게 자라주는 게 아빠의 가장 큰 기쁨이야.", "emotion": "proud", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 3,
            "conversations": [
                {"speaker": "father", "text": "오늘 학교에서 뭐 재미있는 일 있었어?", "emotion": "interested", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "친구랑 같이 과학 실험했어요! 정말 재미있었어요.", "emotion": "excited", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "그래? 어떤 실험을 했는데? 아빠한테도 설명해줘.", "emotion": "curious", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "물과 기름을 섞어서 색깔이 변하는 걸 봤어요. 마법 같았어요!", "emotion": "amazed", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "와, 정말 신기하겠다. 딸아가 과학에 관심이 많아서 아빠가 기뻐.", "emotion": "proud", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 4,
            "conversations": [
                {"speaker": "father", "text": "딸아, 주말에 영화 보러 갈까? 네가 좋아하는 애니메이션 나왔어.", "emotion": "excited", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "정말요? 어떤 영화인데요? 팝콘도 먹을 수 있어요?", "emotion": "excited", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "그래, 팝콘도 사주고 아이스크림도 사줄게. 딸아가 좋아할 거야.", "emotion": "loving", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠 최고! 저 영화 정말 보고 싶었어요. 감사해요!", "emotion": "grateful", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 행복해하는 모습을 보는 게 아빠의 가장 큰 기쁨이야.", "emotion": "content", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 5,
            "conversations": [
                {"speaker": "father", "text": "딸아, 오늘 숙제는 다 했어? 어려운 건 없었어?", "emotion": "concerned", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "네, 다 했어요! 수학 문제 하나가 어려웠는데 해결했어요.", "emotion": "proud", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "그래? 아빠가 도와줄까 했는데, 혼자 해결했구나. 대단해!", "emotion": "proud", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠가 항상 도와주시니까 자신감이 생겼어요. 감사해요!", "emotion": "grateful", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 이렇게 자라주니까 아빠가 정말 기뻐. 앞으로도 잘 해줘.", "emotion": "loving", "pace": "slow", "pitch": "low"}
            ]
        }
    ]
    
    # 6일~10일: 복잡한 대화 (감정 변동)
    complex_conversations = [
        {
            "day": 6,
            "conversations": [
                {"speaker": "father", "text": "딸아, 오늘 왜 그렇게 조용해? 무슨 일 있어?", "emotion": "concerned", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "친구랑 다퉜어요... 제가 실수했는데 사과했는데도 안 받아줘요.", "emotion": "sad", "pace": "slow", "pitch": "low"},
                {"speaker": "father", "text": "아, 그런 일이 있었구나. 아빠도 그런 적 있어. 시간이 지나면 괜찮아질 거야.", "emotion": "comforting", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "정말요? 아빠도 친구랑 다퉈본 적 있어요?", "emotion": "curious", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "그래, 아빠도 많이 다퉈봤어. 하지만 진짜 친구는 언젠가 이해해줄 거야.", "emotion": "wise", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 7,
            "conversations": [
                {"speaker": "father", "text": "딸아, 시험 성적이 나왔는데... 아빠가 좀 실망했어.", "emotion": "disappointed", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠... 저 정말 열심히 했는데... 다음엔 더 잘할게요.", "emotion": "guilty", "pace": "slow", "pitch": "low"},
                {"speaker": "father", "text": "아빠도 너무했나? 딸아가 열심히 한 건 아빠가 알아. 실수는 누구나 하는 거야.", "emotion": "regretful", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "정말요? 아빠가 저를 믿어주시는 거예요?", "emotion": "hopeful", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "당연하지. 딸아가 최선을 다했다면 그게 충분해. 아빠가 항상 응원할게.", "emotion": "supportive", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 8,
            "conversations": [
                {"speaker": "father", "text": "딸아, 아빠가 회사에서 일이 안 좋아서... 좀 힘들어.", "emotion": "tired", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠, 너무 무리하지 마세요. 저도 아빠 도와드릴 수 있어요.", "emotion": "caring", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 이렇게 걱정해주니까 아빠가 더 힘들어... 네가 걱정하지 말고.", "emotion": "conflicted", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠, 우리 가족이니까 같이 힘내요. 저도 아빠처럼 강해질게요.", "emotion": "determined", "pace": "normal", "pitch": "high"},
                {"speaker": "father", "text": "딸아... 아빠가 정말 고마워. 네가 있어서 아빠가 버틸 수 있어.", "emotion": "grateful", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 9,
            "conversations": [
                {"speaker": "father", "text": "딸아, 아빠가 오늘 화가 났어. 네가 약속을 안 지켰잖아.", "emotion": "angry", "pace": "fast", "pitch": "high"},
                {"speaker": "daughter", "text": "아빠, 죄송해요... 제가 깜빡했어요. 정말 미안해요.", "emotion": "apologetic", "pace": "slow", "pitch": "low"},
                {"speaker": "father", "text": "약속은 지켜야 하는 거야. 아빠가 실망했어.", "emotion": "disappointed", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "다음엔 절대 안 그럴게요. 아빠 용서해주세요.", "emotion": "pleading", "pace": "slow", "pitch": "low"},
                {"speaker": "father", "text": "알았어. 다음엔 꼭 지켜야 해. 아빠가 믿고 있어.", "emotion": "forgiving", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 10,
            "conversations": [
                {"speaker": "father", "text": "딸아, 아빠가 오늘 정말 기뻐! 회사에서 승진했어!", "emotion": "excited", "pace": "fast", "pitch": "high"},
                {"speaker": "daughter", "text": "정말요? 축하해요 아빠! 저도 너무 기뻐요!", "emotion": "excited", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 있어서 아빠가 더 열심히 할 수 있었어. 고마워!", "emotion": "grateful", "pace": "normal", "pitch": "normal"},
                {"speaker": "daughter", "text": "아빠가 항상 열심히 하시니까 당연한 결과예요! 저도 아빠처럼 되고 싶어요.", "emotion": "proud", "pace": "fast", "pitch": "high"},
                {"speaker": "father", "text": "딸아가 자랑스러워. 우리 가족이 함께라서 더 행복해.", "emotion": "happy", "pace": "slow", "pitch": "low"}
            ]
        }
    ]
    
    # 11일~15일: 극적인 감정 (치매, 감정조절 장애)
    dramatic_conversations = [
        {
            "day": 11,
            "conversations": [
                {"speaker": "father", "text": "딸아... 너 누구야? 내 딸이 맞아?", "emotion": "confused", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠, 저예요. 딸이에요. 기억 안 나세요?", "emotion": "worried", "pace": "slow", "pitch": "low"},
                {"speaker": "father", "text": "아... 딸아구나. 아빠가 잠깐 헷갈렸어. 미안해.", "emotion": "embarrassed", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "괜찮아요 아빠. 저희가 같이 기억해보아요.", "emotion": "patient", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "그래... 딸아가 있어서 다행이야. 아빠가 혼자면 어떡할지 몰라.", "emotion": "vulnerable", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 12,
            "conversations": [
                {"speaker": "father", "text": "딸아! 왜 네가 내 방에 있어? 나가! 당장 나가!", "emotion": "angry", "pace": "fast", "pitch": "high"},
                {"speaker": "daughter", "text": "아빠, 진정하세요. 저예요. 딸이에요.", "emotion": "calm", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "거짓말하지 마! 내 딸은 어디 갔어? 너는 누구야?", "emotion": "furious", "pace": "fast", "pitch": "high"},
                {"speaker": "daughter", "text": "아빠, 저희가 같이 사진도 찍었잖아요. 기억해보세요.", "emotion": "gentle", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "사진? 어디? 보여줘... 아... 딸아구나. 아빠가 또 헷갈렸어.", "emotion": "confused", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 13,
            "conversations": [
                {"speaker": "father", "text": "딸아... 아빠가 무서워. 어두워서 아무것도 안 보여.", "emotion": "fearful", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠, 괜찮아요. 저가 여기 있어요. 불도 켜져 있어요.", "emotion": "reassuring", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "정말? 불이 켜져 있어? 아빠가 안 보여... 눈이 나빠진 것 같아.", "emotion": "panicked", "pace": "fast", "pitch": "high"},
                {"speaker": "daughter", "text": "아빠, 천천히 심호흡하세요. 저가 아빠 손 잡아드릴게요.", "emotion": "comforting", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "딸아 손이 따뜻해... 아빠가 안심돼. 네가 있어서 다행이야.", "emotion": "relieved", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 14,
            "conversations": [
                {"speaker": "father", "text": "딸아... 아빠가 오늘 정말 슬퍼. 왜 이렇게 되는 걸까?", "emotion": "depressed", "pace": "very_slow", "pitch": "very_low"},
                {"speaker": "daughter", "text": "아빠, 울지 마세요. 저가 아빠 곁에 있어요. 항상 있어요.", "emotion": "loving", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "아빠가 네 짐이 되는 것 같아... 너무 미안해.", "emotion": "guilty", "pace": "slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠가 짐이 아니에요. 아빠는 제가 사랑하는 분이에요.", "emotion": "loving", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "딸아... 아빠가 고마워. 네가 있어서 아빠가 살 수 있어.", "emotion": "grateful", "pace": "slow", "pitch": "low"}
            ]
        },
        {
            "day": 15,
            "conversations": [
                {"speaker": "father", "text": "딸아... 아빠가 오늘 정말 행복해. 네가 있어서...", "emotion": "content", "pace": "very_slow", "pitch": "low"},
                {"speaker": "daughter", "text": "아빠, 저도 아빠가 있어서 행복해요. 항상 감사해요.", "emotion": "loving", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "아빠가 네 곁에서 늙어가는 게 정말 행복해...", "emotion": "peaceful", "pace": "very_slow", "pitch": "low"},
                {"speaker": "daughter", "text": "저도 아빠 곁에서 늙어가는 게 행복해요. 사랑해요 아빠.", "emotion": "loving", "pace": "slow", "pitch": "normal"},
                {"speaker": "father", "text": "딸아... 아빠도 사랑해... 정말 사랑해...", "emotion": "loving", "pace": "very_slow", "pitch": "very_low"}
            ]
        }
    ]
    
    scenarios = daily_conversations + complex_conversations + dramatic_conversations
    
    return scenarios

def save_scenarios_to_json(scenarios, filename="conversation_scenarios.json"):
    """시나리오를 JSON 파일로 저장합니다."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(scenarios, f, ensure_ascii=False, indent=2)
    print(f"시나리오가 {filename}에 저장되었습니다.")

if __name__ == "__main__":
    scenarios = generate_conversation_scenarios()
    save_scenarios_to_json(scenarios)
    
    print("15일간의 대화 시나리오가 생성되었습니다:")
    for day_scenario in scenarios:
        print(f"Day {day_scenario['day']}: {len(day_scenario['conversations'])}개의 대화")