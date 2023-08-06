import logging
import random
import re

import base64

from copy import deepcopy
from time import sleep
from collections import OrderedDict

import js2py
from requests.sessions import Session

from urllib.parse import urlparse
from urllib.parse import urlunparse

from cfscrape.jsfuck import jsunfuck
from cfscrape.exceptions import CfParseException, CfCaptchaException


DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
]


BUG_REPORT = """\
Cloudflare may have changed their technique, or there may be a bug in the script.
Raise an issue here: https://github.com/EdmundMartin/cloudflare-scrape
"""


class CloudflareScraper(Session):

    def __init__(self, *args, **kwargs):
        self.delay = kwargs.pop('delay', 8)
        super(CloudflareScraper, self).__init__(*args, **kwargs)
        self._tries = 0
        self._max_tries = kwargs.get('max_tries', 5)
        self._method = None

        if "requests" in self.headers['User-Agent']:
            # Set a random User-Agent if no custom User-Agent has been set
            self.headers["User-Agent"] = random.choice(DEFAULT_USER_AGENTS)

    def set_cloudflare_challenge_delay(self, delay):
        if isinstance(delay, (int, float)) and delay > 0:
            self.delay = delay

    def is_cloudflare_challenge(self, resp):
        if resp.status_code in [429, 503]:
            if b'data-translate="why_captcha_headline' in resp.content:
                raise CfCaptchaException('Page requires solving a Google ReCaptcha to proceed')
            else:
                return resp.headers.get('Server', '').startswith('cloudflare') and b"jschl_vc" in resp.content and b"jschl_answer" in resp.content
        return False

    def request(self, method, url, *args, **kwargs):
        self.headers['Accept-Encoding'] = 'gzip, deflate'
        self.headers['Accept-Language'] = 'en-US,en;q=0.9'
        self.headers['DNT'] = '1'
        self._method = method
        resp = super(CloudflareScraper, self).request(method, url, *args, **kwargs)

        # Check if Cloudflare anti-bot is on
        if self.is_cloudflare_challenge(resp):
            resp = self.solve_cf_challenge(resp, **kwargs)

        return resp

    def solve_cf_challenge(self, resp, **original_kwargs):
        body = resp.text

        # Cloudflare requires a delay before solving the challenge
        if self.delay == 8:
            try:
                delay = float(re.search(r'submit\(\);\r?\n\s*},\s*([0-9]+)', body).group(1)) / float(1000)
                if isinstance(delay, (int, float)):
                    self.delay = delay
            except:
                pass

        sleep(self.delay)

        parsed_url = urlparse(resp.url)
        domain = parsed_url.netloc
        submit_url = '{}://{}/cdn-cgi/l/chk_jschl'.format(parsed_url.scheme, domain)

        cloudflare_kwargs = deepcopy(original_kwargs)
        cloudflare_kwargs.setdefault('headers', {'Referer': resp.url})

        try:
            params = cloudflare_kwargs.setdefault(
                'params', OrderedDict(
                    [
                        ('s', re.search(r'name="s"\svalue="(?P<s_value>[^"]+)', body).group('s_value')),
                        ('jschl_vc', re.search(r'name="jschl_vc" value="(\w+)"', body).group(1)),
                        ('pass', re.search(r'name="pass" value="(.+?)"', body).group(1)),
                    ]
                )
            )

        except Exception as e:
            raise CfParseException("Unable to parse Cloudflare anti-bots page: {} {}".format(e, BUG_REPORT))

        params["jschl_answer"] = self.solve_challenge(body, domain)
        method = resp.request.method

        cloudflare_kwargs["allow_redirects"] = False

        redirect = self.request(method, submit_url, **cloudflare_kwargs)
        if 'Location' not in redirect.headers and self._tries < self._max_tries:
            self._tries += 1
            return self.request(self._method, resp.url)
        elif 'Location' not in redirect.headers:
            raise CfParseException("Unable to pass security after five attempts")
        self._tries = 0
        redirect_location = urlparse(redirect.headers["Location"])

        if not redirect_location.netloc:
            redirect_url = urlunparse(
                (
                    parsed_url.scheme,
                    domain,
                    redirect_location.path,
                    redirect_location.params,
                    redirect_location.query,
                    redirect_location.fragment
                )
            )
            return self.request(method, redirect_url, **original_kwargs)

        return self.request(method, redirect.headers["Location"], **original_kwargs)

    def solve_challenge(self, body, domain):
        try:
            js = re.search(
                r"setTimeout\(function\(\){\s+(var s,t,o,p,b,r,e,a,k,i,n,g,f.+?\r?\n[\s\S]+?a\.value =.+?)\r?\n",
                body
            ).group(1)
        except Exception:
            raise CfParseException("Unable to identify Cloudflare IUAM Javascript on website. {}".format(BUG_REPORT))

        js = re.sub(r"a\.value = ((.+).toFixed\(10\))?", r"\1", js)
        js = re.sub(r'(e\s=\sfunction\(s\)\s{.*?};)', '', js, flags=re.DOTALL | re.MULTILINE)
        js = re.sub(r"\s{3,}[a-z](?: = |\.).+", "", js).replace("t.length", str(len(domain)))

        js = js.replace('; 121', '')

        # Strip characters that could be used to exit the string context
        # These characters are not currently used in Cloudflare's arithmetic snippet
        js = re.sub(r"[\n\\']", "", js)

        if "toFixed" not in js:
            raise CfParseException("Error parsing Cloudflare IUAM Javascript challenge. {}".format(BUG_REPORT))

        try:
            jsEnv = """
            var t = "{domain}";
            var g = String.fromCharCode;
            
            o = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
            e = function(s) {{
                s += "==".slice(2 - (s.length & 3));
                var bm, r = "", r1, r2, i = 0;
                for (; i < s.length;) {{
                    bm = o.indexOf(s.charAt(i++)) << 18 | o.indexOf(s.charAt(i++)) << 12 | (r1 = o.indexOf(s.charAt(i++))) << 6 | (r2 = o.indexOf(s.charAt(i++)));
                    r += r1 === 64 ? g(bm >> 16 & 255) : r2 === 64 ? g(bm >> 16 & 255, bm >> 8 & 255) : g(bm >> 16 & 255, bm >> 8 & 255, bm & 255);
                }}
                return r;
            }};

            
            function italics (str) {{ return '<i>' + this + '</i>'; }};
            var document = {{
                getElementById: function () {{
                    return {{'innerHTML': '{innerHTML}'}};
                }}
            }};
            {js}
            """

            innerHTML = re.search(
                '<div(?: [^<>]*)? id="([^<>]*?)">([^<>]*?)<\/div>',
                body,
                re.MULTILINE | re.DOTALL
            )
            innerHTML = innerHTML.group(2).replace("'", r"\'") if innerHTML else ""

            js = jsunfuck(jsEnv.format(domain=domain, innerHTML=innerHTML, js=js))

            def atob(s):
                return base64.b64decode('{}'.format(s)).decode('utf-8')
            
            js2py.disable_pyimport()
            context = js2py.EvalJs({"atob": atob})
            result = context.eval(js)
        except Exception:
            logging.error("Error executing Cloudflare IUAM Javascript. {}".format(BUG_REPORT))
            raise 

        try:
            float(result)
        except Exception:
            raise ValueError("Cloudflare IUAM challenge returned unexpected answer. {}".format(BUG_REPORT))

        return result

    @classmethod
    def create_scraper(cls, sess=None, **kwargs):
        """
        Convenience function for creating a ready-to-go CloudflareScraper object.
        """
        scraper = cls(**kwargs)

        if sess:
            attrs = ['auth', 'cert', 'cookies', 'headers', 'hooks', 'params', 'proxies', 'data']
            for attr in attrs:
                val = getattr(sess, attr, None)
                if val:
                    setattr(scraper, attr, val)

        return scraper

    # Functions for integrating cloudflare-scrape with other applications and scripts
    @classmethod
    def get_tokens(cls, url, user_agent=None, **kwargs):
        scraper = cls.create_scraper()
        if user_agent:
            scraper.headers["User-Agent"] = user_agent

        try:
            resp = scraper.get(url, **kwargs)
            resp.raise_for_status()
        except Exception as e:
            raise CfParseException("Could not get tokens for given URL: {}, {}".format(url, e))

        domain = urlparse(resp.url).netloc

        for d in scraper.cookies.list_domains():
            if d.startswith(".") and d in ("." + domain):
                cookie_domain = d
                break
        else:
            raise ValueError("Unable to find Cloudflare cookies. Does the site actually have Cloudflare IUAM (\"I'm Under Attack Mode\") enabled?")

        return (
            {
                "__cfduid": scraper.cookies.get("__cfduid", "", domain=cookie_domain),
                "cf_clearance": scraper.cookies.get("cf_clearance", "", domain=cookie_domain)
            },
            scraper.headers["User-Agent"]
        )

    @classmethod
    def get_cookie_string(cls, url, user_agent=None, **kwargs):
        """
        Convenience function for building a Cookie HTTP header value.
        """
        tokens, user_agent = cls.get_tokens(url, user_agent=user_agent, **kwargs)
        return "; ".join("=".join(pair) for pair in tokens.items()), user_agent


create_scraper = CloudflareScraper.create_scraper
get_tokens = CloudflareScraper.get_tokens
get_cookie_string = CloudflareScraper.get_cookie_string
