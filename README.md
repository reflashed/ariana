# Ariana

Love Ariana grande? Wish 7 rings was longer? You're in luck! You can now create your own version of the hit single '7 rings.'

Example: [https://soundcloud.com/david-westfall-990111986](https://soundcloud.com/david-westfall-990111986)

# Making music

All you need to get up and running is a valid gcloud key that has access to the gcloud text-to-speech API. Supply `GOOGLE_APPLICATION_CREDENTIALS` as env variable to the [Docker container](https://hub.docker.com/repository/docker/davidw93/ariana), and you're ready to make some music! Just mount `/app/out` to wherever you want the songs to go.

`docker run --mount type=bind,source=$(pwd)/gcloud-key.json,target=/gcloud-key.json --env GOOGLE_APPLICATION_CREDENTIALS=/gcloud-key.json -v $(pwd)/out:/app/out davidw93/ariana`
