# squad-api

#### Setup
1. Install Virtualbox -- https://www.virtualbox.org/wiki/Downloads
2. Install Vagrant -- http://www.vagrantup.com/downloads.html
3. Clone repository and provision:
```
$ git clone git@github.com:groupthinkk/squad-api.git
$ cd squad-api
$ vagrant up
```

The app will now be accessible at `localhost:9991`

#### Admin
Navigating to http://127.0.0.1:9991/admin/ will allow you to login to the admin interface. A superuser is already setup with the following credentials:
```
username: squad
password: squadgoals
```

##### Instagram Users
Once you're logged in, you'll be able to add Instagram users by username. This will automatically validate the user and pull in relevant information from the Instagram API. The user admin panel can be found at http://127.0.0.1:9991/admin/instagram/user/.

##### Instagram Posts
A user's posts can be pulled in using a background process by selecting the user and selecting the "Update user posts" action, then clicking "Go". Check out the posts coming in in realtime by navigating to http://127.0.0.1:9991/admin/instagram/post/.

#### API
The following API methods are currently available:
- `GET /api/v0/instagram/users` lists all Instagram users
- `GET /api/v0/instagram/posts` lists all Instagram posts
- `GET /api/v0/instagram/posts/random` retrieves a random post along with translated bucket estimates

The above views will allow you to the explore the API via the browser. To retrieve these endpoints as JSON, append `?format=json` as a query parameter. Here's a fully formed example:

```
http://127.0.0.1:9991/api/v0/instagram/posts/random?format=json
```

#### TODO
- ~~Setup API~~
- Implement basic normalization model in Python
