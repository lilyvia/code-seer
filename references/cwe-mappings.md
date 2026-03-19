# CWE 漏洞映射表

本文件将安全审计中识别的9种常见漏洞类型映射到对应的CWE(Common Weakness Enumeration)ID,并提供中文描述和风险评估。

---

## 1. SQL注入 (SQL Injection)

**CWE ID**: CWE-89

### 中文描述
SQL注入是一种代码注入技术,攻击者通过在输入字段中插入恶意SQL语句,使得应用程序执行非预期的数据库操作。这种漏洞通常出现在应用程序直接使用用户输入构建SQL查询而未进行适当过滤或参数化的情况下。

### 常见攻击场景
- **登录绕过**: 攻击者在用户名或密码字段输入 `' OR '1'='1`,绕过身份验证
- **数据窃取**: 利用 `UNION SELECT` 语句从其他表中提取敏感数据
- **数据库结构探测**: 通过错误信息或时间延迟推断数据库结构和版本
- **数据篡改**: 使用 `UPDATE` 或 `DELETE` 语句修改或删除数据
- **权限提升**: 执行存储过程或系统命令获取更高权限

### 风险等级
**高危** (Critical)

SQL注入可能导致:
- 完整的数据库泄露
- 数据完整性破坏
- 服务器完全被控制(在某些数据库配置下)

### OWASP Top 10 映射
- **2017 A1**: Injection
- **2021 A03**: Injection

---

## 2. 跨站脚本攻击 XSS (Cross-Site Scripting)

**CWE ID**: CWE-79

### 中文描述
XSS漏洞允许攻击者将恶意脚本注入到受信任的网页中。当用户浏览包含恶意脚本的页面时,脚本会在用户的浏览器中执行,从而窃取用户信息、会话令牌或执行其他恶意操作。

### 常见攻击场景
- **存储型XSS**: 恶意脚本被永久存储在目标服务器上(如论坛帖子、评论区)
- **反射型XSS**: 恶意脚本通过URL参数传递,诱导用户点击恶意链接
- **DOM型XSS**: 通过修改页面DOM结构触发,不涉及服务器端处理
- **Cookie窃取**: 利用 `document.cookie` 获取用户会话信息
- **键盘记录**: 记录用户在页面上的键盘输入

### 风险等级
**中危-高危** (Medium-High)

XSS可能导致:
- 会话劫持
- 用户凭证泄露
- 钓鱼攻击
- 恶意软件分发

### OWASP Top 10 映射
- **2017 A7**: Cross-Site Scripting (XSS)
- **2021 A03**: Injection

---

## 3. 命令执行 (Command Injection)

**CWE ID**: CWE-78

### 中文描述
命令执行漏洞发生在应用程序将用户输入直接传递给操作系统命令解释器(如shell)时。攻击者可以注入额外的命令字符,在服务器上执行任意操作系统命令。

### 常见攻击场景
- **系统命令拼接**: 使用分号 `;` 或逻辑运算符 `&&` 注入额外命令
- **管道注入**: 利用管道符 `|` 将数据传递给其他命令
- **反向shell**: 使用 `nc` 或 `/bin/sh` 建立反向连接
- **文件读取**: 使用 `cat` 命令读取敏感文件如 `/etc/passwd`
- **权限探测**: 使用 `whoami`, `id` 等命令获取系统信息

### 风险等级
**高危-严重** (High-Critical)

命令执行可能导致:
- 服务器完全控制
- 内网渗透
- 数据泄露和篡改
- 服务中断

### OWASP Top 10 映射
- **2017 A1**: Injection
- **2021 A03**: Injection

---

## 4. 反序列化漏洞 (Deserialization Vulnerability)

**CWE ID**: CWE-502

### 中文描述
不安全的反序列化漏洞发生在应用程序反序列化来自不可信来源的数据时。攻击者可以构造恶意序列化对象,在反序列化过程中执行任意代码或触发非预期的应用程序行为。

### 常见攻击场景
- **POP链攻击**: 构造Property-Oriented Programming链,通过魔术方法触发恶意代码
- **Gadget利用**: 利用已知类库中的危险方法组合(gadget)执行命令
- **类型混淆**: 通过修改序列化数据中的类型信息绕过安全检查
- **Java反序列化**: 利用 `ObjectInputStream` 的已知漏洞
- **PHP对象注入**: 利用PHP的 `unserialize()` 函数特性

### 风险等级
**严重** (Critical)

不安全的反序列化可能导致:
- 远程代码执行(RCE)
- 身份认证绕过
- 拒绝服务攻击
- 数据篡改

### OWASP Top 10 映射
- **2017 A8**: Insecure Deserialization
- **2021 A08**: Software and Data Integrity Failures

---

## 5. 路径穿越 (Path Traversal)

**CWE ID**: CWE-22

### 中文描述
路径穿越(也称为目录遍历)漏洞允许攻击者通过 `../` 或 `..\` 等序列访问服务器文件系统中受限的文件和目录。应用程序未能正确验证或净化用户提供的文件路径时,就会出现此漏洞。

### 常见攻击场景
- **敏感文件读取**: 使用 `../../../etc/passwd` 读取系统文件
- **配置文件泄露**: 访问 `../config/database.yml` 等配置文件
- **源代码泄露**: 读取应用程序源代码文件
- **日志文件访问**: 获取包含敏感信息的日志文件
- **空字节绕过**: 使用 `%00` 截断绕过文件扩展名检查

### 风险等级
**中危-高危** (Medium-High)

路径穿越可能导致:
- 敏感信息泄露
- 源代码泄露导致进一步的漏洞挖掘
- 配置文件信息泄露

### OWASP Top 10 映射
- **2017 A5**: Broken Access Control
- **2021 A01**: Broken Access Control

---

## 6. 服务器端请求伪造 SSRF (Server-Side Request Forgery)

**CWE ID**: CWE-918

### 中文描述
SSRF漏洞允许攻击者诱使服务器应用程序向攻击者选择的任意域名发送HTTP请求。攻击者可以利用此漏洞访问内部服务、绕过防火墙限制或与内部API交互。

### 常见攻击场景
- **内网探测**: 扫描内网开放的端口和服务(如 `http://127.0.0.1:22`)
- **元数据服务访问**: 访问云服务商的元数据API(如AWS `169.254.169.254`)
- **内部API调用**: 调用只有服务器能访问的内部管理接口
- **文件协议利用**: 使用 `file:///etc/passwd` 读取本地文件
- **Redis/ElasticSearch攻击**: 向未授权访问的内部服务发送恶意请求

### 风险等级
**高危-严重** (High-Critical)

SSRF可能导致:
- 内部网络信息泄露
- 云环境凭据泄露
- 内部服务被攻击
- 远程代码执行(配合其他服务)

### OWASP Top 10 映射
- **2021 A10**: Server-Side Request Forgery (SSRF)

---

## 7. XML外部实体注入 XXE (XML External Entity Injection)

**CWE ID**: CWE-611

### 中文描述
XXE漏洞发生在应用程序解析XML输入时,允许引用外部实体。攻击者可以利用此漏洞读取服务器上的任意文件、执行服务器端请求伪造(SSRF)或导致拒绝服务攻击。

### 常见攻击场景
- **文件读取**: 通过 `<!ENTITY xxe SYSTEM "file:///etc/passwd">` 读取文件
- **内网探测**: 利用外部实体请求内网资源
- **拒绝服务**: 通过递归实体引用( Billion Laughs攻击)消耗系统资源
- **数据外带**: 通过将文件内容作为URL参数发送到攻击者服务器
- **远程代码执行**: 在PHP等环境中通过 `expect` 包装器执行命令

### 风险等级
**高危** (High)

XXE可能导致:
- 任意文件读取
- 服务器端请求伪造
- 拒绝服务
- 内部网络信息泄露

### OWASP Top 10 映射
- **2017 A4**: XML External Entities (XXE)
- **2021 A05**: Security Misconfiguration

---

## 8. 鉴权缺陷 (Authentication Weakness)

**CWE ID**: CWE-287 (Improper Authentication), CWE-306 (Missing Authentication for Critical Function)

### 中文描述
鉴权缺陷包括多种认证相关的问题,如弱密码策略、会话管理不当、缺少多因素认证、硬编码凭据等。这些缺陷可能导致攻击者绕过认证机制或冒充其他用户。

### 常见攻击场景
- **暴力破解**: 针对弱密码或缺少速率限制的登录接口
- **会话固定**: 攻击者强制用户使用已知的会话ID
- **会话劫持**: 窃取或预测会话令牌
- **JWT弱点**: 使用弱签名算法(如 `none` 算法)或密钥混淆攻击
- **缺少认证**: 敏感API端点未进行身份验证
- **密码重置绕过**: 通过篡改重置令牌或安全问题绕过验证

### 风险等级
**中危-高危** (Medium-High)

鉴权缺陷可能导致:
- 未授权访问
- 账户接管
- 权限提升
- 敏感数据泄露

### OWASP Top 10 映射
- **2017 A2**: Broken Authentication
- **2021 A07**: Identification and Authentication Failures

---

## 9. 硬编码密钥 (Hardcoded Credentials)

**CWE ID**: CWE-798

### 中文描述
硬编码密钥指将密码、API密钥、加密密钥或其他敏感凭据直接嵌入到源代码、配置文件或二进制文件中。这使得任何能够访问代码的人都能获取这些敏感信息。

### 常见攻击场景
- **源代码泄露**: 从公开的代码仓库(如GitHub)获取硬编码凭据
- **反编译攻击**: 从编译后的二进制文件中提取密钥
- **配置信息泄露**: 配置文件中的数据库密码或API密钥
- **默认凭据**: 使用产品默认的管理员密码未修改
- **硬编码JWT密钥**: 应用程序使用硬编码的密钥签名JWT令牌
- **AWS/Azure密钥泄露**: 云服务商访问密钥硬编码在代码中

### 风险等级
**高危** (High)

硬编码密钥可能导致:
- 完全系统接管
- 数据泄露
- 云服务资源被滥用
- 供应链攻击

### OWASP Top 10 映射
- **2021 A07**: Identification and Authentication Failures

---

## 风险等级汇总表

| 漏洞类型 | CWE ID | 风险等级 | OWASP Top 10 (2021) |
|---------|--------|---------|---------------------|
| SQL注入 | CWE-89 | Critical | A03: Injection |
| XSS | CWE-79 | Medium-High | A03: Injection |
| 命令执行 | CWE-78 | High-Critical | A03: Injection |
| 反序列化漏洞 | CWE-502 | Critical | A08: Software and Data Integrity Failures |
| 路径穿越 | CWE-22 | Medium-High | A01: Broken Access Control |
| SSRF | CWE-918 | High-Critical | A10: Server-Side Request Forgery |
| XXE | CWE-611 | High | A05: Security Misconfiguration |
| 鉴权缺陷 | CWE-287, CWE-306 | Medium-High | A07: Identification and Authentication Failures |
| 硬编码密钥 | CWE-798 | High | A07: Identification and Authentication Failures |

---

## 参考资料

- [CWE 官方网站](https://cwe.mitre.org/)
- [OWASP Top 10 2021](https://owasp.org/Top10/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
