import fastapi
from fastapi import Request
from model import generate_question
from fastapi.middleware.cors import CORSMiddleware

app = fastapi.FastAPI()

# 모든 주소(*)를 허용
origins = ["*"]

# CORSMiddleware를 등록합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 나창대 23.07.31
# @app.post("/test")
# async def test(request: Request):
#     split_text_list = []
#     input_data = await request.json()
#     print(input_data)

#     # 텍스트만 파싱
#     context = input_data["context"]

#     # 전체 내용을 한 번에 처리
#     result = generate_question(context)
#     split_text_list.append(result)

#     # 문장을 마침표를 기준으로 문단으로 나누기
#     sentences = context.split('.')
#     paragraphs = []
#     paragraph = ""
#     for sentence in sentences:
#         paragraph += sentence.strip() + ". "
#         if len(paragraph) > 30:
#             paragraphs.append(paragraph)
#             paragraph = ""

#     # 마지막 문단 처리
#     if paragraph.strip():
#         paragraphs.append(paragraph)

#     # 문단씩 짤라서 처리 range뒤에 숫자만 원하는 문단으로 짜르면 됩니다.
#     for i in range(0, len(paragraphs), 3):
#         combined_paragraph = ""
#         for j in range(3):
#             if i + j < len(paragraphs):
#                 combined_paragraph += paragraphs[i + j]
#         result = generate_question(combined_paragraph)
#         split_text_list.append(result)

#     return split_text_list

@app.post("/test")
async def test(request: Request):
    split_text_list = []
    input_data = await request.json()
    print(input_data)

    # 텍스트만 파싱
    context = input_data["context"]

    # 전체 내용을 한 번에 처리
    result = generate_question(context)
    split_text_list.append(result)

    # 문장을 마침표를 기준으로 문단으로 나누기
    sentences = context.split('.')
    paragraphs = []
    paragraph = ""
    for sentence in sentences:
        paragraph += sentence.strip() + ". "
        if len(paragraph) > 30:
            paragraphs.append(paragraph)
            paragraph = ""

    # 마지막 문단 처리
    if paragraph.strip():
        paragraphs.append(paragraph)

    # 문단씩 짤라서 처리 range뒤에 숫자만 원하는 문단으로 짜르면 됩니다.
    for i in range(0, len(paragraphs), 3):
        combined_paragraph = ""
        for j in range(3):
            if i + j < (len(paragraphs) - 1):
                combined_paragraph += paragraphs[i + j]
                print(f'모델 입력 전: {combined_paragraph}')
        result = generate_question(combined_paragraph)
        split_text_list.append(result)

    return split_text_list

@app.post("/chat")
async def test(request: Request):
    input_data = await request.json()
    # 텍스트만 파싱
    context = input_data["context"]

    return generate_question(context)