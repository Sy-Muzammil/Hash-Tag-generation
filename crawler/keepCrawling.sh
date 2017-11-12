source venv/bin/activate
while [ 1 ]
do
    python tweetsMedia.py > XLOG 2>&1
    sleep 10
done
