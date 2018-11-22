# wework_api

基于 Flask 的企业微信 API，极简、易读、即插即用。 




## 文件结构

* `verify.py`：验证服务器主文件。在首次指定服务器地址或者重新指定服务器地址时，系统会需要对用户提供的服务器地址进行验证。只需要启动该文件后进行验证即可，验证成功后可以关闭。
* `index.py`：服务主文件。在服务器验证完毕后，可以启动该文件提供服务。该文件提供了基本的接收上送消息以及解析消息的能力。具体处理消息的工作可以基于此进一步开发。
* `sendmessage.py`：消息下发类。尽管企业微信可以针对上送的消息进行回应，但存在对应每条上送的消息只能下发一条回应消息、回应消息超时时间太短、无法主动下发消息等弊端，因此将每一条下发的消息都使用主动的方式下发，便于适应多种使用场景。
* `config.py`：主配置文件。对整个项目的一些参数进行配置，其中包括必填参数和可选参数，项目的运行依赖于所有必填参数。在最简情况下，仅需提供所有必填参数即可直接运行。
* `ierror.py`：官方提供的错误类。
* `WXBizMsgCrypt.py`：官方提供的加密类。



## 依赖

* Python 3
  * Crypto 库：官方提供的加密类基于 Crypto 库。
  * flask 库：需要基于 flask 启动 HTTP 服务。
  * requests 库：使用 requests 库构造和发送 HTTP 请求。
  * redis 库：下发消息需要持有有效 token，为提高效率以及避免频率限制，会使用 redis 将 token 缓存到本地直至其失效。
* Redis



## 使用方法

1. 在 `config.py` 中提供所有必填参数，以及按需提供可选参数；
2. 执行 `python3 verify.py` 启动验证服务，准备接收来自企业微信的验证请求；
3. 验证通过后停止验证服务；
4. 执行 `python3 index.py` 启动主服务；
5. to be implemented.



## TODO

* 同步通讯录功能
