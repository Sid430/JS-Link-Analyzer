from flask import Flask, request, jsonify
import openai
import os
import sys

app = Flask(__name)

try:
    openai.api_key = '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'
except KeyError:
    sys.stderr.write("BAD")
    exit(1)

# Initialize an empty set to store unique companies
unique_companies = set()
non_unknown_links = []

@app.route('/process-links', methods=['POST'])
def process_links():
    # Receive data from the extension
    data = request.get_json()
    links = data.get('links')

    # Initialize an empty set to store unique companies
    unique_companies = set()
    non_unknown_links = []

    # Process links using the code you provided
    for link in links:
        link = link.strip()  # Remove leading and trailing whitespaces
        if link:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful link-analyzer who only responds with one word (do not add periods to the end of that word). Note: If you cannot determine or the link is unknown, do not return anything (just a blank). Never return Unknown or a similar version."},
                    {"role": "user", "content": f"What company is featured in: {link}"},
                ]
            )

            # Extract assistant's reply
            assistant_reply = response['choices'][0]['message']['content']

            # If the reply is not "unknown" or similar, add the link to the non_unknown_links list
            if assistant_reply not in ["unknown", "Unknown", "unknown.", "Unknown.", "blank", "Blank", "blank.", "Blank.", "undetermined", "Undetermined", "Unspecified", "Unspecified.", "unspecified", "unspecified.", "Impossible", "impossible", "Impossible.", "impossible."]:
                non_unknown_links.append(link)

            # Add the company to the set (set automatically handles duplicates)
            unique_companies.add(assistant_reply)

    # Convert the set to a list for writing to the output file
    unique_companies_list = list(unique_companies)

    # Remove entries with "unknown" or "Unknown"
    filtered_companies = [company for company in unique_companies_list if company.lower() not in ["unknown", "Unknown", "unknown.", "Unknown.", "blank", "Blank", "blank.", "Blank.", "undetermined", "Undetermined"]]

    # Write the results to the output file
    # Note: In this example, we don't write to a file, but you can modify it to save the results as needed
    return jsonify({'results': filtered_companies, 'non_unknown_links': non_unknown_links})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

