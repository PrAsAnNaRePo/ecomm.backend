import requests
import json

def test_api():
    base_url = "http://localhost:8000"
    
    def send_message(message, thread_id=None):
        url = f"{base_url}/chat"
        payload = {"message": message}
        if thread_id:
            payload["thread_id"] = thread_id
        
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            print(f"Assistant: {data['response']}")
            if data['sources']:
                print("Sources:")
                for source in data['sources']:
                    print(f"- {source['title']}: {source['url']}")
            print(f"Thread ID: {data['thread_id']}")
            return data['thread_id']
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    print("Starting a new conversation...")
    thread_id = send_message("What are the best selling products on Amazon?")
    
    if thread_id:
        print("\nContinuing the conversation...")
        send_message("Can you give me more details about electronics?", thread_id)
        
        print("\nAsking another follow-up question...")
        send_message("What about smartphones specifically?", thread_id)
    
    # Test with an invalid thread ID
    print("\nTesting with an invalid thread ID...")
    send_message("This should fail", "invalid_thread_id")

if __name__ == "__main__":
    test_api()