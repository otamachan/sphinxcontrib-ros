#!/bin/bash
set -e
pip install sphinx .
cd doc
make html
cd _build/html
git init
git add .
git config user.name "Travis CI"
git config user.email "otamachan@gmail.com"
touch .nojekyll
git add .
git commit -m "Deploy to GitHub Pages"
git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1
