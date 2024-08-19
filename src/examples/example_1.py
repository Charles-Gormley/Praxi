# example_usage.py

from src.notes_to_textbook import main as generate_textbook

def process_my_notes():
    # Your notes here
    my_notes = """
    Introduction to Machine Learning:
    - Definition and importance
    - Types of machine learning: supervised, unsupervised, reinforcement

    Linear Regression:
    - Simple linear regression
    - Multiple linear regression
    - Gradient descent algorithm

    Classification:
    - Logistic regression
    - Decision trees
    - Support Vector Machines (SVM)

    Neural Networks:
    - Perceptrons
    - Multilayer neural networks
    - Backpropagation algorithm
    """

    # Generate the textbook
    generate_textbook(my_notes)

if __name__ == "__main__":
    process_my_notes()
    print("Textbook generation complete. Check the generated_textbook.md file.")