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

@app.post("/test")
async def test(request: Request):
    print('test호출')
    split_text_list = []
    input_data = await request.json()
    print(input_data)
    # 텍스트만 파싱
    context = input_data["context"]

    # 텍스트 문단 나누기
    if len(context) > 30:
        text_list = context.split('.')
    else:
        text_list = list(context)
    # 함수에 적용
    for i in range(len(text_list)-1):
        result = generate_question(text_list[i])
        split_text_list.append(result)
        print(f'원본글: {text_list[i]}, 답변: {split_text_list[i]}')

    return split_text_list

    # return split_text_list

@app.post("/chat")
async def test(request: Request):
    input_data = await request.json()
    # 텍스트만 파싱
    context = input_data["context"]

    return generate_question(context)