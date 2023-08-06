def __setup__():
    import base64
    import binascii
    import cbor2
    import cgi
    import functools
    import inspect
    import json
    import os
    import struct
    import threading
    import types
    import urllib.parse

    def iter2http(it, headers=None):
        length = 0
        if headers is None:
            headers = {"Content-Type": "text/html; charset=UTF-8"}
            yield headers

        for element in it:
            if element is None:
                yield b""
            elif isinstance(element, dict):
                headers.update(element)
            elif isinstance(element, (list, set, tuple, range, types.GeneratorType)):
                for subelement in iter2http(element, headers):
                    length += len(subelement)
                    yield subelement
            elif isinstance(element, bytes):
                length += len(element)
                yield element
            else:
                element = str(element).encode("utf-8")
                length += len(element)
                yield element

        headers["Content-Length"] = length

    class LimmatScreen(object):
        def __init__(self, app, ref_id, func, **kwargs):
            self._app = app
            self._ref_id = ref_id
            self._func = func
            self._sig = inspect.signature(func)
            num_pargs = 0
            self._kwarg_names = []
            for name, param in self._sig.parameters.items():
                if param.kind == param.POSITIONAL_OR_KEYWORD:
                    num_pargs += 1
                elif param.kind == param.KEYWORD_ONLY:
                    self._kwarg_names.append(name)
                else:
                    raise ValueError(
                        f"{func}: {name} must be POSITIONAL_OR_KEYWORD or KEYWORD_ONLY"
                    )

            if num_pargs != 1:
                raise ValueError(f"{func}: exactly ONE parameter POSITIONAL_OR_KEYWORD")

        def link(self, **kwargs):
            for name in kwargs:
                if name not in self._kwarg_names:
                    raise ValueError(f"unknown parameter {name}")

            return "/" + self._app.dumps([self._ref_id, self._app._ctx, kwargs])

        def __str__(self):
            return self.link()

        def invoke(self, kwargs, request_args):
            for name, value in request_args.items():
                if name not in self._sig.parameters:
                    continue
                if name not in kwargs:
                    kwargs[name] = value

            context = self._app._ctx
            bound = self._sig.bind(context, **kwargs)
            bound.apply_defaults()
            return self._func(*bound.args, **bound.kwargs)

    class LimmatApp(threading.local):
        def __init__(self):
            self._refs = {}
            self._entrypoints = {}
            self._key = bytes.fromhex("0f4ec041f8ee504c37e5b0c87558e301")
            self._ctx = {}

        def screen(self, _func=None, **kwargs):
            if _func is None:
                return functools.partial(self.screen, **kwargs)

            ref_id = len(self._refs)
            self._refs[ref_id] = LimmatScreen(self, ref_id, _func, **kwargs)

            entrypoint = kwargs.get("entrypoint")
            if entrypoint:
                self._entrypoints[entrypoint] = self._refs[ref_id]

            return self._refs[ref_id]

        def dumps(self, obj):
            data = cbor2.dumps(obj)
            k = struct.unpack(">4L", self._key)
            xx = os.urandom(8)
            iv = xx

            data = struct.pack(">L", len(data)) + data
            data += os.urandom(8 - (len(data) % 8))
            out = [xx]

            i = 0
            while i < len(data):
                v0, v1 = struct.unpack(
                    ">2L", bytes([(x ^ y) for x, y in zip(iv, data[i: i + 8])])
                )
                i += 8

                s, delta, mask = 0, 0x9E3779B9, 0xFFFFFFFF
                for _ in range(48):
                    v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + k[s & 3]))) & mask
                    s = (s + delta) & mask
                    v1 = (v1 + (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + k[s >> 11 & 3]))) & mask

                iv = struct.pack(">2L", v0, v1)
                out.append(iv)

            tmp = base64.urlsafe_b64encode(b"".join(out)).decode("ascii")
            return tmp

        def loads(self, s):
            data = base64.urlsafe_b64decode(s.encode("ascii"))
            k = struct.unpack(">4L", self._key)
            iv = data[:8]
            out = []

            i = 8
            while i < len(data):
                block = data[i: i + 8]
                i += 8

                v0, v1 = struct.unpack(">2L", block)
                delta, mask = 0x9E3779B9, 0xFFFFFFFF
                s = (delta * 48) & mask

                for _ in range(48):
                    v1 = (v1 - (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + k[s >> 11 & 3]))) & mask
                    s = (s - delta) & mask
                    v0 = (v0 - (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + k[s & 3]))) & mask

                dec = bytes([(x ^ y) for x, y in zip(iv, struct.pack(">2L", v0, v1))])
                iv = block

                out.append(dec)

            data = b"".join(out)
            length = struct.unpack(">L", data[:4])[0]
            return cbor2.loads(data[4: length + 4])

        def __call__(self, environ, start_response):
            method = environ.get("REQUEST_METHOD")

            # Guard against unsupported HTTP verbs
            if method not in ("GET", "POST"):
                start_response("403 Forbidden", [])
                return []

            # Parse the request
            path = environ.get("PATH_INFO")
            args = urllib.parse.parse_qsl(
                environ.get("QUERY_STRING"), keep_blank_values=True
            )

            if method == "POST":
                reqfh = environ.get("wsgi.input")
                mime, ctargs = cgi.parse_header(environ.get("CONTENT_TYPE"))
                charset = ctargs.get("charset", "ascii")
                clen = int(environ.get("CONTENT_LENGTH"))

                if mime in (
                    "application/x-www-form-urlencoded",
                    "application/x-url-encoded",
                ):
                    body = reqfh.read(clen).decode(charset)
                    args.extend(urllib.parse.parse_qsl(body, keep_blank_values=True))

                elif mime == "application/json":
                    body = reqfh.read(clen).decode(charset)
                    args.extend(json.loads(body).items())

                elif mime == "multipart/form-data":
                    pdict = {
                        "boundary": ctargs.get("boundary").encode("ascii"),
                        "CONTENT-LENGTH": clen,
                    }
                    for name, values in cgi.parse_multipart(
                        reqfh, pdict, encoding=charset
                    ).items():
                        for value in values:
                            args.append((name, value))

            # Transforming args
            argdict = {}
            for name, value in args:
                if name not in argdict:
                    argdict[name] = value
                elif isinstance(argdict[name], list):
                    argdict[name].append(value)
                else:
                    argdict[name] = [argdict[name], value]

            results = []
            if method == "GET" and path in self._entrypoints:
                self._ctx = {}
                results.append({"Location": self._entrypoints[path].link()})

            else:
                try:
                    ref_id, ctx, kwargs = self.loads(path[1:])
                    self._ctx = ctx
                    handler = self._refs[ref_id]
                    results.append(handler.invoke(kwargs, argdict))

                except binascii.Error:
                    pass

                except struct.error:
                    pass

            results = iter2http(results)
            headers = next(results)
            results = list(results)

            if "Location" in headers:
                status = "303 See Other"
            elif results:
                status = "200 OK"
            else:
                status = "403 Forbidden"

            header_list = []
            for key, value in headers.items():
                header_list.append((str(key), str(value)))

            start_response(status, header_list)
            return results

    app = LimmatApp()

    def get_app_instance():
        return app

    return get_app_instance


get_app = __setup__()
del __setup__
