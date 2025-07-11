import torchaudio
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
import torch

# 1. LLM 연동 함수 (임시: 직접 대화 스크립트 반환)
def call_llm(topic):
    # 실제 LLM API 연동 대신, 예시 대화 스크립트 반환
    return [
        {"text": "안녕하세요! 오늘 날씨가 참 좋네요.", "emotion": "happy", "style": "fast"},
        {"text": "산책하기 딱 좋은 날씨죠?", "emotion": "happy", "style": "normal"}
    ]

# 2. 게이트웨이(파라미터 자동 결정)
def decide_tts_params(utter):
    params = {
        "rate": 1.0,
        "pitch": 1.0,
        "emotion": "neutral",
        "quality": 1.0
    }
    emotion_map = {"happy": "happy", "sad": "sad", "angry": "angry", "fear": "fearful", "neutral": "neutral"}
    style_map = {"fast": 1.2, "slow": 0.8, "normal": 1.0}
    if "emotion" in utter and utter["emotion"] in emotion_map:
        params["emotion"] = emotion_map[utter["emotion"]]
    if "style" in utter and utter["style"] in style_map:
        params["rate"] = style_map[utter["style"]]
    if "pitch" in utter:
        params["pitch"] = float(utter["pitch"])
    if "quality" in utter:
        params["quality"] = float(utter["quality"])
    return params

# 3. Zonos 모델 로딩 및 화자 임베딩 준비
def load_speaker_embedding(model, sample_path):
    wav, sr = torchaudio.load(sample_path)
    speaker = model.make_speaker_embedding(wav, sr)
    return speaker

# 4. 대화 스크립트 → 음성 합성 및 저장
def synthesize_dialogue(topic, speaker_sample_path, output_prefix="output_"):
    # (1) 대화 스크립트 생성
    dialogue = call_llm(topic)
    # (2) Zonos 모델 로딩
    model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer")
    # (3) 화자 임베딩 추출
    speaker = load_speaker_embedding(model, speaker_sample_path)
    # (4) 각 문장별 음성 합성 및 저장
    for idx, utter in enumerate(dialogue):
        params = decide_tts_params(utter)
        cond_dict = make_cond_dict(
            text=utter["text"],
            speaker=speaker,
            language="ko",
            **params
        )
        conditioning = model.prepare_conditioning(cond_dict)
        codes = model.generate(conditioning)
        wavs = model.autoencoder.decode(codes).cpu()
        out_path = f"{output_prefix}{idx+1}.wav"
        torchaudio.save(out_path, wavs[0], model.autoencoder.sampling_rate)
        print(f"[생성 완료] {out_path} : {utter['text']}")

if __name__ == "__main__":
    # 테스트용 화자 샘플 경로와 대화 주제 입력
    speaker_sample = "assets/exampleaudio.mp3"  # 실제 화자 샘플로 교체 가능
    topic = "오늘 날씨에 대해 대화해줘. 밝고 빠른 말투로."
    synthesize_dialogue(topic, speaker_sample) 