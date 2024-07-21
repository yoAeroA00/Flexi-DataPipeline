# Flexi-DataPipeline

## Introduction

Welcome to the **FlexibleDataPipeline_OCR-LLM-MongoDB** project! This repository hosts a robust and adaptable data pipeline designed to convert images and PDFs, into a defined JSON schema. Leveraging the power of Azure OCR and Azure AI (ChatGPT), this pipeline efficiently processes diverse image types, transforming them into structured data stored in MongoDB. The flexibility of the code allows easy adaptation to different input formats and schemas, making it a versatile solution for various data processing needs.

## Features

- **Azure OCR Integration**: Utilize Azure's Optical Character Recognition (OCR) capabilities to accurately extract text from images and PDFs.
- **Azure AI (ChatGPT) Integration**: Process extracted text using Azure AI (ChatGPT) to ensure accurate and context-aware data transformation.
- **MongoDB Storage**: Store the structured data in MongoDB, a NoSQL database known for its scalability and flexibility.
- **Customizable JSON Schema**: Easily adapt the output JSON schema to fit your specific requirements.
- **Support for Various Input Formats**: Handle a wide range of image and PDF formats, ensuring broad applicability.

## Installation

To get started with the FlexibleDataPipeline, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yoAeroA00/Flexi-DataPipeline.git
    cd FlexibleDataPipeline_OCR-LLM-MongoDB
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set up Azure OCR and Azure AI (ChatGPT)**:
    - Ensure you have an Azure account and the necessary API keys.
    - Update the `.env` file with your Azure OCR and Azure AI credentials.

4. **Configure MongoDB**:
    - Install MongoDB and start the MongoDB server.
    - Update the `.env` file with your MongoDB connection details.

## Usage

1. **Prepare your input files**:
    - Place your images and PDFs in the `input` directory.

2. **Run the pipeline**:
    ```bash
    python main.py
    ```

3. **Check the output**:
    - The processed data will be stored in MongoDB as per the defined JSON schema.

## Configuration

The pipeline can be customized through various files and directories:

- **Azure OCR and Azure AI (ChatGPT)**: Configure the API keys and endpoints in the `.env` file.
- **MongoDB Configuration**: Update MongoDB connection details in the `.env` file. You should specify the MongoDB connection string and database settings in the environment variables, which the application will read to connect to MongoDB.
- **LLM Prompts and JSON Schema's**: Customize or update the LLM prompts, including the JSON schema definitions, by modifying files located in the `app/core/config/prompts/` directory. This directory contains JSON files that define the prompts used by the Azure AI (ChatGPT) integration, and the schema is embedded within these prompt files.

Make sure to check these configuration files and directories to tailor the pipeline to your specific requirements.

## Contributing

We welcome contributions to enhance the FlexibleDataPipeline. To contribute:

1. Fork the repository.
2. Create a new branch.
    ```bash
    git checkout -b feature-new-feature
    ```
3. Make your changes and commit them.
    ```bash
    git commit -m "Add new feature"
    ```
4. Push to the branch.
    ```bash
    git push origin feature-new-feature
    ```
5. Create a pull request.

## License

This project is licensed under the GNU Affero General Public License (AGPL). See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or support, please open an issue or contact the repository owner.
