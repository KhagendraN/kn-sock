from kn_sock import http_get, http_post

if __name__ == "__main__":
    print("[HTTP][CLIENT] GET example:")
    body = http_get("example.com", 80, "/")
    print(body[:200], "...\n")

    print("[HTTP][CLIENT] POST example:")
    body = http_post("httpbin.org", 80, "/post", data="foo=bar&baz=qux")
    print(body[:200], "...\n")
