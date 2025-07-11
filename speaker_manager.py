import torchaudio
from zonos.model import Zonos
import torch

class SpeakerManager:
    """
    여러 화자 샘플을 관리하고, 각 화자별 임베딩을 추출/저장/제공하는 클래스
    - 화자 정보: 이름, 나이, 성향, 배경, 샘플 파일 경로 등
    - 임베딩: zonos 모델로 추출, dict로 관리
    """
    def __init__(self, model: Zonos):
        self.model = model
        self.speakers = {}  # {화자이름: {info..., 'embedding': ...}}

    def add_speaker(self, name, sample_path, profile=None):
        """
        화자 추가 및 임베딩 추출
        name: 화자 이름(고유)
        sample_path: 화자 음성 샘플 파일 경로
        profile: dict(나이, 성향, 배경 등)
        """
        wav, sr = torchaudio.load(sample_path)
        embedding = self.model.make_speaker_embedding(wav, sr)
        info = profile.copy() if profile else {}
        info.update({"name": name, "sample_path": sample_path, "embedding": embedding})
        self.speakers[name] = info

    def get_embedding(self, name):
        """화자 이름으로 임베딩 반환"""
        return self.speakers[name]["embedding"]

    def get_profile(self, name):
        """화자 이름으로 프로필 반환"""
        return self.speakers[name]

    def list_speakers(self):
        """등록된 화자 이름 리스트 반환"""
        return list(self.speakers.keys())

# 사용 예시
if __name__ == "__main__":
    model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer")
    sm = SpeakerManager(model)
    sm.add_speaker("민수", "assets/exampleaudio.mp3", {"나이": 25, "성향": "밝고 긍정적", "배경": "대학생"})
    print(sm.list_speakers())
    print(sm.get_profile("민수")) 