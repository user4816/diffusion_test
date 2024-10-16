from diffusers import DiffusionPipeline
import torch
from PIL import Image

# Pretrained 모델 불러오기
pipeline = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
pipeline.to("cuda")

# 2. Gradient Checkpointing 사용 
if hasattr(pipeline, "enable_gradient_checkpointing"):
    pipeline.enable_gradient_checkpointing()

torch.cuda.empty_cache()

# 이미지를 로컬에서 불러오기
image_path = "input.png"  # 로컬에 저장된 이미지 경로
init_image = Image.open(image_path).convert("RGB")
init_image = init_image.resize((256, 256))  # 입력 이미지 크기 조정

# 변환할 텍스트 프롬프트 정의
prompt = "The input is an eye-diagram under signal integrity. Generate it with a height of 700mV and width of 140ps."

# 이미지를 모델에 입력하고 변환된 결과 받기
generated_image = pipeline(
    prompt=prompt,
    image=init_image,
    strength=0.75,  # 원본 이미지에 대한 영향력 (0~1 사이 값)
    guidance_scale=7.5,  # 텍스트 프롬프트 대한 가이드 스케일
).images[0]

# 출력 이미지 크기 조정
generated_image = generated_image.resize((256, 256))

# 결과 출력
generated_image.show()

# 결과 이미지 저장
generated_image.save("output.png")
