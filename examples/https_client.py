from kn_sock import https_get, https_post

if __name__ == "__main__":
    print("[HTTPS][CLIENT] GET example:")
    body = https_get("example.com", 443, "/")
    print(body[:200], "...\n")

    print("[HTTPS][CLIENT] POST example:")
    body = https_post("httpbin.org", 443, "/post", data="foo=bar&baz=qux")
    print(body[:200], "...\n")
