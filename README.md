MedInvoice-to-Excel

English README | 中文说明

MedBill2Excel 是一个自动化工具，利用 PaddleOCR 从医疗发票图片中识别文字，并通过 Ollama 对内容进行智能分类，最终生成结构化的 Excel 表格。
适用于 医院、保险、财务 等需要批量处理医疗票据的场景。

功能特点

自动OCR识别：基于 PaddleOCR 高精度提取发票文字。

智能分类：通过 Ollama 模型（推荐使用 Qwen2.5）进行内容解析和分类。

Excel 自动生成：输出结构化表格，方便统计与归档。

批量处理：支持多个发票文件一次性处理。

使用须知

操作系统：目前仅在 Windows 测试通过（其他平台未验证）。

模型选择：需要安装 Ollama 及 Qwen2.5 模型（建议避免使用带深度思考的模型，可能会影响速度与准确性）。

依赖安装：确保已安装 requirements.txt 中的依赖。

图片质量：建议使用分辨率清晰、无遮挡的发票扫描件或照片。

安装步骤
# 1. 克隆仓库
git clone https://github.com/yourusername/MedInvoice-to-Excel.git
cd MedInvoice-to-Excel

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装 Ollama（参考官方文档）
# https://ollama.com/

# 4. 拉取推荐模型
ollama pull qwen2.5

# 5. 运行程序
python main.py --input ./invoices --output ./results

示例
原始发票图像	识别结果（Excel）

	
许可证

本项目遵循 MIT License。
