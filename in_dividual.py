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
    
    return {"messages": messages}

def process_json_file(input_file, output_dir):
    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = json.load(infile)
            openai_format = convert_to_openai_format(data)
            
            output_filename = os.path.splitext(os.path.basename(input_file))[0] + '_converted.jsonl'
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as outfile:
                json.dump(openai_format, outfile, ensure_ascii=False)
                outfile.write('\n')
        return True
    except Exception as e:
        print(f"Error processing file {input_file}: {str(e)}")
        return False

def process_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]
    print(f"Found {len(json_files)} JSON files in the input directory.")
    
    successful_conversions = 0
    for json_file in tqdm(json_files, desc="Processing files"):
        input_path = os.path.join(input_dir, json_file)
        if process_json_file(input_path, output_dir):
            successful_conversions += 1

    print(f"Successfully converted files: {successful_conversions}/{len(json_files)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert multiple JSON files to individual OpenAI fine-tuning format files')
    parser.add_argument('input_dir', help='Input directory containing JSON files')
    parser.add_argument('output_dir', help='Output directory for converted JSONL files')
    args = parser.parse_args()

    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")

    process_directory(args.input_dir, args.output_dir)
    print(f"Conversion complete. Output directory: {args.output_dir}")