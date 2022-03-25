
```sh
# find IP
ifconfig
# find the local IP address
ifconfig | grep inet | grep broadcast

# download file from website
wget https://{file}
# download file from server to local
scp {user}@{server}:{server_path}/{file} {local_path}/{file}
# upload file from local to server
scp -P{port} {local_path}/{file} {user}@{server}:~/{server_path}
# download the whole directory
scp -r {user}@{server}:{server_path}/{directory} {local_path}/

# synchronize a file
rsync -zvh {source}/{file} {target}/
# synchronize directories
rsync -zarvh --progress {source}/ {target}/

# check HTTP response headers
curl -i https://httpbin.org/get
# download file from the web, resume if the connection was previously lost
curl -O -C - {web_file}
# redirect if the website has a chain of redirects
curl -L --max-redirs {number} {web}
# return verbose info from the web, `>` for request data, `<` for response headers, `*` for other details about the request
curl -v {web}
# send post request with specified headers and data
curl -X POST {web} \
    -H '{key1}: {value1}' -H '{key2}: {value2}' \
    -d @{file}

# check public IP
curl ifconfig.me
curl ifconfig.co
# check private IP
hostname -I | awk '{print $i}'
```
