import os
import requests
from dotenv import load_dotenv


load_dotenv()


HASHNODE_API_KEY = ':sob:';


API_ENDPOINT = 'https://api.hashnode.com/'


create_draft_mutation = """
mutation CreateDraft($input: CreateDraftInput!) {
  createDraft(input: $input) {
    draft {
      id
      title
      content {
        markdown
      }
      publication {
        id
      }
      tags {
        name
      }
      coverImage {
        url
      }
    }
  }
}
"""


publish_post_mutation = """
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post {
      url
    }
  }
}
"""

def create_draft(title, content_markdown, publication_id, tags, cover_image_url):
    headers = {
        'Authorization': f'Bearer {HASHNODE_API_KEY}',
        'Content-Type': 'application/json'
    }

    variables = {
        "input": {
            "title": title,
            "contentMarkdown": content_markdown,
            "publicationId": publication_id,  
            "tags": tags,
            "coverImageOptions": {
                "type": "custom",
                "customImageURL": cover_image_url
            },
            "slug": title.lower().replace(" ", "-"),
            "originalArticleURL": "",
            "disableComments": False
        }
    }

    response = requests.post(API_ENDPOINT, json={'query': create_draft_mutation, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        draft_data = response.json()['data']['createDraft']['draft']
        publication_id = draft_data['publication']['id']  
        return draft_data, publication_id
    else:
        raise Exception(f"Failed to create draft. Status code: {response.status_code}. Error: {response.text}")

def publish_post(draft_id, publication_id):
    headers = {
        'Authorization': f'Bearer {HASHNODE_API_KEY}',
        'Content-Type': 'application/json'
    }

    variables = {
        "input": {
            "draftId": draft_id,
            "publicationId": publication_id,
            "title": "",  
            "contentMarkdown": "",  
        }
    }

    response = requests.post(API_ENDPOINT, json={'query': publish_post_mutation, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        return response.json()['data']['publishPost']['post']['url']
    else:
        raise Exception(f"Failed to publish post. Status code: {response.status_code}. Error: {response.text}")

if __name__ == '__main__':
    
    title = "Sample Draft Title"
    content_markdown = "# Sample Draft Content\n\nThis is a test draft."

    try:
        
        draft_data, publication_id = create_draft(title, content_markdown, "default", ["programming", "python"], "https://example.com/cover-image.jpg")
        draft_id = draft_data['id']
        print(f"Draft created with ID: {draft_id} under publication ID: {publication_id}")

        
        post_url = publish_post(draft_id, publication_id)
        print(f"Post published successfully. URL: {post_url}")

    except Exception as e:
        print(f"Error: {str(e)}")
