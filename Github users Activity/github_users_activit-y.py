import urllib.request
import urllib.parse
import json
import argparse


def get_respond(username):
    url = f"https://api.github.com/users/{username}/events"
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'My-GitHub-Activity-CLI')
    response = urllib.request.urlopen(req)
    raw_data = response.read()
    events_data = json.loads(raw_data.decode('utf-8'))
    return events_data


def despoise(events_data):
    print("OUTPUT:")
    for event in events_data[:3]:
        event_type = event.get('type')
        repo_name = event.get('repo', {}).get('name')
        payload = event.get('payload', {})

        if event_type == 'PushEvent':
            size = payload.get('size', 0)
            # 直接使用 Pushed 动词
            print(f"- Pushed {size} commit(s) to {repo_name}")

        elif event_type == 'ReleaseEvent':
            action = payload.get('action', 'released')
            tag_name = payload.get('release', {}).get('tag_name', 'unknown version')
            print(f"- {action.capitalize()} release {tag_name} in {repo_name}")

        elif event_type == 'CreateEvent':
            ref_type = payload.get('ref_type', 'resource')
            print(f"- Created a new {ref_type} in {repo_name}")

        elif event_type == 'DeleteEvent':
            ref_type = payload.get('ref_type', 'resource')
            print(f"- Deleted a {ref_type} in {repo_name}")

        else:
            print(f"- {event_type} in {repo_name}")






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("username")
    args = parser.parse_args()
    events_data = get_respond(args.username)
    despoise(events_data)
