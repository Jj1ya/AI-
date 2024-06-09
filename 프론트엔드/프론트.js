// src/components/PostList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PostList = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    const fetchPosts = async () => {
      const response = await axios.get('/api/posts/');
      setPosts(response.data);
    };
    fetchPosts();
  }, []);

  return (
    <div>
      <h1>Post List</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h3>{post.title}</h3>
            <p>{post.content}</p>
            <p>Created at: {post.created_at}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default PostList;

// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PostList from './components/PostList';

const App = () => {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/" component={PostList} />
        </Switch>
      </div>
    </Router>
  );
};

export default App;
