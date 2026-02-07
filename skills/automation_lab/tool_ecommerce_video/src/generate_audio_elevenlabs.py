import os
import sys
import requests
import json
import time
from datetime import datetime

# Configuration for auditing
USD_TO_BRL = 5.80  # Approximate exchange rate
PLAN_COST_USD = 22.00  # Creator plan cost

def get_subscription_info(api_key):
    url = "https://api.elevenlabs.io/v1/user/subscription"
    headers = {"xi-api-key": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Warning: Could not fetch subscription info: {e}")
    return None

def print_audit_report(start_info, end_info, text_length, duration_ms):
    if not start_info or not end_info:
        print("\n⚠️  Audit incomplete: Could not fetch subscription data.")
        return

    chars_start = start_info.get('character_count', 0)
    chars_end = end_info.get('character_count', 0)
    limit = start_info.get('character_limit', 1) # avoid div by zero
    
    chars_used = chars_end - chars_start
    # If chars_used is 0 or negative (due to reset or sync lag), use text length as fallback estimate
    if chars_used <= 0:
        chars_used = text_length
        note = "(Estimated from text length)"
    else:
        note = "(Verified from API)"

    # Cost calculation (Pro-rata based on monthly plan)
    # Creator plan: $22 for 100,000 chars (approx, actually 110k in some regions or older plans, let's use limit)
    cost_per_char_usd = PLAN_COST_USD / limit if limit > 0 else 0
    total_cost_usd = chars_used * cost_per_char_usd
    total_cost_brl = total_cost_usd * USD_TO_BRL

    print("\n" + "="*60)
    print(f"🧾 DETAILED AUDIT REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(f"⏱️  Operation Time: {duration_ms:.2f}ms")
    print(f"📝 Text Length: {text_length} chars")
    print("-" * 60)
    print(f"📊 CONSUMPTION {note}:")
    print(f"   • Previous Usage: {chars_start:,} / {limit:,}")
    print(f"   • Current Usage:  {chars_end:,} / {limit:,}")
    print(f"   • DELTA (Cost):   {chars_used} characters")
    print("-" * 60)
    print(f"💰 FINANCIAL IMPACT (Pro-rata Estimate):")
    print(f"   • Cost (USD):     ${total_cost_usd:.4f}")
    print(f"   • Cost (BRL):     R${total_cost_brl:.4f}")
    print(f"   • Plan Usage:     {(chars_used / limit * 100):.4f}% of monthly quota")
    print("-" * 60)
    print(f"📉 REMAINING:")
    print(f"   • Credits:        {limit - chars_end:,} characters")
    print(f"   • Potential:      ~{(limit - chars_end) / (chars_used if chars_used > 0 else 1):.0f} more videos like this")
    print("="*60 + "\n")

def generate_audio(text_file, output_file, voice_id="21m00Tcm4TlvDq8ikWAM"): # Rachel voice by default
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        print("Error: ELEVENLABS_API_KEY environment variable not set.")
        sys.exit(1)

    try:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: Text file not found at {text_file}")
        sys.exit(1)

    # AUDIT: Start Snapshot
    print("🔍 Fetching account status for audit...")
    start_info = get_subscription_info(api_key)
    start_time = time.time()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    print(f"🎙️  Generating audio for text ({len(text)} chars)...")
    response = requests.post(url, json=data, headers=headers)
    
    end_time = time.time()

    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'wb') as f:
            f.write(response.content)
        print(f"✅ Audio saved to {output_file}")
        
        # AUDIT: End Snapshot & Report
        # Small delay to ensure API updates stats (sometimes there's a slight lag)
        time.sleep(1) 
        end_info = get_subscription_info(api_key)
        
        print_audit_report(start_info, end_info, len(text), (end_time - start_time) * 1000)
        
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_audio_elevenlabs.py <text_file> <output_file> [voice_id]")
        sys.exit(1)
    
    text_file = sys.argv[1]
    output_file = sys.argv[2]
    voice_id = sys.argv[3] if len(sys.argv) > 3 else "21m00Tcm4TlvDq8ikWAM"
    
    generate_audio(text_file, output_file, voice_id)
