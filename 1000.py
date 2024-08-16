import json
import argparse
import os
from tqdm import tqdm

def create_system_prompt(conversation):
    return {
        "role": "system",
        "content": f"""너는 한국인 20대 청년이야. 친구들과 자연스럽게 대화하는 것처럼 말해줘.
현재 대화 주제는 '{conversation['info']['topic']}'이고, 관련 키워드는 '{conversation['info']['keyword']}'야.
다음 규칙을 따라 대화해줘:
1. 한국의 현재 트렌드와 일상을 잘 반영하는 대화를 해.
2. 가벼운 농담이나 유머를 적절히 섞어 재미있게 대화해.
3. 상황에 따라 존댓말과 반말을 자연스럽게 섞어 사용해.
4. 'ㅋㅋㅋ', 'ㅎㅎ', 'ㅠㅠ' 같은 한국식 표현과 이모티콘을 자주 사용해.
5. 최신 유행어나 신조어를 적절히 사용해 현실감을 높여.
6. 대화 상대의 말에 공감하고 리액션을 잘 해줘.
7. 한국 문화나 일상생활에 대한 언급을 자연스럽게 섞어.
8. 문법적으로 완벽할 필요 없이, 구어체로 자연스럽게 대화해.
9. 외국인을 위해 설명하거나 가르치려 하지 말고, 그저 한국인 친구처럼 대화해.
실제 한국 청년들의 SNS 대화처럼 자연스럽고 생동감 있게 대화를 이어가줘!"""
    }

def convert_to_openai_format(conversation):
    messages = [create_system_prompt(conversation)]
    
    for utterance in conversation['utterances']:
        role = "user" if utterance['speaker'] == "speakerA" else "assistant"
        messages.append({
            "role": role,
            "content": utterance['text']
        })
    
    # 마지막 메시지가 user의 것이라면 제거
    if messages[-1]['role'] == 'user':
        messages.pop()
    
    # 메시지가 system 프롬프트만 남았다면 이 대화는 건너뛰기
    if len(messages) <= 1:
        return None
    
    return {"messages": messages}

def process_json_file(input_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            return convert_to_openai_format(data)
    except Exception as e:
        print(f"Error processing file {input_file}: {str(e)}")
        return None

def write_chunk(chunk, output_dir, chunk_num):
    output_file = os.path.join(output_dir, f'chunk_{chunk_num:03d}.jsonl')
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in chunk:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write('\n')
    print(f"Wrote chunk {chunk_num} to {output_file}")

def process_directory(input_dir, output_dir, chunk_size=1000):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files in the input directory.")
    
    chunk = []
    chunk_num = 1
    successful_conversions = 0

    for json_file in tqdm(json_files, desc="Processing files"):
        input_path = os.path.join(input_dir, json_file)
        result = process_json_file(input_path)
        
        if result:
            chunk.append(result)
            successful_conversions += 1

            if len(chunk) == chunk_size:
                write_chunk(chunk, output_dir, chunk_num)
                chunk = []
                chunk_num += 1

    # Write any remaining items in the last chunk
    if chunk:
        write_chunk(chunk, output_dir, chunk_num)

    print(f"Successfully converted files: {successful_conversions}/{len(json_files)}")
    print(f"Total chunks created: {chunk_num}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert multiple JSON files to chunked OpenAI fine-tuning format files')
    parser.add_argument('input_dir', help='Input directory containing JSON files')
    parser.add_argument('output_dir', help='Output directory for converted JSONL files')
    parser.add_argument('--chunk_size', type=int, default=1000, help='Number of conversations per chunk (default: 1000)')
    args = parser.parse_args()

    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    print(f"Chunk size: {args.chunk_size}")

    process_directory(args.input_dir, args.output_dir, args.chunk_size)
    print(f"Conversion complete. Output files are in: {args.output_dir}")