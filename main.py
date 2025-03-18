#!/usr/bin/env python3

import json
import os
import argparse
import re
from groq import Groq


def find_versioned_file(version, file_type):
    """
    Dynamically finds a versioned file inside the given version directory.
    Example: If version='latest', looks for 'okw.schema_latest.json', 'prompt_latest.txt', etc.
    """
    base_dir = os.path.dirname(os.path.realpath(__file__))
    version_path = os.path.join(base_dir, "versions", version)

    if not os.path.exists(version_path):
        return None  # Version folder doesn't exist

    # Search for file ending with _{version}.json or _{version}.txt
    for file in os.listdir(version_path):
        if file.startswith(file_type) and file.endswith(f"_{version}.json") or file.endswith(f"_{version}.txt"):
            return os.path.join(version_path, file)

    return None  # No matching file found


def load_versioned_file(version, file_type):
    """
    Loads a JSON or text file from the appropriate version directory.
    Dynamically detects versioned filenames (e.g., okw.schema_latest.json, prompt_latest.txt).
    """
    file_path = find_versioned_file(version, file_type)

    if file_path is None:
        raise FileNotFoundError(f"Versioned file '{file_type}' not found in version '{version}'.")

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file) if file_path.endswith(".json") else file.read()


def parse_json_response(response):
    """
    Attempts to parse a string as JSON. Uses regex extraction if necessary.
    """
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                print("Failed to parse extracted JSON.")
        print("No JSON object found in the response.")
        return None


def generate_prompt(domain, scenario, product, schema, type_label, prompt_template):
    """
    Constructs a structured prompt for data generation based on a given schema.
    The template for the prompt is loaded dynamically from the versioned `prompt.txt` file.
    """
    return prompt_template.format(
        domain=domain,
        scenario=scenario,
        product=product,
        type_label=type_label,
        schema=json.dumps(schema, indent=2)
    ).strip()


def generate_data_for_product(client, domain, scenario, product, schemas, model, prompt_template):
    """
    Generates structured synthetic data for a given product using the Groq API.
    """
    data = {}
    for type_label in ["OKW", "OKH"]:
        chosen_schema = schemas[type_label]
        prompt = generate_prompt(domain, scenario, product, chosen_schema, type_label, prompt_template)
        print(f"Generating {type_label} data for '{product}' in domain '{domain}'...")

        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=model,
            temperature=0.3,
            max_tokens=4000,
            top_p=0.3
        )

        generated_json = parse_json_response(response.choices[0].message.content)
        if generated_json is None:
            print(f"Warning: Could not extract valid JSON for '{product}' ({type_label}). Using empty dict instead.")
            generated_json = {}

        data[type_label] = generated_json
    return data


def process_version(version, args):
    """
    Loads schemas and prompt from a specified version directory, generates data,
    and saves it inside the corresponding version folder.
    """
    try:
        # Load schema files for OKW and OKH dynamically
        schema_okw = load_versioned_file(version, "okw.schema")
        schema_okh = load_versioned_file(version, "okh.schema")
        prompt_template = load_versioned_file(version, "prompt")

        print(f"\nProcessing version: {version}")

        client = Groq(api_key=args.api_key)
        schemas = {"OKW": schema_okw, "OKH": schema_okh}

        # Display loaded files
        print(f"✅ Successfully loaded version {version} files.")

        # Get products list
        sample_products = args.products or ["Oatmeal cookie", "Pancake", "Chocolate Cake"]
        if args.count > len(sample_products):
            sample_products *= (args.count // len(sample_products)) + 1
        sample_products = sample_products[:args.count]

        all_generated_data = {}
        for product in sample_products:
            product_data = generate_data_for_product(client, args.domain, args.scenario, product, schemas, args.model, prompt_template)
            all_generated_data[product] = product_data

        # Save data in corresponding version folder
        output_path = os.path.join("versions", version, f"generated_data_{version}.json")
        with open(output_path, "w") as outfile:
            json.dump(all_generated_data, outfile, indent=2)

        print(f"✅ Data generation complete for version {version}. Data saved to {output_path}\n")

    except FileNotFoundError as e:
        print(f"⚠️ Skipping version {version}: {e}")
        available_files = os.listdir(os.path.join("versions", version))
        print(f"📂 Available files in 'versions/{version}/': {available_files}")


def main(args):
    """
    Main execution flow to handle different versions dynamically.
    """
    versions_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "versions")

    if args.version == "all":
        # Process all available versions
        available_versions = [d for d in os.listdir(versions_dir) if os.path.isdir(os.path.join(versions_dir, d))]
        for version in available_versions:
            process_version(version, args)
    else:
        process_version(args.version, args)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic supply chain resilience dataset (OKW & OKH) for multiple versions.")

    parser.add_argument("--version", type=str, default="latest",
                        help="Specify schema/prompt version (e.g., v1, v2, latest, or 'all' to process all versions).")
    parser.add_argument("--output", type=str, default="generated_data.json",
                        help="Output file path for the generated JSON data (per version).")
    parser.add_argument("--products", nargs="+",
                        help="List of product names to generate data for.")
    parser.add_argument("--count", type=int, default=3,
                        help="Number of products to generate.")
    parser.add_argument("--domain", type=str, default="cooking",
                        help="Domain context for the generated data.")
    parser.add_argument("--scenario", type=str, default="A chaotic environment where a baker wants to bake something",
                        help="Scenario describing environment or context.")
    parser.add_argument("--model", type=str, default="llama-3.3-70b-versatile",
                        help="Model name for Groq API completions.")
    parser.add_argument("--api_key", type=str, required=True,
                        help="API key for Groq.")

    args = parser.parse_args()
    main(args)
