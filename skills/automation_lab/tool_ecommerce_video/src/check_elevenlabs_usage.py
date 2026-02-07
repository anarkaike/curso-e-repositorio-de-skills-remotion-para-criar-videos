import os
import requests
import sys

def get_usage():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        # Try to load from absolute path
        env_path = "/Users/junio/Documents/PROJETOS/videos-programaticos/.env"
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r') as f:
                    for line in f:
                        if line.startswith('ELEVENLABS_API_KEY='):
                            api_key = line.strip().split('=', 1)[1]
                            break
            except:
                pass
            
    if not api_key:
        print("Error: ELEVENLABS_API_KEY not found.")
        return

    url = "https://api.elevenlabs.io/v1/user/subscription"
    headers = {
        "xi-api-key": api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            character_count = data.get('character_count', 0)
            character_limit = data.get('character_limit', 0)
            tier = data.get('tier', 'unknown')
            next_reset = data.get('next_character_count_reset_unix', 0)
            
            # Exchange rate estimate (USD to BRL)
            usd_to_brl = 5.80 
            
            print(f"--- ElevenLabs Usage ---")
            print(f"Plan: {tier}")
            print(f"Used: {character_count} characters")
            print(f"Limit: {character_limit} characters")
            
            remaining = character_limit - character_count
            print(f"Remaining: {remaining} characters")
            
            # Cost estimation logic (simplified)
            # This is tricky without knowing exact billing history, but we can estimate value.
            # Standard overage is approx $0.30 per 1000 characters on paid plans.
            # But usually 'usage' is within the monthly quota which is prepaid.
            
            print(f"\n--- Cost Estimation (Approximate) ---")
            print("Note: This is based on standard pay-as-you-go rates if you were to pay for this usage separately.")
            print("If this usage is within your monthly plan, you have already paid for it via subscription.")
            
            # Estimate value of used characters based on overage rate ($0.30/1k chars is common for Enterprise/high tier, 
            # but let's use a generic $0.30/1k for 'value' estimation or just $0.00 for included)
            
            # Better approach: Just show the usage. The user asked "how much I spent".
            # If it's free tier, spent is 0.
            # If it's paid, it's the subscription price.
            
            print(f"Usage percentage: {(character_count / character_limit * 100):.1f}%")
            
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_usage()
