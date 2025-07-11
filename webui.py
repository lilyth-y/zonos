print('webui.py 시작')
print('import gradio')
import gradio as gr
print('import os')
import os
print('import zonos.model')
from zonos.model import Zonos
print('import zonos.conditioning')
from zonos.conditioning import make_cond_dict
print('import torchaudio')
import torchaudio
print('import llm_openai')
from llm_openai import generate_dialogue_with_metadata
print('import gateway')
from gateway import decide_tts_params
print('import speaker_manager')
from speaker_manager import SpeakerManager
print('import torch')
import torch

print('Zonos 모델 로딩 시작')
model = Zonos.from_pretrained("Zyphra/Zonos-v0.1-transformer")
print('Zonos 모델 로딩 완료')
speaker_manager = SpeakerManager(model)

def get_speaker_names(speaker_infos):
    return [info['이름'] for info in speaker_infos if info['이름'] and info['샘플']]

# 1. LLM → 대화 스크립트 미리보기/수정용 DataFrame 생성
def generate_script(topic, speaker_infos, num_utterances, emotion_emphasis):
    # 화자 등록
    speaker_manager.speakers.clear()
    for info in speaker_infos:
        if info['이름'] and info['샘플']:
            speaker_manager.add_speaker(
                info['이름'], info['샘플'],
                {k: v for k, v in info.items() if k not in ['이름', '샘플']}
            )
    speaker_names = speaker_manager.list_speakers()
    if not speaker_names:
        return []
    speaker_profile = speaker_manager.get_profile(speaker_names[0])
    topic_prompt = topic
    if emotion_emphasis:
        topic_prompt += " 감정 변화가 확실하게 드러나게 해줘."
    dialogue = generate_dialogue_with_metadata(topic_prompt, speaker_profile, num_utterances, speaker_names)
    # DataFrame: [화자, 문장, 감정, 스타일, rate, pitch]
    rows = []
    for utt in dialogue:
        rows.append([
            utt.get('speaker', speaker_names[0]),
            utt.get('text', ''),
            utt.get('emotion', ''),
            utt.get('style', ''),
            utt.get('rate', ''),
            utt.get('pitch', '')
        ])
    return rows

# 2. 최종 대화 스크립트(수정본) → 음성 합성
def synthesize_from_script(speaker_infos, script_rows):
    # 화자 등록(재확인)
    speaker_manager.speakers.clear()
    for info in speaker_infos:
        if info['이름'] and info['샘플']:
            speaker_manager.add_speaker(
                info['이름'], info['샘플'],
                {k: v for k, v in info.items() if k not in ['이름', '샘플']}
            )
    speaker_names = speaker_manager.list_speakers()
    if not speaker_names:
        return [], None
    results = []
    wav_list = []
    for idx, row in enumerate(script_rows):
        speaker_name, text, emotion, style, rate, pitch = row
        if speaker_name not in speaker_names:
            speaker_name = speaker_names[0]
        speaker_emb = speaker_manager.get_embedding(speaker_name)
        # 파라미터 dict 생성
        params = {'emotion': emotion, 'style': style}
        if rate: params['rate'] = float(rate)
        if pitch: params['pitch'] = float(pitch)
        params = decide_tts_params(params)
        cond_dict = make_cond_dict(
            text=text,
            speaker=speaker_emb,
            language="ko",
            **params
        )
        conditioning = model.prepare_conditioning(cond_dict)
        codes = model.generate(conditioning)
        wavs = model.autoencoder.decode(codes).cpu()
        out_path = f"tmp_output_{idx+1}.wav"
        torchaudio.save(out_path, wavs[0], model.autoencoder.sampling_rate)
        results.append((text, speaker_name, emotion, out_path))
        wav_list.append(wavs[0])
    # 전체 합친 오디오 생성
    if wav_list:
        full_audio = torch.cat(wav_list, dim=-1)
        full_path = "full_dialogue.wav"
        torchaudio.save(full_path, full_audio, model.autoencoder.sampling_rate)
    else:
        full_path = None
    return results, full_path

# Gradio UI

def build_webui():
    print('build_webui 진입')
    with gr.Blocks() as demo:
        gr.Markdown("""
        # 🟢 대화 합성 에이전트 WebUI
        - 대화 주제, 화자 정보, 샘플, 감정 강조 등 입력 → 자연스러운 대화 음성 합성
        - 여러 화자 지원, 감정별 톤 변화 강조 가능
        - [TIP] 화자 이름을 반드시 입력하고, 각 화자별로 샘플을 업로드하세요.
        """)
        topic = gr.Textbox(label="대화 주제", value="오늘 날씨에 대해 대화해줘.")
        num_utterances = gr.Slider(1, 5, value=2, step=1, label="생성할 문장 수")
        emotion_emphasis = gr.Checkbox(label="감정 변화 강조", value=True)
        with gr.Column():
            speaker_infos = gr.Dataframe(
                headers=["이름", "나이", "성향", "배경", "샘플"],
                datatype=["str", "str", "str", "str", "file"],
                row_count=2,
                label="화자 정보 및 샘플 업로드 (여러 명 가능, 이름 필수)"
            )
        # 1단계: 대화 스크립트 생성 및 미리보기/수정
        script_df = gr.Dataframe(
            headers=["화자", "문장", "감정", "스타일", "rate", "pitch"],
            datatype=["str", "str", "str", "str", "number", "number"],
            row_count=5,
            label="대화 스크립트 미리보기/수정 (수정 후 아래에서 합성 실행)"
        )
        gen_btn = gr.Button("대화 스크립트 생성/갱신")
        gen_btn.click(
            fn=generate_script,
            inputs=[topic, speaker_infos, num_utterances, emotion_emphasis],
            outputs=script_df
        )
        # 2단계: 최종 스크립트로 음성 합성
        output = gr.Dataframe(
            headers=["문장", "화자", "감정", "음성"],
            datatype=["str", "str", "str", "audio"],
            label="합성 결과 (문장별)"
        )
        full_audio = gr.Audio(label="전체 대화 오디오 (합치기)")
        synth_btn = gr.Button("최종 스크립트로 음성 합성 실행")
        synth_btn.click(
            fn=synthesize_from_script,
            inputs=[speaker_infos, script_df],
            outputs=[output, full_audio]
        )
    return demo

if __name__ == "__main__":
    try:
        print('build_webui 호출')
        demo = build_webui()
        print('demo.launch() 호출')
        demo.launch(server_name="0.0.0.0", server_port=7860)
    except Exception as e:
        import traceback
        print("실행 중 오류 발생:", e)
        traceback.print_exc() 
