# MedInvoice-to-Excel
MedBill2Excel 是一个自动化工具，利用 PaddleOCR 从医疗发票图片中识别文字，并通过 Ollama 对内容进行智能分类，最终生成结构化的 Excel 表格，适用于医院、保险和财务等需要批量处理医疗票据的场景。 
MedBill2Excel is an automated tool that extracts text from medical invoices with PaddleOCR, classifies it via Ollama, and outputs structured Excel sheets—ideal for bulk processing in healthcare, insurance, and finance.
### 使用须知
需要在windows平台使用(其他平台没有测试过)
需要安装ollama及qwen2.5模型(此模型仅为目前推荐，不建议使用带有深度思考的模型)
安装requirement.txt的插件
