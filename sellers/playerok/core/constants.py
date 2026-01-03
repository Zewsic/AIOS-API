BASE_HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "access-control-allow-headers": "sentry-trace, baggage",
    "apollo-require-preflight": "true",
    "apollographql-client-name": "web",
    "content-type": "application/json",
    "origin": "https://playerok.com",
    "priority": "u=1, i",
    "referer": "https://playerok.com/",
    "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-gql-op": "viewer",
    "x-gql-path": "/products/[slug]",
    "x-timezone-offset": "-180",
}

EXAMPLE_USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 7_0_2; en-US) Gecko/20100101 Firefox/57.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 9_8_3) AppleWebKit/534.47 (KHTML, like Gecko) Chrome/51.0.1124.252 Safari/535",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_2_9) Gecko/20100101 Firefox/65.6",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_0_2) AppleWebKit/536.44 (KHTML, like Gecko) Chrome/49.0.2950.348 Safari/602",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 9_9_9; en-US) Gecko/20130401 Firefox/59.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1_1; en-US) AppleWebKit/534.17 (KHTML, like Gecko) Chrome/53.0.2619.208 Safari/535",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_7_8) Gecko/20130401 Firefox/59.9",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_0) Gecko/20130401 Firefox/68.4",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_3_5; en-US) Gecko/20100101 Firefox/53.9",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 7_1_1; en-US) Gecko/20130401 Firefox/61.0",
]

CLOUDFLARE_SIGNATURES = [
    "<title>Just a moment...</title>",
    "window._cf_chl_opt",
    "Enable JavaScript and cookies to continue",
    "Checking your browser before accessing",
    "cf-browser-verification",
    "Cloudflare Ray ID",
]
