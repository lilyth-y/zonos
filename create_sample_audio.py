import torch
import torchaudio
import numpy as np
from pathlib import Path

def create_father_sample():
    """아버지 목소리 샘플을 생성합니다."""
    # 기존 샘플 오디오를 로드
    wav, sr = torchaudio.load("assets/exampleaudio.mp3")
    
    # 아버지 목소리 특성을 시뮬레이션 (더 낮은 피치, 느린 속도)
    # 피치를 낮추기 위해 리샘플링
    father_wav = torchaudio.functional.resample(wav, sr, int(sr * 0.8))
    
    # 볼륨을 약간 낮춤
    father_wav = father_wav * 0.9
    
    # 파일 저장
    torchaudio.save("assets/father_sample.wav", father_wav, sr)
    print("아버지 샘플 오디오 생성 완료: assets/father_sample.wav")

def create_daughter_sample():
    """딸 목소리 샘플을 생성합니다."""
    # 기존 샘플 오디오를 로드
    wav, sr = torchaudio.load("assets/exampleaudio.mp3")
    
    # 딸 목소리 특성을 시뮬레이션 (더 높은 피치, 빠른 속도)
    # 피치를 높이기 위해 리샘플링
    daughter_wav = torchaudio.functional.resample(wav, sr, int(sr * 1.2))
    
    # 볼륨을 약간 높임
    daughter_wav = daughter_wav * 1.1
    
    # 파일 저장
    torchaudio.save("assets/daughter_sample.wav", daughter_wav, sr)
    print("딸 샘플 오디오 생성 완료: assets/daughter_sample.wav")

def create_simple_samples():
    """간단한 샘플 오디오를 생성합니다."""
    sr = 22050
    duration = 3.0  # 3초
    t = torch.linspace(0, duration, int(sr * duration))
    
    # 아버지 목소리 (낮은 주파수)
    father_freq = 120  # 낮은 주파수
    father_wav = torch.sin(2 * np.pi * father_freq * t) * 0.3
    father_wav = father_wav.unsqueeze(0)  # 스테레오로 변환
    
    # 딸 목소리 (높은 주파수)
    daughter_freq = 220  # 높은 주파수
    daughter_wav = torch.sin(2 * np.pi * daughter_freq * t) * 0.3
    daughter_wav = daughter_wav.unsqueeze(0)  # 스테레오로 변환
    
    # 파일 저장
    torchaudio.save("assets/father_sample.wav", father_wav, sr)
    torchaudio.save("assets/daughter_sample.wav", daughter_wav, sr)
    
    print("간단한 샘플 오디오 생성 완료:")
    print("  - assets/father_sample.wav (120Hz)")
    print("  - assets/daughter_sample.wav (220Hz)")

def main():
    """메인 함수"""
    print("샘플 오디오 생성 시작...")
    
    # assets 디렉토리 확인
    Path("assets").mkdir(exist_ok=True)
    
    try:
        # 기존 오디오 파일이 있으면 그것을 사용
        if Path("assets/exampleaudio.mp3").exists():
            print("기존 샘플 오디오를 사용하여 변형 생성...")
            create_father_sample()
            create_daughter_sample()
        else:
            print("기존 샘플 오디오가 없어서 간단한 샘플 생성...")
            create_simple_samples()
    except Exception as e:
        print(f"오디오 변형 생성 실패: {e}")
        print("간단한 샘플 오디오 생성...")
        create_simple_samples()
    
    print("샘플 오디오 생성 완료!")

if __name__ == "__main__":
    main()