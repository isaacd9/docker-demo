## Docker Demo Repository for DS3 Talk
### Isaac Diamond

#### About
This is a repository containing the Python code and Dockerfile from the DS3 talk on January 27th, 2017. `analysis.py` implements a simple sentiment analysis REST API using `textblob` and `flask`.

API Spec:

```bash
POST /
```

```bash
{
  text: "Text you want to be analyzed"
}
```
Analyzes a block of text for sentiment and returns result

```bash
GET /list
```
List text currently in cache

```bash
GET /flush
```
Flushes cache

#### Prereqs

- You must have a computer capable of running Docker
- You must have internet access
- ['Docker']("https://docker.com") must be installed and running (Check that both the `Client` and `Server` are present when you run `docker version`)
- Helpful, but not necessary are `curl` and `jq` or some other tool that can make HTTP requests (Postman, HTTPie, etc...)

#### Building and Running

To build the Docker container: `make build`. This implicitly invokes: `docker build -t idiamond/docker-demo .`

To run the Docker container: `make run`. This implicitly invokes  ``docker run --rm -it -v `pwd`/_cache:/data/_cache -p 5000:5000 idiamond/docker-demo``.
If you prefer to run the container detached, try `docker run --rm -d -v `pwd`/_cache:/data/_cache -p 5000:5000 idiamond/docker-demo`. You can view the container state with `docker ps`. When you're done with the container, run `docker stop <hash>` where `hash` is the value listed under `CONTAINER ID`.

#### Testing

The container should now be running on port `:5000`

Try to send a request over the wire to it using `curl` (I've piped it to `jq` just for readability, but this isn't required):

```bash
curl -X POST -s -F "text=The so-called angry crowds in home districts of some Republicans are actually, in numerous cases, planned out by liberal activists. Sad" http://127.0.0.1:5000/ | jq
```

Notice that `cache_hit` should be missing in the return JSON. This means, this data has never been seen before & and the application has failed to retrieve it from cache.

If you try this again, the cache data should be there and `cache_hit` should be `true`.

You can list the cached text by running
```bash
curl -X GET -s http://127.0.0.1:5000/list | jq
```

and flush the cache with
```bash
curl -X GET -s http://127.0.0.1:5000/flush | jq
```

#### License

Copyright (C) 2017 Isaac Diamond

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
