# API Testing Examples

## Base URL
```
https://yourdomain.vercel.app
```

---

## Authentication Endpoints

### 1. Register New User
```bash
curl -X POST https://yourdomain.vercel.app/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (201 Created)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com"
}
```

---

### 2. Login User
```bash
curl -X POST https://yourdomain.vercel.app/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePassword123!"
  }'
```

**Response (200 OK)**:
```json
{
  "message": "Login successful",
  "token": "abc123defgh456ijkl789mnopqr",
  "username": "john_doe"
}
```

**Save the token!** Use it for authenticated requests.

---

### 3. Get User Profile
```bash
curl -X GET https://yourdomain.vercel.app/accounts/profile/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "username": "john_doe",
  "email": "john@example.com",
  "bio": null,
  "profile_picture": null,
  "following": []
}
```

---

### 4. List All Users
```bash
curl -X GET https://yourdomain.vercel.app/accounts/users/
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "followers_count": 5
  },
  {
    "id": 2,
    "username": "jane_smith",
    "email": "jane@example.com",
    "followers_count": 12
  }
]
```

---

## Post Management Endpoints

### 5. List All Posts
```bash
curl -X GET https://yourdomain.vercel.app/api/posts/
```

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "title": "My First Post",
    "content": "This is my first post on the social media API!",
    "author": {
      "id": 1,
      "username": "john_doe"
    },
    "created_at": "2025-12-12T10:30:00Z",
    "updated_at": "2025-12-12T10:30:00Z",
    "likes_count": 5,
    "comments_count": 2
  }
]
```

---

### 6. Create New Post
```bash
curl -X POST https://yourdomain.vercel.app/api/posts/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr" \
  -d '{
    "title": "My Amazing Post",
    "content": "This is the content of my amazing post. It can be quite long!"
  }'
```

**Response (201 Created)**:
```json
{
  "id": 2,
  "title": "My Amazing Post",
  "content": "This is the content of my amazing post. It can be quite long!",
  "author": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2025-12-12T10:35:00Z",
  "updated_at": "2025-12-12T10:35:00Z"
}
```

---

### 7. Get Single Post
```bash
curl -X GET https://yourdomain.vercel.app/api/posts/2/
```

**Response (200 OK)**:
```json
{
  "id": 2,
  "title": "My Amazing Post",
  "content": "This is the content of my amazing post. It can be quite long!",
  "author": {
    "id": 1,
    "username": "john_doe"
  },
  "created_at": "2025-12-12T10:35:00Z",
  "updated_at": "2025-12-12T10:35:00Z",
  "comments": [
    {
      "id": 1,
      "content": "Great post!",
      "author": "jane_smith",
      "created_at": "2025-12-12T10:40:00Z"
    }
  ],
  "likes_count": 3
}
```

---

### 8. Update Post
```bash
curl -X PUT https://yourdomain.vercel.app/api/posts/2/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr" \
  -d '{
    "title": "My Updated Post",
    "content": "Updated content here!"
  }'
```

**Response (200 OK)**:
```json
{
  "id": 2,
  "title": "My Updated Post",
  "content": "Updated content here!",
  "updated_at": "2025-12-12T10:45:00Z"
}
```

---

### 9. Delete Post
```bash
curl -X DELETE https://yourdomain.vercel.app/api/posts/2/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (204 No Content)**:
(No response body)

---

## Comment Endpoints

### 10. Add Comment to Post
```bash
curl -X POST https://yourdomain.vercel.app/api/posts/1/comments/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr" \
  -d '{
    "content": "This is an amazing post!"
  }'
```

**Response (201 Created)**:
```json
{
  "id": 5,
  "content": "This is an amazing post!",
  "author": {
    "id": 1,
    "username": "john_doe"
  },
  "post": 1,
  "created_at": "2025-12-12T10:50:00Z"
}
```

---

### 11. List Comments on Post
```bash
curl -X GET https://yourdomain.vercel.app/api/posts/1/comments/
```

**Response (200 OK)**:
```json
[
  {
    "id": 5,
    "content": "This is an amazing post!",
    "author": "john_doe",
    "created_at": "2025-12-12T10:50:00Z"
  },
  {
    "id": 6,
    "content": "I agree!",
    "author": "jane_smith",
    "created_at": "2025-12-12T10:52:00Z"
  }
]
```

---

### 12. Delete Comment
```bash
curl -X DELETE https://yourdomain.vercel.app/api/posts/1/comments/5/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (204 No Content)**:
(No response body)

---

## Like Endpoints

### 13. Like a Post
```bash
curl -X POST https://yourdomain.vercel.app/api/posts/1/like/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
{
  "message": "Post liked successfully"
}
```

---

### 14. Unlike a Post
```bash
curl -X POST https://yourdomain.vercel.app/api/posts/1/unlike/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
{
  "message": "Post unliked successfully"
}
```

---

## User Relationship Endpoints

### 15. Follow a User
```bash
curl -X POST https://yourdomain.vercel.app/accounts/users/2/follow/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
{
  "message": "You are now following jane_smith"
}
```

---

### 16. Unfollow a User
```bash
curl -X POST https://yourdomain.vercel.app/accounts/users/2/unfollow/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
{
  "message": "You have unfollowed jane_smith"
}
```

---

## Feed Endpoint

### 17. Get Personalized Feed
```bash
curl -X GET https://yourdomain.vercel.app/api/feed/ \
  -H "Authorization: Token abc123defgh456ijkl789mnopqr"
```

**Response (200 OK)**:
```json
[
  {
    "id": 3,
    "title": "Post from followed user",
    "content": "Content from someone you follow",
    "author": "jane_smith",
    "created_at": "2025-12-12T09:00:00Z",
    "likes_count": 10
  },
  {
    "id": 4,
    "title": "Another post",
    "content": "From another followed user",
    "author": "john_smith",
    "created_at": "2025-12-12T08:00:00Z",
    "likes_count": 7
  }
]
```

---

## Error Responses

### Missing Authentication
```bash
curl -X POST https://yourdomain.vercel.app/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test"}'
```

**Response (401 Unauthorized)**:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### Invalid Credentials
```bash
curl -X POST https://yourdomain.vercel.app/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "wrong@example.com",
    "password": "wrongpass"
  }'
```

**Response (400 Bad Request)**:
```json
{
  "non_field_errors": [
    "Unable to log in with provided credentials."
  ]
}
```

---

### Resource Not Found
```bash
curl -X GET https://yourdomain.vercel.app/api/posts/9999/
```

**Response (404 Not Found)**:
```json
{
  "detail": "Not found."
}
```

---

### Permission Denied (Trying to edit someone else's post)
```bash
curl -X PUT https://yourdomain.vercel.app/api/posts/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token different_user_token" \
  -d '{"title": "Hacked!"}'
```

**Response (403 Forbidden)**:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Testing with Postman or Insomnia

### Import Collection
You can use these example requests in Postman or Insomnia:

1. **Set base URL variable**: `{{base_url}}` = `https://yourdomain.vercel.app`
2. **Set auth token variable**: `{{token}}` = (value from login response)
3. Replace `/api/posts/1/` with `/api/posts/{{post_id}}/` etc.

### Environment Variables
```json
{
  "base_url": "https://yourdomain.vercel.app",
  "token": "abc123defgh456ijkl789mnopqr",
  "user_id": "1",
  "post_id": "1"
}
```

---

## Testing with JavaScript/Fetch API

### Register User
```javascript
const response = await fetch('https://yourdomain.vercel.app/accounts/register/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    username: 'john_doe',
    email: 'john@example.com',
    password: 'SecurePassword123!'
  })
});
const data = await response.json();
console.log(data);
```

### Login & Save Token
```javascript
const loginResponse = await fetch('https://yourdomain.vercel.app/accounts/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'john@example.com',
    password: 'SecurePassword123!'
  })
});
const loginData = await loginResponse.json();
const token = loginData.token;
localStorage.setItem('authToken', token);
```

### Make Authenticated Request
```javascript
const token = localStorage.getItem('authToken');
const response = await fetch('https://yourdomain.vercel.app/api/posts/', {
  method: 'GET',
  headers: {
    'Authorization': `Token ${token}`
  }
});
const posts = await response.json();
console.log(posts);
```

### Create Post
```javascript
const token = localStorage.getItem('authToken');
const response = await fetch('https://yourdomain.vercel.app/api/posts/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Token ${token}`
  },
  body: JSON.stringify({
    title: 'My First Post',
    content: 'This is awesome!'
  })
});
const newPost = await response.json();
console.log(newPost);
```

---

## Testing Checklist

After deployment, test these in order:

- [ ] GET `/api/posts/` → Should return 200
- [ ] POST `/accounts/register/` → Should return 201
- [ ] POST `/accounts/login/` → Should return token
- [ ] POST `/api/posts/` (with token) → Should create post
- [ ] GET `/api/posts/{id}/` → Should return post
- [ ] PUT `/api/posts/{id}/` (as author) → Should update
- [ ] DELETE `/api/posts/{id}/` (as author) → Should delete
- [ ] POST `/api/posts/{id}/like/` → Should like
- [ ] POST `/accounts/users/{id}/follow/` → Should follow
- [ ] GET `/api/feed/` (with token) → Should show feed

---

**All examples use real data structures that match your Django models!**
