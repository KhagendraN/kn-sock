# Testing & Troubleshooting

## Known Issues & Troubleshooting

| Issue               | Symptom/Output                         | Solution                                  |
|---------------------|----------------------------------------|-------------------------------------------|
| Port already in use | `[Errno 98] Address already in use`    | Use a different port or kill other process|
| No response/404     | `404 Not found` or empty output        | Check route/path; static only by default  |
| HTTPS errors        | SSL certificate errors                 | Use valid/test certs or skip verification |
| Hostname not found  | `[Errno -2] Name or service not known` | Use container IP for Docker setups        |

## Manual Test

Start the server
```bash
docker-compose run --rm knsock run-http-server 8000
```

In another terminal
```bash
docker-compose run --rm knsock http-get <server-ip> 8000 /
# Example:
docker-compose run --rm knsock http-get 172.18.0.2 8000 /
```

Verify that the response is 200 OK and that the expected body appears.

### Related Topics

* **[CLI commands](cli.md)**
* **[Python API](python-api.md)**
* **[Reference](reference.md)**