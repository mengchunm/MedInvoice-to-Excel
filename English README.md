# MedInvoice-to-Excel

English README | [Chinese Version](https://github.com/mengchunm/MedInvoice-to-Excel/blob/main/README.md)

MedBill2Excel is an automated tool that uses PaddleOCR to extract text from medical invoice images, then classifies the content intelligently via Ollama, and finally generates structured Excel spreadsheets.
It is suitable for hospitals, insurance companies, and finance departments that need to process large batches of medical receipts.

## Features

Automated OCR Recognition: High-accuracy text extraction from invoices using PaddleOCR.

Intelligent Classification: Content parsing and classification with Ollama models (Qwen2.5 recommended).

Excel Auto-Generation: Outputs structured spreadsheets for easy statistics and archiving.

Batch Processing: Supports processing multiple invoice files at once.

## Requirements

Operating System: Currently tested only on Windows (other platforms unverified).

Model Selection: Requires installation of Ollama and the Qwen2.5 model (avoid using deep-thinking models as they may slow down speed and reduce accuracy).

Dependencies: Make sure to install all dependencies listed in requirements.txt.

Image Quality: Clear, unobstructed scans or photos of invoices are recommended.

## Installation
1. Clone the repository
git clone https://github.com/yourusername/MedInvoice-to-Excel.git
cd MedInvoice-to-Excel

 2. Install dependencies
pip install -r requirements.txt

 3. Install Ollama (see official documentation)
 https://ollama.com/

 4. Pull the recommended model
ollama pull qwen2.5

 5. Run the program
python main.py --input ./invoices --output ./results

Example
Original Invoice Image	OCR Result (Excel)
	
License

This project is licensed under the MIT License.
