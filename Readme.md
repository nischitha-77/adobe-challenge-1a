# PDF Processing Tool

This repository contains a lightweight tool to extract structured information from PDF documents and convert it into JSON format. The tool is optimized to run inside a Docker container and complies with typical performance and system constraints.

## Features

* Parses PDFs to extract the document title and main headings
* Supports detection of hierarchical structure using font size and formatting patterns
* Outputs results as structured JSON files
* Designed to run automatically on a batch of PDFs from a specified input directory

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/your-username/pdf-processing-tool.git
cd pdf-processing-tool
```

### Build the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-processor .
```

### Run the Processor

```bash
docker run --rm \
  -v $(pwd)/sample_dataset/pdfs:/app/input:ro \
  -v $(pwd)/sample_dataset/outputs:/app/output \
  --network none \
  pdf-processor
```

## Project Structure

```
.
├── sample_dataset/
│   ├── pdfs/                   # Input PDF files
│   ├── outputs/                # Output JSON files
│   └── schema/                
│       └── output_schema.json # Output format definition
├── process_pdfs.py            # PDF processing script
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker setup
└── README.md                  # Project documentation
```

## Output Example

Each PDF file will generate a corresponding JSON file with the following format:

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Section Heading",
      "page": 2
    }
  ]
}
```

## Requirements

* Python 3.10+
* pdfminer.six

To install dependencies manually:

```bash
pip install -r requirements.txt
```




