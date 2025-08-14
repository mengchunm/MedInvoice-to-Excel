import os
import json
import pandas as pd
import requests
from paddleocr import PaddleOCR
from pathlib import Path


def call_ollama(text_data):
    """调用Ollama模型解析OCR文本数据"""
    prompt = f"""
请从以下医疗票据OCR识别的文本中提取信息，返回JSON格式：
{text_data}

请按照以下字段并返回JSON格式：
- 票据代码
- 票据号码
- 交款人
- 医保类型:门诊/门特/住院
- 开票日期
- 医院名称
- 个人自付

说明:
票据代码为8位纯数字
票据号码为10位纯数字
开票日期统一格式为:xxxx-xx-xx
有的字段可能残缺，例如"门特"仅显示为"特"

返回格式示例：
{{
    "票据代码": "51042213",
    "票据号码": "0091121245", 
    "交款人": "李嘉玲",
    "报销类型":"门特",
    "开票日期": "2025-02-06",
    "医院名称": "成都市中医结合医院",
    "个人自付": "1372.85"
}}

只返回JSON，不要其他文字说明。
"""

    try:
        response = requests.post(
            'http://localhost:11434/api/generate',
            json={
                'model': 'qwen2.5:7b',
                'prompt': prompt,
                'stream': False
            },
            timeout=120
        )

        if response.status_code == 200:
            result = response.json()
            return result.get('response', '')
        else:
            print(f"Ollama API错误: {response.status_code}")
            return None
    except Exception as e:
        print(f"调用Ollama失败: {e}")
        return None


def extract_json_from_response(response_text):
    """从响应中提取JSON数据"""
    try:
        # 尝试直接解析
        return json.loads(response_text)
    except:
        try:
            # 查找JSON部分
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response_text[start:end]
                return json.loads(json_str)
        except:
            pass
    return None


def batch_ocr_process():
    """批量处理OCR识别"""
    # 设置路径
    input_dir = Path("D:/Users/saevio/Desktop/test")
    output_dir = Path("D:/Users/saevio/Desktop/test/save")

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化OCR
    ocr = PaddleOCR(
        # text_detection_model_name="PP-OCRv5_server_det",
        # text_recognition_model_name="PP-OCRv5_server_rec",
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
    )

    # 支持的图片格式
    image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.tif'}

    # 存储所有提取的数据
    extracted_data = []

    # 遍历输入目录中的所有图片
    for img_path in input_dir.iterdir():
        if img_path.suffix.lower() in image_extensions:
            print(f"正在处理: {img_path.name}")

            try:
                # OCR识别
                result = ocr.predict(str(img_path))

                for i, res in enumerate(result):
                    res.print()

                    # 保存结果文件
                    base_name = img_path.stem
                    if len(result) > 1:
                        img_save_path = output_dir / f"{base_name}_page{i}.png"
                        json_save_path = output_dir / f"{base_name}_page{i}.json"
                    else:
                        img_save_path = output_dir / f"{base_name}.png"
                        json_save_path = output_dir / f"{base_name}.json"

                    res.save_to_img(str(img_save_path))
                    res.save_to_json(str(json_save_path))

                    # 读取JSON数据
                    with open(json_save_path, 'r', encoding='utf-8') as f:
                        json_data = json.load(f)

                    # 提取rec_texts数据
                    rec_texts = json_data.get('rec_texts', [])
                    text_data = '\n'.join(rec_texts)

                    print(f"OCR识别的文本数据：\n{text_data}\n")

                    # 调用Ollama模型解析
                    print("正在调用Ollama模型解析...")
                    ollama_response = call_ollama(text_data)

                    if ollama_response:
                        print(f"Ollama响应：{ollama_response}")

                        # 提取JSON数据
                        parsed_data = extract_json_from_response(ollama_response)

                        if parsed_data:
                            # 添加源文件信息
                            parsed_data['源文件'] = img_path.name
                            extracted_data.append(parsed_data)
                            print(f"成功提取数据：{parsed_data}")
                        else:
                            print("无法解析Ollama响应为JSON格式")
                            # 添加空白记录
                            empty_record = {
                                '源文件': img_path.name,
                                '票据代码': '',
                                '票据号码': '',
                                '交款人': '',
                                '开票日期': '',
                                '医院名称': '',
                                '个人自付': ''
                            }
                            extracted_data.append(empty_record)
                    else:
                        print("Ollama模型调用失败")
                        # 添加空白记录
                        empty_record = {
                            '源文件': img_path.name,
                            '票据代码': '',
                            '票据号码': '',
                            '交款人': '',
                            '开票日期': '',
                            '医院名称': '',
                            '个人自付': ''
                        }
                        extracted_data.append(empty_record)

            except Exception as e:
                print(f"处理 {img_path.name} 时出错: {e}")
                continue

    # 将数据写入Excel表格
    if extracted_data:
        df = pd.DataFrame(extracted_data)
        excel_path = output_dir / "医疗票据信息汇总.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        print(f"\n数据已保存到Excel文件: {excel_path}")
        print(f"共处理 {len(extracted_data)} 条记录")

        # 显示汇总信息
        print("\n提取的数据汇总：")
        print(df.to_string(index=False))
    else:
        print("没有成功提取到任何数据")


if __name__ == "__main__":
    # 运行批量处理
    batch_ocr_process()
