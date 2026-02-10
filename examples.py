"""
Example script demonstrating how to use the IBQ QR Code Generator
"""
import requests
import json


# API Base URL
BASE_URL = "http://localhost:8000/api/v1"


def example_1_generate_single_qr():
    """Example 1: Generate a single QR code"""
    print("Example 1: Generate a single QR code")
    print("-" * 50)
    
    payload = {
        "business_card": {
            "name": "John Doe",
            "phone": "+1-234-567-8900",
            "email": "john.doe@company.com",
            "company": "Tech Corp",
            "job_title": "Software Engineer",
            "website": "https://www.company.com",
            "address": "123 Main Street",
            "city": "New York",
            "state": "NY",
            "postal_code": "10001",
            "country": "USA"
        },
        "size": 10,
        "border": 4,
        "error_correction": "H",
        "foreground_color": "black",
        "background_color": "white",
        "output_format": "png",
        "include_logo": False
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: {result['message']}")
        print(f"   Filename: {result['filename']}")
        print(f"   Size: {result['file_size']} bytes")
        print(f"   Format: {result['format']}")
        
        # Download the file
        download_response = requests.get(f"{BASE_URL}/download/{result['filename']}")
        with open(f"example_{result['filename']}", "wb") as f:
            f.write(download_response.content)
        print(f"   Downloaded to: example_{result['filename']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()


def example_2_generate_colored_qr():
    """Example 2: Generate a colored QR code"""
    print("Example 2: Generate a colored QR code")
    print("-" * 50)
    
    payload = {
        "business_card": {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "phone": "+1-555-0100",
            "company": "Creative Agency"
        },
        "size": 12,
        "border": 2,
        "error_correction": "H",
        "foreground_color": "#4F46E5",  # Indigo
        "background_color": "#F3F4F6",  # Light gray
        "output_format": "png"
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: Generated colored QR code")
        print(f"   Filename: {result['filename']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()


def example_3_generate_svg():
    """Example 3: Generate SVG QR code"""
    print("Example 3: Generate SVG QR code")
    print("-" * 50)
    
    payload = {
        "business_card": {
            "name": "Bob Johnson",
            "email": "bob@startup.io",
            "company": "StartUp Inc"
        },
        "output_format": "svg"
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success: Generated SVG QR code")
        print(f"   Filename: {result['filename']}")
        print(f"   Format: {result['format']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()


def example_4_batch_generate():
    """Example 4: Batch generate QR codes"""
    print("Example 4: Batch generate QR codes")
    print("-" * 50)
    
    # Create a batch of business cards
    cards = [
        {
            "business_card": {
                "name": f"Employee {i}",
                "email": f"employee{i}@company.com",
                "phone": f"+1-555-010{i}",
                "company": "Big Corporation"
            },
            "output_format": "png"
        }
        for i in range(1, 6)
    ]
    
    response = requests.post(f"{BASE_URL}/batch-generate", json=cards)
    
    if response.status_code == 200:
        results = response.json()
        successful = sum(1 for r in results if r['success'])
        print(f"✅ Success: Generated {successful} out of {len(cards)} QR codes")
        for i, result in enumerate(results, 1):
            if result['success']:
                print(f"   {i}. {result['filename']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()


def example_5_health_check():
    """Example 5: Check API health"""
    print("Example 5: Check API health")
    print("-" * 50)
    
    response = requests.get(f"{BASE_URL}/health")
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ API Status: {result['status']}")
        print(f"   Service: {result['service']}")
    else:
        print(f"❌ Error: {response.status_code}")
    
    print()


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("IBQ QR Code Generator - Examples")
    print("=" * 50 + "\n")
    
    try:
        # Check if API is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("❌ Error: API is not responding")
            print("   Please start the server with: python -m uvicorn app.main:app --reload")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API")
        print("   Please start the server with: python -m uvicorn app.main:app --reload")
        exit(1)
    
    # Run examples
    example_5_health_check()
    example_1_generate_single_qr()
    example_2_generate_colored_qr()
    example_3_generate_svg()
    example_4_batch_generate()
    
    print("=" * 50)
    print("All examples completed!")
    print("=" * 50 + "\n")
