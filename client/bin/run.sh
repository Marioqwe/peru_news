#!/bin/bash

npm install

if [ "$NODE_ENV" = 'production' ]; then
    npm run build-production
else # default to development.
    npm run watch
fi
