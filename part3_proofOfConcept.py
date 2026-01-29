import json
import random
import time

# Load configuration 
with open("config.json") as f:
    config = json.load(f)

# Mock LLM API
def mock_llm_call(provider, prompt):
    """
    Simulate a call to LLM API.
    Randomly fails 10% of the time to test failover.
    Returns response, tokens_used
    """
    if random.random() < 0.1: # simulate failure
    raise Exception(f"{provider} API error")
    # Simulate tokens used (input + output)
    tokens_used = len(prompt.split()) + random.randint(10, 50)
    # Simulate latency
    time.sleep(random.uniform(0.1, 0.5))
    return f"Mock response from {provider}", tokens_used

# Assign user to A/B variant
def select_ab_variant(user_id):
    if not config.get("ab_testing", {}).get("enabled", False):
        return None
    splits = config["ab_testing"]["splits"]
    rnd = random.uniform(0, 100)
    cumulative = 0
    for split in splits:
        cumulative += split["percentage"]
        if rnd <= cumulative:
            return split
    return splits[-1] # fallback

# LLM Client with failover
def call_llm(user_id, user_profile):
    variant = select_ab_variant(user_id)
    provider_name = variant["provider"]
    prompt_version = variant["prompt_version"]
    prompt_template = config["prompts"][prompt_version]["template"]
    prompt = prompt_template.replace("{{user_profile}}", user_profile)

    telemetry = {
        "user_id": user_id,
        "config_version": config["version"],
        "prompt_version": prompt_version,
        "provider_attempts": [],
        "success": False,
        "tokens": 0,
        "latency": 0,
        "error": None
    }

    providers_to_try = [provider_name]
    fallback = config["providers"].get(provider_name, {}).get("fallback")
    if fallback:
        providers_to_try.append(fallback)

    start_time = time.time()
    for p in providers_to_try:
        attempt = {"provider": p, "success": False, "error": None}
        try:
            response, tokens = mock_llm_call(p, prompt)
            attempt["success"] = True
            telemetry["success"] = True
            telemetry["tokens"] = tokens
            telemetry["latency"] = time.time() - start_time
            telemetry["provider_attempts"].append(attempt)
            return response, telemetry
        except Exception as e:
            attempt["error"] = str(e)
            telemetry["provider_attempts"].append(attempt)
            continue

    telemetry["success"] = False
    telemetry["latency"] = time.time() - start_time
    telemetry["error"] = "All providers failed"
    return None, telemetry

# Run simulation
if __name__ == "__main__":
    logs = []

    # simulate 10 users
    for i in range(10):
        user_id = f"user_{i}"
        user_profile = f"profile_data_{i}"
        response, telemetry = call_llm(user_id, user_profile)
        logs.append(telemetry)
        print(f"User {user_id} response: {response}")
        print("Telemetry:", telemetry)
        print("-" * 50)

    # optionally, save logs to file
    with open("telemetry_logs.json", "w") as f:
        json.dump(logs, f, indent=2)