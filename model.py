import torch
import numpy as np
from argparse import ArgumentParser
from tokenizers import SentencePieceBPETokenizer
from transformers import GPT2LMHeadModel, GPT2Config

parser = ArgumentParser()
parser.add_argument("-m", "--model-path", type=str, required=True)
parser.add_argument("-o", "--output-path", type=str, required=True)
parser.add_argument("-b", "--num-beams", type=int, default=5)

# 모델 경로 위치 잡기
model = GPT2LMHeadModel.from_pretrained("sangdal/ChatBot")
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = model.to(device)

# tokenizer폴더 경로위치 잡기
tokenizer = SentencePieceBPETokenizer.from_file(
    vocab_filename="./tokenizer/vocab.json", merges_filename="./tokenizer/merges.txt", add_prefix_space=False
)


# 경량화 기법을 적용한 생성 함수
def generate_question(context, num_beams=3):
    global model, tokenizer

    torch.autograd.set_grad_enabled(False)

    example = {"context": context, "question": "", "answer": ""}

    inputs = tokenizer.encode(example["context"])
    input_ids = torch.tensor(inputs.ids, dtype=torch.long).unsqueeze(0).to(device)

    model.eval()

    generated_results = []

    origin_seq_len = input_ids.size(-1)

    decoded_sequences = model.generate(
        input_ids=input_ids,
        max_length=origin_seq_len + 150,  # 질문의 최대길이
        min_length=origin_seq_len + 5,  # 질문의 최소길이
        pad_token_id=0,
        bos_token_id=1,
        eos_token_id=2,
        num_beams=num_beams,
        repetition_penalty=1.3,
        no_repeat_ngram_size=3,
        num_return_sequences=1,
    )

    for decoded_tokens in decoded_sequences.tolist():
        decoded_question_text = tokenizer.decode(decoded_tokens[origin_seq_len:])
        decoded_question_text = decoded_question_text.split("</s>")[0].replace("<s>", "")
        decoded_question_text = decoded_question_text.split("질문:")[-1]
        generated_results.append(decoded_question_text)

    return generated_results
