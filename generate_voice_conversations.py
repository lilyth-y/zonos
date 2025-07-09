import torch
import torchaudio
import json
import os
from pathlib import Path
from zonos.model import Zonos
from zonos.conditioning import make_cond_dict
from zonos.utils import DEFAULT_DEVICE as device

def load_conversation_scenarios(filename="conversation_scenarios.json"):
    """대화 시나리오를 로드합니다."""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_speaker_embeddings(model, father_audio_path, daughter_audio_path):
    """아버지와 딸의 스피커 임베딩을 생성합니다."""
    speakers = {}
    
    # 아버지 스피커 임베딩 생성
    if os.path.exists(father_audio_path):
        wav, sampling_rate = torchaudio.load(father_audio_path)
        speakers['father'] = model.make_speaker_embedding(wav, sampling_rate)
        print(f"아버지 스피커 임베딩 생성 완료")
    else:
        print(f"아버지 오디오 파일을 찾을 수 없습니다: {father_audio_path}")
        return None
    
    # 딸 스피커 임베딩 생성
    if os.path.exists(daughter_audio_path):
        wav, sampling_rate = torchaudio.load(daughter_audio_path)
        speakers['daughter'] = model.make_speaker_embedding(wav, sampling_rate)
        print(f"딸 스피커 임베딩 생성 완료")
    else:
        print(f"딸 오디오 파일을 찾을 수 없습니다: {daughter_audio_path}")
        return None
    
    return speakers

def get_emotion_vector(emotion):
    """감정에 따른 벡터를 반환합니다."""
    # 기본 벡터: [Happiness, Sadness, Disgust, Fear, Surprise, Anger, Other, Neutral]
    emotion_vectors = {
        "happy": [0.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1],
        "excited": [0.9, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
        "content": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "proud": [0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1],
        "caring": [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "loving": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "grateful": [0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1],
        "interested": [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3],
        "curious": [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "amazed": [0.3, 0.0, 0.0, 0.0, 0.7, 0.0, 0.0, 0.0],
        "admiring": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "concerned": [0.0, 0.3, 0.0, 0.2, 0.0, 0.0, 0.3, 0.2],
        "sad": [0.0, 0.8, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1],
        "comforting": [0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.3],
        "wise": [0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.4],
        "disappointed": [0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "guilty": [0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1],
        "regretful": [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "hopeful": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "supportive": [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "tired": [0.0, 0.4, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3],
        "conflicted": [0.0, 0.3, 0.0, 0.2, 0.0, 0.0, 0.3, 0.2],
        "determined": [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.2],
        "angry": [0.0, 0.0, 0.0, 0.0, 0.0, 0.8, 0.1, 0.1],
        "apologetic": [0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "pleading": [0.0, 0.5, 0.0, 0.2, 0.0, 0.0, 0.2, 0.1],
        "forgiving": [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3],
        "confused": [0.0, 0.2, 0.0, 0.4, 0.0, 0.0, 0.2, 0.2],
        "worried": [0.0, 0.3, 0.0, 0.4, 0.0, 0.0, 0.2, 0.1],
        "embarrassed": [0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "vulnerable": [0.0, 0.6, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "patient": [0.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.4],
        "furious": [0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.1],
        "gentle": [0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.3],
        "fearful": [0.0, 0.0, 0.0, 0.8, 0.0, 0.0, 0.1, 0.1],
        "reassuring": [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3],
        "panicked": [0.0, 0.0, 0.0, 0.9, 0.0, 0.0, 0.0, 0.1],
        "comforting": [0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.3],
        "relieved": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "depressed": [0.0, 0.9, 0.0, 0.0, 0.0, 0.0, 0.0, 0.1],
        "loving": [0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.2],
        "guilty": [0.0, 0.7, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1],
        "grateful": [0.7, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.1],
        "content": [0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.2],
        "peaceful": [0.4, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.3]
    }
    
    return emotion_vectors.get(emotion, [0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.4])

def get_pace_settings(pace):
    """말하기 속도 설정을 반환합니다."""
    pace_settings = {
        "very_slow": 8.0,
        "slow": 10.0,
        "normal": 15.0,
        "fast": 20.0,
        "very_fast": 25.0
    }
    return pace_settings.get(pace, 15.0)

def get_pitch_settings(pitch, emotion):
    """피치 설정을 반환합니다."""
    base_pitch_std = {
        "very_low": 15.0,
        "low": 25.0,
        "normal": 35.0,
        "high": 50.0,
        "very_high": 70.0
    }
    
    pitch_std = base_pitch_std.get(pitch, 35.0)
    
    # 감정에 따른 피치 조정
    if emotion in ["excited", "angry", "furious", "panicked"]:
        pitch_std *= 1.5
    elif emotion in ["sad", "depressed", "tired"]:
        pitch_std *= 0.7
    
    return pitch_std

def generate_conversation_audio(model, speakers, scenarios, output_dir="generated_conversations"):
    """대화 시나리오를 음성으로 생성합니다."""
    
    # 출력 디렉토리 생성
    Path(output_dir).mkdir(exist_ok=True)
    
    for day_scenario in scenarios:
        day = day_scenario['day']
        conversations = day_scenario['conversations']
        
        print(f"\n=== Day {day} 대화 생성 중 ===")
        
        # 일별 디렉토리 생성
        day_dir = Path(output_dir) / f"day_{day:02d}"
        day_dir.mkdir(exist_ok=True)
        
        for i, conv in enumerate(conversations):
            speaker_name = conv['speaker']
            text = conv['text']
            emotion = conv['emotion']
            pace = conv['pace']
            pitch = conv['pitch']
            
            print(f"  {speaker_name}: {text[:30]}...")
            
            # 스피커 임베딩 가져오기
            if speaker_name not in speakers:
                print(f"    경고: {speaker_name} 스피커를 찾을 수 없습니다.")
                continue
            
            speaker_embedding = speakers[speaker_name]
            
            # 감정 벡터 생성
            emotion_vector = get_emotion_vector(emotion)
            
            # 말하기 속도 설정
            speaking_rate = get_pace_settings(pace)
            
            # 피치 설정
            pitch_std = get_pitch_settings(pitch, emotion)
            
            # 조건 딕셔너리 생성
            cond_dict = make_cond_dict(
                text=text,
                speaker=speaker_embedding,
                language="ko-kr",  # 한국어
                emotion=emotion_vector,
                speaking_rate=speaking_rate,
                pitch_std=pitch_std,
                fmax=22050.0
            )
            
            # 조건 준비
            conditioning = model.prepare_conditioning(cond_dict)
            
            # 음성 생성
            torch.manual_seed(42 + day * 10 + i)  # 일관된 결과를 위한 시드 설정
            codes = model.generate(conditioning)
            
            # 오디오 디코딩
            wavs = model.autoencoder.decode(codes).cpu()
            
            # 파일 저장
            output_filename = day_dir / f"{speaker_name}_{i+1:02d}.wav"
            torchaudio.save(output_filename, wavs[0], model.autoencoder.sampling_rate)
            
            print(f"    저장됨: {output_filename}")
        
        print(f"Day {day} 완료!")

def main():
    """메인 함수"""
    print("Zonos 음성 합성 시작...")
    
    # 모델 로드
    print("모델 로딩 중...")
    model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer", device=device)
    print("모델 로딩 완료!")
    
    # 스피커 임베딩 생성
    print("스피커 임베딩 생성 중...")
    speakers = create_speaker_embeddings(
        model, 
        "assets/father_sample.wav",  # 아버지 샘플 오디오
        "assets/daughter_sample.wav"  # 딸 샘플 오디오
    )
    
    if speakers is None:
        print("스피커 임베딩 생성 실패. 샘플 오디오 파일이 필요합니다.")
        return
    
    # 대화 시나리오 로드
    print("대화 시나리오 로드 중...")
    scenarios = load_conversation_scenarios()
    
    # 음성 생성
    print("음성 합성 시작...")
    generate_conversation_audio(model, speakers, scenarios)
    
    print("\n모든 대화 음성 생성 완료!")

if __name__ == "__main__":
    main()