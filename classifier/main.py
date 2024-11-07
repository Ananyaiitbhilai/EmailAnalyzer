import json
import concurrent.futures
import argparse
from tqdm import tqdm
from email_classifier import EmailClassifier

def process_email(email_data, classifier):
    result = classifier.classify_email(email_data)
    
    # Combine input data with classification results
    output = {**email_data, **result}
    
    return output

def read_json(file_path):
    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            else:
                print("Error: Input file does not contain a JSON array.")
                return []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return []

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process emails and classify them.")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output JSON file")
    args = parser.parse_args()

    # Initialize classifier
    classifier = EmailClassifier()
    
    # Read input data
    print(f"Reading input file: {args.input_file}")
    emails = read_json(args.input_file)
    
    if not emails:
        print("No valid emails found in the input file. Please check the file format.")
        return

    print(f"Successfully read {len(emails)} emails from the input file.")
    
    # Process emails in parallel
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_email, email, classifier) for email in emails]
        
        # Process results as they complete
        for future in tqdm(concurrent.futures.as_completed(futures), total=len(emails), desc="Processing emails"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing email: {e}")
    
    # Write results to output file as a JSON array
    with open(args.output_file, 'w') as out_f:
        json.dump(results, out_f, indent=2)
    
    print(f"Processing complete. Results saved to {args.output_file}")

if __name__ == '__main__':
    main()

# Use: python main.py input_dataset.jsonl output_dataset.jsonl