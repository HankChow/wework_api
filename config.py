########## 以下为必填参数，填写后方可运行

# 在“接收消息服务器配置”中填写的 Token 值
TOKEN=''

# 在“接收消息服务器配置”中填写的 EncodingAESKey 值
ENCODINGAWSKEY=''

# 所属企业的企业 ID
CORPID=''

# 下发消息是使用的应用 Secret 值
CORPSECRET=''

# 下发消息时使用的应用 ID
AGENTID=''

########## 以上为必填参数，填写后方可运行





########## 以下为可选参数，默认全为 None

# 接收消息服务器的端口，默认为 80
SERVERPORT=None

# 下发消息的最大字符数，当消息大于 2048 字符时会被企业微信截断为前 2048 字符，长消息将会以该参数值为长度被切分为多条消息，默认为2000
MESSAGELENGTH=None

########## 以上为可选参数，默认全为 None





########## 配置参数检查
if not SERVERPORT:
    SERVERPORT = 80
if not MESSAGELENGTH or MESSAGELENGTH > 2000:
    MESSAGELENGTH = 2000
