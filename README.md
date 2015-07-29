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
