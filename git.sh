git add --all

echo "Please input commit message"
read MSG

git commit -am $MSG

git push
