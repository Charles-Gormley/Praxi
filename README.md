# Praxi - The Notes to Textbook Converter

This project contains a Python script that converts a set of notes into a structured markdown textbook using the OpenAI GPT model. It processes input notes, generates detailed sections for each concept, and compiles them into a cohesive markdown document.

## Prerequisites

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/notes-to-textbook-converter.git
   cd notes-to-textbook-converter
   ```

2. Install the required packages:
   ```
   pip install openai python-dotenv
   ```

3. Create a `.env` file in the project root and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Usage

1. Open the `notes_to_textbook.py` file and modify the `example_notes` string in the `__main__` section with your own notes.

2. Run the script:
   ```
   python notes_to_textbook.py
   ```

3. The generated textbook will be saved as `generated_textbook.md` in the same directory.

## Customization

- You can modify the `Config` class in `notes_to_textbook.py` to change settings such as the OpenAI model, maximum retries, or output file name.
- To implement more sophisticated note processing, update the `ConceptProcessor.process_notes()` method.
- To change the structure of generated sections, modify the prompt in `TextbookGenerator.generate_section()`.

## Example

An example script `example_usage.py` is provided to demonstrate how to use the Notes to Textbook Converter in your own Python scripts.

To run the example, go into the src/examples folder & run
```
python example_1.py
```

This will generate a textbook based on the example notes provided in the script.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
