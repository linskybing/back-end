"""
Test script for independent daily quest system
"""
import requests
import json

BASE_URL = "http://localhost:8080"

def test_daily_quests():
    user_id = "test_daily_quest_user"
    
    print("=" * 70)
    print("Testing Independent Daily Quest System")
    print("=" * 70)
    
    # 1. Create a test user
    print("\n1. Creating test user...")
    response = requests.post(f"{BASE_URL}/users/", json={
        "user_id": user_id,
        "pet_name": "任務測試雞"
    })
    print(f"   Status: {response.status_code}")
    
    # 2. Perform daily check (should auto-complete Quest 1)
    print("\n2. Performing daily check (auto-completes Quest 1: 每日登入)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/daily-check")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Already checked: {result.get('already_checked', False)}")
    
    # 3. Get daily quest status
    print("\n3. Getting daily quest status...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/daily-quests")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"\n   Daily Quests:")
        for quest in data.get("quests", []):
            print(f"   [{quest['id']}] {quest['title']}")
            print(f"       Description: {quest['description']}")
            print(f"       Progress: {quest['progress']}/{quest['goal']}")
            print(f"       Completed: {'✓' if quest['completed'] else '✗'}")
            print(f"       Rewards: STR+{quest['reward_strength']} STA+{quest['reward_stamina']} MOOD+{quest['reward_mood']}")
    
    # 4. Claim Quest 1 reward
    print("\n4. Claiming Quest 1 reward (每日登入)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/daily-quests/1/claim")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: {result.get('success', False)}")
        print(f"   Message: {result.get('message', 'N/A')}")
        if result.get('rewards'):
            rewards = result['rewards']
            print(f"   Received: STR+{rewards['strength']} STA+{rewards['stamina']} MOOD+{rewards['mood']}")
    
    # 5. Log short exercise (not enough for Quest 2)
    print("\n5. Logging short exercise (300 seconds, 2000 steps)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/exercise", json={
        "exercise_type": "Walking",
        "duration_seconds": 300,
        "volume": 1.0,
        "steps": 2000
    })
    print(f"   Status: {response.status_code}")
    
    # 6. Check quest status
    print("\n6. Checking quest status after short exercise...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/daily-quests")
    if response.status_code == 200:
        data = response.json()
        for quest in data.get("quests", []):
            if quest['id'] in [2, 3]:
                print(f"   [{quest['id']}] {quest['title']}: {quest['progress']}/{quest['goal']} {'✓' if quest['completed'] else '✗'}")
    
    # 7. Log more exercise (complete Quest 2)
    print("\n7. Logging more exercise to complete Quest 2 (400 seconds)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/exercise", json={
        "exercise_type": "Running",
        "duration_seconds": 400,
        "volume": 1.5,
        "steps": 1500
    })
    print(f"   Status: {response.status_code}")
    
    # 8. Check quest status
    print("\n8. Checking quest status after total 700 seconds...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/daily-quests")
    if response.status_code == 200:
        data = response.json()
        for quest in data.get("quests", []):
            if quest['id'] in [2, 3]:
                completed_str = "✓ COMPLETED!" if quest['completed'] else "✗"
                print(f"   [{quest['id']}] {quest['title']}: {quest['progress']}/{quest['goal']} {completed_str}")
    
    # 9. Claim Quest 2 reward
    print("\n9. Claiming Quest 2 reward (運動十分鐘)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/daily-quests/2/claim")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: {result.get('success', False)}")
        if result.get('rewards'):
            rewards = result['rewards']
            print(f"   Received: STR+{rewards['strength']} STA+{rewards['stamina']} MOOD+{rewards['mood']}")
    
    # 10. Log walking exercise to complete Quest 3
    print("\n10. Logging walking exercise to complete Quest 3 (2000 steps)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/exercise", json={
        "exercise_type": "Walking",
        "duration_seconds": 100,
        "volume": 1.0,
        "steps": 2000
    })
    print(f"   Status: {response.status_code}")
    
    # 11. Final quest status
    print("\n11. Final quest status check...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/daily-quests")
    if response.status_code == 200:
        data = response.json()
        print(f"\n   ========== Daily Quest Summary ==========")
        total_progress = 0
        for quest in data.get("quests", []):
            completed_str = "✓" if quest['completed'] else "✗"
            print(f"   [{completed_str}] {quest['title']}: {quest['progress']}/{quest['goal']}")
            if quest['completed']:
                total_progress += 1
        print(f"   =========================================")
        print(f"   Completed: {total_progress}/3 quests")
    
    # 12. Try to claim Quest 3 reward
    print("\n12. Claiming Quest 3 reward (走路5000步)...")
    response = requests.post(f"{BASE_URL}/users/{user_id}/daily-quests/3/claim")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Success: {result.get('success', False)}")
        if result.get('rewards'):
            rewards = result['rewards']
            print(f"   Received: STR+{rewards['strength']} STA+{rewards['stamina']} MOOD+{rewards['mood']}")
    elif response.status_code == 400:
        error = response.json()
        print(f"   Expected error: {error.get('detail', 'N/A')}")
    
    # 13. Get final pet status
    print("\n13. Getting final pet status...")
    response = requests.get(f"{BASE_URL}/users/{user_id}/pet")
    if response.status_code == 200:
        pet = response.json()
        print(f"   Pet Name: {pet.get('name')}")
        print(f"   Level: {pet.get('level')}")
        print(f"   Strength: {pet.get('strength')}")
        print(f"   Stamina: {pet.get('stamina')}")
        print(f"   Mood: {pet.get('mood')}")
        print(f"   Daily Exercise: {pet.get('daily_exercise_seconds')} seconds")
        print(f"   Daily Steps: {pet.get('daily_steps')} steps")
    
    print("\n" + "=" * 70)
    print("✅ Daily Quest System Test Completed!")
    print("=" * 70)

if __name__ == "__main__":
    test_daily_quests()
