# research.loop receipt — 2026-06-17T00:29:42Z

target: cheaper/faster local inference (MLX tricks, quantization, speculative decoding)

Traceback (most recent call last):
  File "$HOME/grokgo/spikes/openclaude-local/badass-fable.py", line 117, in <module>
    main()
    ~~~~^^
  File "$HOME/grokgo/spikes/openclaude-local/badass-fable.py", line 93, in main
    print(chat(messages))
          ~~~~^^^^^^^^^^
  File "$HOME/grokgo/spikes/openclaude-local/badass-fable.py", line 78, in chat
    return chat_http(messages, timeout=timeout)
  File "$HOME/grokgo/spikes/openclaude-local/badass-fable.py", line 47, in chat_http
    with urllib.request.urlopen(req, timeout=timeout) as r:
         ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 187, in urlopen
    return opener.open(url, data, timeout)
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 487, in open
    response = self._open(req, data)
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 504, in _open
    result = self._call_chain(self.handle_open, protocol, protocol +
                              '_open', req)
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 464, in _call_chain
    result = func(*args)
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 1350, in http_open
    return self.do_open(http.client.HTTPConnection, req)
           ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/urllib/request.py", line 1325, in do_open
    r = h.getresponse()
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/http/client.py", line 1459, in getresponse
    response.begin()
    ~~~~~~~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/http/client.py", line 336, in begin
    version, status, reason = self._read_status()
                              ~~~~~~~~~~~~~~~~~^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/http/client.py", line 297, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
               ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.14/3.14.5/Frameworks/Python.framework/Versions/3.14/lib/python3.14/socket.py", line 729, in readinto
    return self._sock.recv_into(b)
           ~~~~~~~~~~~~~~~~~~~~^^^
TimeoutError: timed out
