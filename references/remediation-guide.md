# 安全漏洞修复指南

本指南提供针对9种常见安全漏洞的详细修复步骤,包含多语言安全代码示例和最佳实践。

---

## 目录

1. [SQL注入修复](#1-sql注入修复)
2. [XSS跨站脚本修复](#2-xss跨站脚本修复)
3. [命令执行修复](#3-命令执行修复)
4. [反序列化漏洞修复](#4-反序列化漏洞修复)
5. [路径穿越修复](#5-路径穿越修复)
6. [SSRF修复](#6-ssrf修复)
7. [XXE修复](#7-xxe修复)
8. [鉴权缺陷修复](#8-鉴权缺陷修复)
9. [硬编码密钥修复](#9-硬编码密钥修复)

---

## 1. SQL注入修复

### 修复步骤

1. **使用参数化查询(Prepared Statements)**: 永远不要将用户输入直接拼接到SQL语句中
2. **使用ORM框架**: 优先使用ORM框架,它们通常内置了防护机制
3. **输入验证**: 对所有用户输入进行白名单验证
4. **最小权限原则**: 数据库账户只授予必要的权限
5. **错误处理**: 不要向用户暴露详细的数据库错误信息

### 安全代码示例

#### Python (使用参数化查询)
```python
# 不安全的代码
user_input = request.form['username']
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)  # 危险!

# 安全的代码 - 使用参数化查询
def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))  # 参数化查询
    return cursor.fetchone()

# 使用ORM (SQLAlchemy)
from sqlalchemy import text

def get_user_safe(username):
    # SQLAlchemy自动使用参数化查询
    result = db.session.query(User).filter_by(username=username).first()
    return result
```

#### Java (使用PreparedStatement)
```java
// 不安全的代码
String query = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);  // 危险!

// 安全的代码 - 使用PreparedStatement
public User getUserByUsername(String username) {
    String query = "SELECT * FROM users WHERE username = ?";
    try (PreparedStatement pstmt = connection.prepareStatement(query)) {
        pstmt.setString(1, username);  // 参数绑定
        ResultSet rs = pstmt.executeQuery();
        // 处理结果...
    }
}

// 使用JPA/Hibernate
@Entity
public class User {
    @Id
    private Long id;
    private String username;
}

// Repository接口自动防护SQL注入
public interface UserRepository extends JpaRepository<User, Long> {
    User findByUsername(String username);  // 安全
}
```

#### Go (使用database/sql)
```go
// 不安全的代码
query := fmt.Sprintf("SELECT * FROM users WHERE username = '%s'", username)
rows, err := db.Query(query)  // 危险!

// 安全的代码 - 使用参数化查询
func getUserByUsername(db *sql.DB, username string) (*User, error) {
    query := "SELECT id, username, email FROM users WHERE username = ?"
    row := db.QueryRow(query, username)  // 参数化查询
    
    var user User
    err := row.Scan(&user.ID, &user.Username, &user.Email)
    if err != nil {
        return nil, err
    }
    return &user, nil
}

// 使用GORM ORM
func getUserWithGORM(db *gorm.DB, username string) (*User, error) {
    var user User
    result := db.Where("username = ?", username).First(&user)
    if result.Error != nil {
        return nil, result.Error
    }
    return &user, nil
}
```

#### PHP (使用PDO)
```php
<?php
// 不安全的代码
$username = $_POST['username'];
$query = "SELECT * FROM users WHERE username = '$username'";
$result = mysqli_query($conn, $query);  // 危险!

// 安全的代码 - 使用PDO预处理语句
function getUserByUsername($pdo, $username) {
    $stmt = $pdo->prepare("SELECT * FROM users WHERE username = :username");
    $stmt->bindParam(':username', $username, PDO::PARAM_STR);
    $stmt->execute();
    return $stmt->fetch(PDO::FETCH_ASSOC);
}

// 使用Laravel Eloquent ORM
$user = User::where('username', $request->input('username'))->first();  // 安全

// 使用Doctrine ORM
$userRepository = $entityManager->getRepository(User::class);
$user = $userRepository->findOneBy(['username' => $username]);  // 安全
?>
```

#### C# (使用参数化查询)
```csharp
// 不安全的代码
string query = $"SELECT * FROM Users WHERE Username = '{username}'";
SqlCommand cmd = new SqlCommand(query, connection);  // 危险!

// 安全的代码 - 使用参数化查询
public User GetUserByUsername(string username)
{
    string query = "SELECT * FROM Users WHERE Username = @username";
    using (SqlCommand cmd = new SqlCommand(query, connection))
    {
        cmd.Parameters.AddWithValue("@username", username);
        using (SqlDataReader reader = cmd.ExecuteReader())
        {
            // 处理结果...
        }
    }
}

// 使用Entity Framework Core
public class ApplicationDbContext : DbContext
{
    public DbSet<User> Users { get; set; }
}

// EF Core自动防护SQL注入
public User GetUserSafe(string username)
{
    return _context.Users
        .FirstOrDefault(u => u.Username == username);  // 安全
}
```

### 最佳实践

- 始终使用参数化查询,即使在LIKE子句中
- 对动态排序字段使用白名单验证
- 避免在存储过程中拼接SQL
- 定期进行SQL注入扫描测试

### 参考资源

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) - SQL注入防护速查表
- [OWASP Query Parameterization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Query_Parameterization_Cheat_Sheet.html) - 查询参数化速查表

---

## 2. XSS跨站脚本修复

### 修复步骤

1. **输出编码**: 对所有动态输出进行HTML实体编码
2. **内容安全策略(CSP)**: 实施CSP限制脚本执行
3. **输入验证**: 验证和清理用户输入
4. **HttpOnly Cookie**: 设置Cookie的HttpOnly标志
5. **现代框架**: 使用自动转义的模板引擎

### 安全代码示例

#### Python
```python
from html import escape
from markupsafe import Markup

# 输出编码
def render_user_content(user_input):
    # 自动转义HTML特殊字符
    safe_content = escape(user_input)
    return f"<div>{safe_content}</div>"

# Flask模板自动转义
from flask import render_template

@app.route('/profile')
def profile():
    user_comment = request.args.get('comment')
    # Jinja2模板默认自动转义
    return render_template('profile.html', comment=user_comment)

# Django模板自动转义
# {{ user_input }}  # 自动转义
# {{ user_input|safe }}  # 手动关闭转义(危险,需谨慎)
```

#### Java
```java
import org.owasp.encoder.Encode;

public class XSSProtection {
    // HTML上下文编码
    public String encodeForHTML(String input) {
        return Encode.forHtml(input);
    }
    
    // JavaScript上下文编码
    public String encodeForJS(String input) {
        return Encode.forJavaScript(input);
    }
    
    // URL上下文编码
    public String encodeForURL(String input) {
        return Encode.forUriComponent(input);
    }
}

// Spring Security CSP配置
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.headers()
            .contentSecurityPolicy("default-src 'self'; script-src 'self'")
            .and()
            .httpStrictTransportSecurity();
        return http.build();
    }
}
```

#### Go
```go
import (
    "html/template"
    "net/http"
)

// Go的html/template自动转义HTML
type PageData struct {
    Title   string
    Content string
}

func handler(w http.ResponseWriter, r *http.Request) {
    data := PageData{
        Title:   "User Profile",
        Content: r.FormValue("comment"),  // 自动转义
    }
    
    tmpl := template.Must(template.ParseFiles("template.html"))
    tmpl.Execute(w, data)  // 自动HTML编码
}

// 手动HTML编码
import "html"

func escapeHTML(input string) string {
    return html.EscapeString(input)
}
```

#### PHP
```php
<?php
// 手动编码
$user_input = $_GET['comment'];
$safe_output = htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');
echo "<div>" . $safe_output . "</div>";

// Blade模板自动转义 (Laravel)
// {{ $user_input }}  // 自动转义
// {!! $user_input !!}  // 不转义(仅用于可信内容)

// Twig模板自动转义 (Symfony)
// {{ user_input }}  // 自动转义
// {{ user_input|raw }}  // 不转义

// 设置HttpOnly Cookie
setcookie("session_id", $token, [
    'expires' => time() + 3600,
    'path' => '/',
    'secure' => true,
    'httponly' => true,  // 防止JavaScript访问
    'samesite' => 'Strict'
]);
?>
```

#### C#
```csharp
using System.Web;
using System.Text.Encodings.Web;

// HTML编码
public string EncodeForHtml(string input)
{
    return HttpUtility.HtmlEncode(input);
    // 或使用 HtmlEncoder.Default.Encode(input)
}

// Razor视图自动编码
// @Model.UserInput  // 自动HTML编码
// @Html.Raw(Model.UserInput)  // 不编码(谨慎使用)

// ASP.NET Core CSP
public void Configure(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        context.Response.Headers.Add("Content-Security-Policy", 
            "default-src 'self'; script-src 'self' 'unsafe-inline'");
        await next();
    });
}

// AntiForgeryToken (CSRF防护)
[ValidateAntiForgeryToken]
[HttpPost]
public IActionResult SubmitForm(FormModel model)
{
    // 处理表单
}
```

### 最佳实践

- 对所有用户输入进行上下文感知编码
- 实施严格的内容安全策略(CSP)
- 使用现代框架的自动转义功能
- 定期进行XSS漏洞扫描

### 参考资源

- [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) - XSS防护速查表
- [OWASP DOM-based XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html) - DOM型XSS防护速查表
- [OWASP Content Security Policy Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html) - CSP速查表

---

## 3. 命令执行修复

### 修复步骤

1. **避免使用系统命令**: 尽量使用编程语言原生API替代系统命令
2. **输入严格验证**: 使用白名单验证所有输入参数
3. **参数化命令**: 使用参数列表而非字符串拼接
4. **沙箱环境**: 在受限环境中执行命令
5. **禁用危险函数**: 配置PHP等语言的禁用函数列表

### 安全代码示例

#### Python
```python
import subprocess
import shlex
import re

# 不安全的代码
import os
filename = request.args.get('filename')
os.system(f"cat {filename}")  # 危险!

# 安全的代码 - 使用参数列表
def safe_file_read(filename):
    # 白名单验证
    if not re.match(r'^[a-zA-Z0-9_\.]+$', filename):
        raise ValueError("Invalid filename")
    
    try:
        result = subprocess.run(
            ['cat', filename],
            capture_output=True,
            text=True,
            timeout=5,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

# 避免shell=True
def list_directory(path):
    # 白名单验证路径
    allowed_paths = ['/tmp', '/var/log']
    if path not in allowed_paths:
        raise ValueError("Path not allowed")
    
    # 使用参数列表,不使用shell
    result = subprocess.run(
        ['ls', '-la', path],
        capture_output=True,
        text=True
    )
    return result.stdout
```

#### Java
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.List;
import java.util.regex.Pattern;

public class CommandExecution {
    private static final Pattern SAFE_FILENAME = Pattern.compile("^[a-zA-Z0-9_\\.]+$");
    private static final List<String> ALLOWED_COMMANDS = Arrays.asList("ls", "cat", "grep");
    
    public String safeCommandExecution(String filename) throws Exception {
        // 白名单验证
        if (!SAFE_FILENAME.matcher(filename).matches()) {
            throw new IllegalArgumentException("Invalid filename");
        }
        
        // 使用ProcessBuilder,避免shell解释器
        ProcessBuilder pb = new ProcessBuilder("cat", filename);
        pb.redirectErrorStream(true);
        
        Process process = pb.start();
        
        try (BufferedReader reader = new BufferedReader(
                new InputStreamReader(process.getInputStream()))) {
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            process.waitFor();
            return output.toString();
        }
    }
}
```

#### Go
```go
package main

import (
    "context"
    "os/exec"
    "regexp"
    "time"
)

var safeFilenamePattern = regexp.MustCompile(`^[a-zA-Z0-9_\.]+$`)

func safeCommandExecution(filename string) (string, error) {
    // 白名单验证
    if !safeFilenamePattern.MatchString(filename) {
        return "", errors.New("invalid filename")
    }
    
    // 使用context设置超时
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    // 使用参数列表,避免shell
    cmd := exec.CommandContext(ctx, "cat", filename)
    output, err := cmd.Output()
    if err != nil {
        return "", err
    }
    
    return string(output), nil
}

// 更安全:使用Go原生文件操作
func readFileNative(filename string) (string, error) {
    // 白名单验证
    if !safeFilenamePattern.MatchString(filename) {
        return "", errors.New("invalid filename")
    }
    
    data, err := os.ReadFile(filename)
    if err != nil {
        return "", err
    }
    
    return string(data), nil
}
```

#### PHP
```php
<?php
// 不安全的代码
$filename = $_GET['filename'];
system("cat " . $filename);  // 危险!
passthru("cat $filename");  // 危险!
exec("cat $filename");  // 危险!

// 安全的代码 - 使用escapeshellarg
function safeCommandExecution($filename) {
    // 白名单验证
    if (!preg_match('/^[a-zA-Z0-9_\.]+$/', $filename)) {
        throw new Exception("Invalid filename");
    }
    
    $escaped = escapeshellarg($filename);
    $output = shell_exec("cat " . $escaped);
    return $output;
}

// 更好的方案:避免使用系统命令
function readFileNative($filename) {
    // 白名单验证
    if (!preg_match('/^[a-zA-Z0-9_\.]+$/', $filename)) {
        throw new Exception("Invalid filename");
    }
    
    $allowed_dir = '/var/www/uploads/';
    $filepath = realpath($allowed_dir . $filename);
    
    // 确保文件在允许目录内
    if (strpos($filepath, realpath($allowed_dir)) !== 0) {
        throw new Exception("Access denied");
    }
    
    return file_get_contents($filepath);
}

// php.ini配置禁用危险函数
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source
?>
```

#### C#
```csharp
using System;
using System.Diagnostics;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

public class CommandExecution
{
    private static readonly Regex SafeFilenamePattern = new Regex(@"^[a-zA-Z0-9_\.]+$");
    
    public async Task<string> SafeCommandExecutionAsync(string filename)
    {
        // 白名单验证
        if (!SafeFilenamePattern.IsMatch(filename))
        {
            throw new ArgumentException("Invalid filename");
        }
        
        var processInfo = new ProcessStartInfo
        {
            FileName = "cat",
            Arguments = filename,  // 参数自动转义
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            UseShellExecute = false,  // 不使用shell
            CreateNoWindow = true
        };
        
        using (var process = new Process { StartInfo = processInfo })
        {
            process.Start();
            string output = await process.StandardOutput.ReadToEndAsync();
            await process.WaitForExitAsync();
            
            if (process.ExitCode != 0)
            {
                throw new Exception($"Command failed: {process.StandardError.ReadToEnd()}");
            }
            
            return output;
        }
    }
    
    // 更安全:使用.NET原生API
    public string ReadFileNative(string filename)
    {
        // 白名单验证
        if (!SafeFilenamePattern.IsMatch(filename))
        {
            throw new ArgumentException("Invalid filename");
        }
        
        string allowedPath = Path.GetFullPath(@"C:\allowed\path\");
        string fullPath = Path.GetFullPath(Path.Combine(allowedPath, filename));
        
        // 路径穿越检查
        if (!fullPath.StartsWith(allowedPath))
        {
            throw new UnauthorizedAccessException("Access denied");
        }
        
        return File.ReadAllText(fullPath);
    }
}
```

### 最佳实践

- 优先使用编程语言的原生API替代系统命令
- 对所有输入进行严格的白名单验证
- 禁用不必要的危险函数
- 在受限环境中运行外部命令

### 参考资源

- [OWASP Command Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) - 命令注入防护速查表

---

## 4. 反序列化漏洞修复

### 修复步骤

1. **避免反序列化不可信数据**: 尽量不反序列化来自用户的输入
2. **使用安全格式**: 使用JSON等简单数据格式替代原生序列化
3. **输入签名验证**: 对序列化数据进行数字签名验证
4. **类型白名单**: 实施严格的反序列化类型白名单
5. **隔离反序列化**: 在低权限环境中执行反序列化操作

### 安全代码示例

#### Python
```python
import json
import pickle
import hmac
import hashlib

# 不安全的代码
data = request.data
obj = pickle.loads(data)  # 危险!可能导致任意代码执行

# 安全的代码 - 使用JSON替代pickle
def safe_deserialize(json_data):
    try:
        return json.loads(json_data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON")

# 如果必须使用pickle,进行签名验证
SECRET_KEY = b'your-secret-key'

def serialize_signed(obj):
    pickled = pickle.dumps(obj)
    signature = hmac.new(SECRET_KEY, pickled, hashlib.sha256).hexdigest()
    return signature.encode() + b':' + pickled

def deserialize_signed(data):
    try:
        signature, pickled = data.split(b':', 1)
        expected = hmac.new(SECRET_KEY, pickled, hashlib.sha256).hexdigest()
        
        if not hmac.compare_digest(signature.decode(), expected):
            raise ValueError("Invalid signature")
        
        return pickle.loads(pickled)
    except Exception as e:
        raise ValueError(f"Deserialization failed: {e}")
```

#### Java
```java
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.DeserializationFeature;
import java.io.*;

public class DeserializationSecurity {
    
    // 不安全的代码
    public Object unsafeDeserialize(byte[] data) throws Exception {
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        return ois.readObject();  // 危险!
    }
    
    // 安全的代码 - 使用JSON替代Java序列化
    public <T> T safeDeserialize(String json, Class<T> clazz) throws Exception {
        ObjectMapper mapper = new ObjectMapper();
        // 禁用不安全的特性
        mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
        return mapper.readValue(json, clazz);
    }
    
    // 如果必须使用Java序列化,使用白名单
    public static class SafeObjectInputStream extends ObjectInputStream {
        private static final Set<String> ALLOWED_CLASSES = Set.of(
            "com.example.SafeClass1",
            "com.example.SafeClass2"
        );
        
        public SafeObjectInputStream(InputStream in) throws IOException {
            super(in);
        }
        
        @Override
        protected Class<?> resolveClass(ObjectStreamClass desc) 
                throws IOException, ClassNotFoundException {
            String className = desc.getName();
            if (!ALLOWED_CLASSES.contains(className)) {
                throw new InvalidClassException("Unauthorized deserialization", className);
            }
            return super.resolveClass(desc);
        }
    }
}
```

#### Go
```go
package main

import (
    "encoding/json"
    "errors"
)

// 不安全的代码 - 使用gob解码不可信数据
// dec := gob.NewDecoder(reader)
// dec.Decode(&obj)  // 危险!

// 安全的代码 - 使用JSON
type User struct {
    ID       int    `json:"id"`
    Username string `json:"username"`
    Email    string `json:"email"`
}

func safeDeserialize(data []byte) (*User, error) {
    var user User
    if err := json.Unmarshal(data, &user); err != nil {
        return nil, err
    }
    
    // 验证数据
    if user.Username == "" || user.Email == "" {
        return nil, errors.New("invalid user data")
    }
    
    return &user, nil
}

// 使用protobuf替代原生序列化
func deserializeWithProtobuf(data []byte) (*pb.User, error) {
    user := &pb.User{}
    if err := proto.Unmarshal(data, user); err != nil {
        return nil, err
    }
    return user, nil
}
```

#### PHP
```php
<?php
// 不安全的代码
$data = $_POST['data'];
$obj = unserialize($data);  // 危险!可能导致对象注入

// 安全的代码 - 使用JSON替代serialize
function safeDeserialize($json) {
    $data = json_decode($json, true);
    if (json_last_error() !== JSON_ERROR_NONE) {
        throw new Exception("Invalid JSON");
    }
    return $data;
}

// 如果必须使用unserialize,进行签名验证
function unserializeSigned($data, $secret) {
    list($signature, $serialized) = explode(':', $data, 2);
    
    $expected = hash_hmac('sha256', $serialized, $secret);
    if (!hash_equals($expected, $signature)) {
        throw new Exception("Invalid signature");
    }
    
    return unserialize($serialized);
}

// 使用允许的类白名单
function safeUnserialize($data) {
    $allowedClasses = ['SafeClass1', 'SafeClass2'];
    return unserialize($data, ['allowed_classes' => $allowedClasses]);
}
?>
```

#### C#
```csharp
using System;
using System.IO;
using System.Runtime.Serialization;
using System.Runtime.Serialization.Json;
using System.Text.Json;

public class DeserializationSecurity
{
    // 不安全的代码
    public object UnsafeDeserialize(byte[] data)
    {
        BinaryFormatter formatter = new BinaryFormatter();
        using (MemoryStream ms = new MemoryStream(data))
        {
            return formatter.Deserialize(ms);  // 危险!
        }
    }
    
    // 安全的代码 - 使用JSON
    public T SafeDeserialize<T>(string json)
    {
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        return JsonSerializer.Deserialize<T>(json, options);
    }
    
    // 使用DataContractSerializer并限制类型
    public object SafeDeserializeWithWhitelist(byte[] data)
    {
        var allowedTypes = new[] { typeof(SafeClass1), typeof(SafeClass2) };
        
        using (MemoryStream ms = new MemoryStream(data))
        {
            // 使用DataContractSerializer而不是BinaryFormatter
            DataContractSerializer serializer = new DataContractSerializer(
                typeof(object),
                allowedTypes
            );
            return serializer.ReadObject(ms);
        }
    }
}

// 完全禁用BinaryFormatter
[Obsolete("BinaryFormatter is insecure and should not be used.", error: true)]
public class SafeClass { }
```

### 最佳实践

- 绝不反序列化来自不可信来源的数据
- 使用JSON、XML等文本格式替代二进制序列化
- 如果必须使用二进制序列化,实施严格的类型白名单
- 对序列化数据进行数字签名

### 参考资源

- [OWASP Deserialization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html) - 反序列化防护速查表

---

## 5. 路径穿越修复

### 修复步骤

1. **路径规范化**: 使用API提供的规范化函数处理路径
2. **基目录验证**: 确保路径在允许的基目录范围内
3. **白名单验证**: 使用正则表达式验证文件名
4. **chroot jail**: 在隔离环境中运行文件操作
5. **间接映射**: 使用ID到文件名的映射,不直接使用用户输入作为文件名

### 安全代码示例

#### Python
```python
import os
import re
from pathlib import Path

# 不安全的代码
filename = request.args.get('filename')
filepath = '/var/www/files/' + filename
with open(filepath, 'r') as f:  # 危险!
    return f.read()

# 安全的代码
def safe_file_read(filename):
    base_dir = Path('/var/www/files').resolve()
    
    # 白名单验证
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', filename):
        raise ValueError("Invalid filename")
    
    # 路径规范化并验证
    file_path = (base_dir / filename).resolve()
    
    # 确保文件在基目录内
    if not str(file_path).startswith(str(base_dir)):
        raise ValueError("Access denied")
    
    # 检查是否为文件
    if not file_path.is_file():
        raise ValueError("Not a file")
    
    with open(file_path, 'r') as f:
        return f.read()

# 使用ID映射更安全的方案
FILE_MAP = {
    '1': 'document1.pdf',
    '2': 'document2.pdf'
}

def read_by_id(file_id):
    if file_id not in FILE_MAP:
        raise ValueError("Invalid file ID")
    
    filename = FILE_MAP[file_id]
    file_path = Path('/var/www/files') / filename
    
    with open(file_path, 'r') as f:
        return f.read()
```

#### Java
```java
import java.io.*;
import java.nio.file.*;
import java.util.regex.Pattern;

public class PathTraversalProtection {
    private static final Pattern SAFE_FILENAME = Pattern.compile("^[a-zA-Z0-9_\\-\\.]+$");
    private static final Path BASE_DIR = Paths.get("/var/www/files").toAbsolutePath().normalize();
    
    public String safeFileRead(String filename) throws IOException {
        // 白名单验证
        if (!SAFE_FILENAME.matcher(filename).matches()) {
            throw new IllegalArgumentException("Invalid filename");
        }
        
        // 路径规范化
        Path filePath = BASE_DIR.resolve(filename).normalize();
        
        // 验证路径在基目录内
        if (!filePath.startsWith(BASE_DIR)) {
            throw new SecurityException("Access denied");
        }
        
        // 安全检查
        if (!Files.exists(filePath) || !Files.isRegularFile(filePath)) {
            throw new FileNotFoundException("File not found");
        }
        
        return Files.readString(filePath);
    }
}
```

#### Go
```go
package main

import (
    "os"
    "path/filepath"
    "regexp"
    "strings"
)

var safeFilenamePattern = regexp.MustCompile(`^[a-zA-Z0-9_\-\.]+$`)

func safeFileRead(filename string) (string, error) {
    // 白名单验证
    if !safeFilenamePattern.MatchString(filename) {
        return "", errors.New("invalid filename")
    }
    
    // 获取绝对路径
    baseDir, _ := filepath.Abs("/var/www/files")
    filePath := filepath.Join(baseDir, filename)
    
    // 规范化路径
    cleanPath := filepath.Clean(filePath)
    
    // 验证路径在基目录内
    if !strings.HasPrefix(cleanPath, baseDir) {
        return "", errors.New("access denied")
    }
    
    // 读取文件
    data, err := os.ReadFile(cleanPath)
    if err != nil {
        return "", err
    }
    
    return string(data), nil
}
```

#### PHP
```php
<?php
// 不安全的代码
$filename = $_GET['filename'];
$content = file_get_contents('/var/www/files/' . $filename);  // 危险!

// 安全的代码
function safeFileRead($filename) {
    $baseDir = realpath('/var/www/files');
    
    // 白名单验证
    if (!preg_match('/^[a-zA-Z0-9_\-\.]+$/', $filename)) {
        throw new Exception("Invalid filename");
    }
    
    // 构建并规范化路径
    $filePath = realpath($baseDir . '/' . $filename);
    
    // 验证路径在基目录内
    if ($filePath === false || strpos($filePath, $baseDir) !== 0) {
        throw new Exception("Access denied");
    }
    
    // 安全检查
    if (!is_file($filePath)) {
        throw new Exception("Not a file");
    }
    
    return file_get_contents($filePath);
}

// ID映射方案
$fileMap = [
    '1' => 'document1.pdf',
    '2' => 'document2.pdf'
];

function readById($fileId) {
    global $fileMap;
    
    if (!isset($fileMap[$fileId])) {
        throw new Exception("Invalid file ID");
    }
    
    $filename = $fileMap[$fileId];
    $filePath = '/var/www/files/' . $filename;
    
    return file_get_contents($filePath);
}
?>
```

#### C#
```csharp
using System;
using System.IO;
using System.Text.RegularExpressions;

public class PathTraversalProtection
{
    private static readonly Regex SafeFilenamePattern = new Regex(@"^[a-zA-Z0-9_\-\.]+$");
    private static readonly string BaseDir = Path.GetFullPath(@"C:\var\www\files");
    
    public string SafeFileRead(string filename)
    {
        // 白名单验证
        if (!SafeFilenamePattern.IsMatch(filename))
        {
            throw new ArgumentException("Invalid filename");
        }
        
        // 构建完整路径
        string filePath = Path.GetFullPath(Path.Combine(BaseDir, filename));
        
        // 验证路径在基目录内
        if (!filePath.StartsWith(BaseDir, StringComparison.OrdinalIgnoreCase))
        {
            throw new UnauthorizedAccessException("Access denied");
        }
        
        // 安全检查
        if (!File.Exists(filePath))
        {
            throw new FileNotFoundException("File not found");
        }
        
        return File.ReadAllText(filePath);
    }
    
    // ID映射方案
    private static readonly Dictionary<string, string> FileMap = new Dictionary<string, string>
    {
        { "1", "document1.pdf" },
        { "2", "document2.pdf" }
    };
    
    public string ReadById(string fileId)
    {
        if (!FileMap.TryGetValue(fileId, out string filename))
        {
            throw new ArgumentException("Invalid file ID");
        }
        
        string filePath = Path.Combine(BaseDir, filename);
        return File.ReadAllText(filePath);
    }
}
```

### 最佳实践

- 使用ID到文件名的间接映射
- 永远不要直接使用用户输入作为文件名
- 使用规范化后的路径进行验证
- 设置严格的文件系统权限

### 参考资源

- [OWASP Path Traversal Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Path_Traversal_Prevention_Cheat_Sheet.html) - 路径穿越防护速查表

---

## 6. SSRF修复

### 修复步骤

1. **URL解析验证**: 解析URL并验证所有组成部分
2. **IP黑名单**: 阻止访问内网IP和保留地址
3. **DNS重绑定防护**: 解析IP并在请求时验证
4. **协议白名单**: 只允许HTTP/HTTPS协议
5. **响应限制**: 限制响应大小和超时时间

### 安全代码示例

#### Python
```python
import ipaddress
import re
import socket
import urllib.parse
import requests

def is_private_ip(ip_str):
    """检查是否为内网IP"""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_reserved
    except ValueError:
        return True

def safe_url_fetch(url):
    # 解析URL
    parsed = urllib.parse.urlparse(url)
    
    # 协议白名单
    if parsed.scheme not in ['http', 'https']:
        raise ValueError("Only HTTP/HTTPS allowed")
    
    # 获取主机名
    hostname = parsed.hostname
    if not hostname:
        raise ValueError("Invalid URL")
    
    # 解析IP
    try:
        ip = socket.getaddrinfo(hostname, None)[0][4][0]
    except socket.gaierror:
        raise ValueError("Could not resolve hostname")
    
    # 检查是否为内网IP
    if is_private_ip(ip):
        raise ValueError("Access to internal resources denied")
    
    # 使用超时和限制响应大小
    response = requests.get(
        url,
        timeout=5,
        stream=True,
        allow_redirects=False  # 禁用重定向
    )
    
    # 限制响应大小
    content = b''
    for chunk in response.iter_content(chunk_size=8192):
        content += chunk
        if len(content) > 1024 * 1024:  # 1MB限制
            raise ValueError("Response too large")
    
    return content

# 使用白名单模式
def fetch_from_whitelist(url):
    allowed_domains = [
        'api.example.com',
        'cdn.example.com'
    ]
    
    parsed = urllib.parse.urlparse(url)
    if parsed.hostname not in allowed_domains:
        raise ValueError("Domain not in whitelist")
    
    return requests.get(url, timeout=5).content
```

#### Java
```java
import java.net.*;
import java.util.Arrays;
import java.util.List;

public class SSRFProtection {
    
    private static final List<String> BLOCKED_SCHEMES = Arrays.asList("file", "ftp", "gopher");
    private static final List<String> ALLOWED_DOMAINS = Arrays.asList(
        "api.example.com",
        "cdn.example.com"
    );
    
    public String safeFetch(String urlString) throws Exception {
        URL url = new URL(urlString);
        
        // 协议检查
        String scheme = url.getProtocol();
        if (BLOCKED_SCHEMES.contains(scheme)) {
            throw new SecurityException("Scheme not allowed");
        }
        
        // 域名白名单检查
        String host = url.getHost();
        if (!ALLOWED_DOMAINS.contains(host)) {
            throw new SecurityException("Domain not in whitelist");
        }
        
        // 解析IP并检查
        InetAddress address = InetAddress.getByName(host);
        if (address.isLoopbackAddress() || address.isSiteLocalAddress()) {
            throw new SecurityException("Access to internal addresses denied");
        }
        
        // 建立连接并设置超时
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setConnectTimeout(5000);
        conn.setReadTimeout(5000);
        conn.setInstanceFollowRedirects(false);
        
        // 限制响应大小
        conn.setRequestProperty("Range", "bytes=0-1048575");  // 1MB限制
        
        try (InputStream is = conn.getInputStream()) {
            return new String(is.readAllBytes(), StandardCharsets.UTF_8);
        }
    }
}
```

#### Go
```go
package main

import (
    "context"
    "errors"
    "io"
    "net"
    "net/http"
    "net/url"
    "time"
)

var allowedDomains = []string{
    "api.example.com",
    "cdn.example.com",
}

func isPrivateIP(ip net.IP) bool {
    return ip.IsLoopback() || ip.IsPrivate() || ip.IsLinkLocalUnicast()
}

func safeFetch(targetURL string) ([]byte, error) {
    // 解析URL
    u, err := url.Parse(targetURL)
    if err != nil {
        return nil, err
    }
    
    // 协议检查
    if u.Scheme != "http" && u.Scheme != "https" {
        return nil, errors.New("only HTTP/HTTPS allowed")
    }
    
    // 域名白名单检查
    allowed := false
    for _, domain := range allowedDomains {
        if u.Hostname() == domain {
            allowed = true
            break
        }
    }
    if !allowed {
        return nil, errors.New("domain not in whitelist")
    }
    
    // 解析IP并检查
    ips, err := net.LookupIP(u.Hostname())
    if err != nil {
        return nil, err
    }
    
    for _, ip := range ips {
        if isPrivateIP(ip) {
            return nil, errors.New("access to internal addresses denied")
        }
    }
    
    // 创建带超时的客户端
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()
    
    req, err := http.NewRequestWithContext(ctx, "GET", targetURL, nil)
    if err != nil {
        return nil, err
    }
    
    client := &http.Client{
        CheckRedirect: func(req *http.Request, via []*http.Request) error {
            return http.ErrUseLastResponse  // 禁用重定向
        },
    }
    
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    // 限制响应大小
    return io.ReadAll(io.LimitReader(resp.Body, 1024*1024))  // 1MB限制
}
```

#### PHP
```php
<?php
// 不安全的代码
$url = $_GET['url'];
$content = file_get_contents($url);  // 危险!

// 安全的代码
function safeFetch($url) {
    $allowedDomains = ['api.example.com', 'cdn.example.com'];
    
    // 解析URL
    $parsed = parse_url($url);
    
    // 协议检查
    if (!in_array($parsed['scheme'], ['http', 'https'])) {
        throw new Exception("Only HTTP/HTTPS allowed");
    }
    
    // 域名白名单
    if (!in_array($parsed['host'], $allowedDomains)) {
        throw new Exception("Domain not in whitelist");
    }
    
    // 解析IP
    $ips = gethostbynamel($parsed['host']);
    foreach ($ips as $ip) {
        // 检查内网IP
        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE) === false) {
            throw new Exception("Access to internal addresses denied");
        }
    }
    
    // 使用cURL并设置限制
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 5);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, false);  // 禁用重定向
    curl_setopt($ch, CURLOPT_PROTOCOLS, CURLPROTO_HTTP | CURLPROTO_HTTPS);
    
    $content = curl_exec($ch);
    curl_close($ch);
    
    return $content;
}
?>
```

#### C#
```csharp
using System;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;

public class SSRFProtection
{
    private static readonly string[] AllowedDomains = {
        "api.example.com",
        "cdn.example.com"
    };
    
    public async Task<string> SafeFetchAsync(string urlString)
    {
        // 解析URL
        if (!Uri.TryCreate(urlString, UriKind.Absolute, out Uri url))
        {
            throw new ArgumentException("Invalid URL");
        }
        
        // 协议检查
        if (url.Scheme != "http" && url.Scheme != "https")
        {
            throw new SecurityException("Only HTTP/HTTPS allowed");
        }
        
        // 域名白名单
        if (!AllowedDomains.Contains(url.Host))
        {
            throw new SecurityException("Domain not in whitelist");
        }
        
        // 解析IP并检查
        var addresses = await Dns.GetHostAddressesAsync(url.Host);
        foreach (var ip in addresses)
        {
            if (IPAddress.IsLoopback(ip) || ip.ToString().StartsWith("10.") ||
                ip.ToString().StartsWith("192.168.") || ip.ToString().StartsWith("172."))
            {
                throw new SecurityException("Access to internal addresses denied");
            }
        }
        
        // 创建带限制的HttpClient
        var handler = new HttpClientHandler
        {
            AllowAutoRedirect = false,  // 禁用重定向
            MaxResponseContentBufferSize = 1024 * 1024  // 1MB限制
        };
        
        using (var client = new HttpClient(handler))
        {
            client.Timeout = TimeSpan.FromSeconds(5);
            
            var response = await client.GetAsync(url);
            return await response.Content.ReadAsStringAsync();
        }
    }
}
```

### 最佳实践

- 使用域名白名单而非黑名单
- 禁用自动重定向
- 解析URL后验证目标IP
- 限制响应大小和请求超时

### 参考资源

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) - SSRF防护速查表

---

## 7. XXE修复

### 修复步骤

1. **禁用DTD**: 禁用XML文档类型定义处理
2. **禁用外部实体**: 禁止解析外部实体
3. **使用简单数据格式**: 优先使用JSON替代XML
4. **输入验证**: 验证XML内容符合预期模式
5. **升级解析器**: 使用最新版本的XML解析库

### 安全代码示例

#### Python
```python
from xml.etree import ElementTree as ET
from defusedxml import ElementTree as DefusedET
import lxml.etree as LET

# 不安全的代码 - 使用标准库
tree = ET.parse(xml_file)  # 危险!易受XXE攻击

# 安全的代码 - 使用defusedxml
# 安装: pip install defusedxml
def safe_xml_parse(xml_string):
    try:
        root = DefusedET.fromstring(xml_string)
        return root
    except DefusedET.DefusedXmlException as e:
        raise ValueError(f"XML parsing error: {e}")

# 使用lxml并禁用外部实体
def safe_lxml_parse(xml_string):
    parser = LET.XMLParser(
        resolve_entities=False,  # 禁用实体解析
        no_network=True,         # 禁用网络访问
        load_dtd=False           # 不加载DTD
    )
    root = LET.fromstring(xml_string, parser=parser)
    return root
```

#### Java
```java
import javax.xml.parsers.*;
import org.xml.sax.InputSource;
import java.io.StringReader;

public class XXEProtection {
    
    public Document safeXmlParse(String xml) throws Exception {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        
        // 禁用DTD
        dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        
        // 禁用外部实体
        dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        
        // 禁用外部DTD
        dbf.setFeature("http://apache.org/xml/features/nonvalidating/load-external-dtd", false);
        
        // 禁用XInclude
        dbf.setXIncludeAware(false);
        dbf.setExpandEntityReferences(false);
        
        DocumentBuilder db = dbf.newDocumentBuilder();
        return db.parse(new InputSource(new StringReader(xml)));
    }
    
    // 使用SAXParser
    public void safeSaxParse(String xml) throws Exception {
        SAXParserFactory spf = SAXParserFactory.newInstance();
        spf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
        spf.setFeature("http://xml.org/sax/features/external-general-entities", false);
        spf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
        
        SAXParser parser = spf.newSAXParser();
        // 解析...
    }
}
```

#### Go
```go
package main

import (
    "encoding/xml"
    "strings"
)

// Go的encoding/xml默认不解析外部实体,相对安全
// 但仍需谨慎使用

type User struct {
    XMLName xml.Name `xml:"user"`
    Name    string   `xml:"name"`
    Email   string   `xml:"email"`
}

func safeXMLParse(xmlData string) (*User, error) {
    var user User
    decoder := xml.NewDecoder(strings.NewReader(xmlData))
    
    // Go的xml.Decoder默认不处理外部实体
    // 但需要确保使用的是encoding/xml而非第三方库
    
    if err := decoder.Decode(&user); err != nil {
        return nil, err
    }
    
    return &user, nil
}

// 更好的方案:使用JSON替代XML
func safeJSONParse(jsonData string) (*User, error) {
    var user User
    if err := json.Unmarshal([]byte(jsonData), &user); err != nil {
        return nil, err
    }
    return &user, nil
}
```

#### PHP
```php
<?php
// 不安全的代码
$xml = file_get_contents('php://input');
$doc = simplexml_load_string($xml);  // 危险!默认允许外部实体

// 安全的代码 - 禁用外部实体
libxml_disable_entity_loader(true);
$doc = simplexml_load_string($xml);

// 或使用DOMDocument并禁用
$dom = new DOMDocument();
$dom->loadXML($xml, LIBXML_NONET | LIBXML_DTDLOAD | LIBXML_DTDATTR | LIBXML_NOENT);
// 注意:上述选项在生产环境中应禁用

// 更安全的DOMDocument配置
$dom = new DOMDocument();
$previousValue = libxml_disable_entity_loader(true);
$dom->loadXML($xml, LIBXML_NONET);
libxml_disable_entity_loader($previousValue);

// PHP 8.0+中libxml_disable_entity_loader已废弃
// 建议使用以下方式:
$dom = new DOMDocument();
$dom->loadXML($xml, LIBXML_NONET | LIBXML_NOENT | LIBXML_DTDLOAD | LIBXML_NOERROR | LIBXML_NOWARNING);
?>
```

#### C#
```csharp
using System;
using System.Xml;
using System.Xml.Linq;

public class XXEProtection
{
    public XmlDocument SafeXmlParse(string xml)
    {
        XmlDocument doc = new XmlDocument();
        
        // 禁用DTD处理
        doc.XmlResolver = null;
        
        // 或使用XmlReaderSettings
        XmlReaderSettings settings = new XmlReaderSettings
        {
            DtdProcessing = DtdProcessing.Prohibit,  // 禁止DTD
            XmlResolver = null,                       // 禁用XML解析器
            MaxCharactersFromEntities = 1024          // 限制实体扩展
        };
        
        using (XmlReader reader = XmlReader.Create(new StringReader(xml), settings))
        {
            doc.Load(reader);
        }
        
        return doc;
    }
    
    // 使用LINQ to XML (更安全)
    public XDocument SafeXDocumentParse(string xml)
    {
        // LINQ to XML默认禁用DTD
        return XDocument.Parse(xml);
    }
}
```

### 最佳实践

- 使用JSON替代XML
- 完全禁用DTD处理
- 禁用所有外部实体
- 使用最新的XML解析库

### 参考资源

- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) - XXE防护速查表

---

## 8. 鉴权缺陷修复

### 修复步骤

1. **实施MFA**: 使用多因素认证
2. **强密码策略**: 强制使用复杂密码并定期更换
3. **会话管理**: 使用安全的会话令牌,设置合理的过期时间
4. **JWT安全**: 使用强签名算法,验证所有声明
5. **速率限制**: 对登录和敏感操作实施速率限制

### 安全代码示例

#### Python
```python
import bcrypt
import jwt
import secrets
from datetime import datetime, timedelta
from flask_limiter import Limiter

# 密码哈希
class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed.encode())

# 安全的JWT实现
class JWTManager:
    SECRET_KEY = secrets.token_urlsafe(32)  # 随机密钥
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE = timedelta(days=7)
    
    @classmethod
    def create_tokens(cls, user_id: str):
        now = datetime.utcnow()
        
        access_payload = {
            'sub': user_id,
            'iat': now,
            'exp': now + cls.ACCESS_TOKEN_EXPIRE,
            'type': 'access'
        }
        
        refresh_payload = {
            'sub': user_id,
            'iat': now,
            'exp': now + cls.REFRESH_TOKEN_EXPIRE,
            'type': 'refresh'
        }
        
        access_token = jwt.encode(access_payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        refresh_token = jwt.encode(refresh_payload, cls.SECRET_KEY, algorithm=cls.ALGORITHM)
        
        return access_token, refresh_token
    
    @classmethod
    def verify_token(cls, token: str, token_type: str = 'access'):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            if payload.get('type') != token_type:
                raise ValueError("Invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

# 速率限制
limiter = Limiter(
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # 登录逻辑
    pass
```

#### Java
```java
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import io.jsonwebtoken.*;
import java.util.Date;
import java.util.concurrent.TimeUnit;
import com.github.benmanes.caffeine.cache.Cache;
import com.github.benmanes.caffeine.cache.Caffeine;

@Component
public class AuthenticationService {
    
    private final BCryptPasswordEncoder passwordEncoder = new BCryptPasswordEncoder(12);
    private final String SECRET_KEY = generateSecureKey();
    
    // 登录失败缓存(速率限制)
    private final Cache<String, Integer> loginAttempts = Caffeine.newBuilder()
        .expireAfterWrite(15, TimeUnit.MINUTES)
        .build();
    
    public String hashPassword(String password) {
        return passwordEncoder.encode(password);
    }
    
    public boolean verifyPassword(String password, String hashed) {
        return passwordEncoder.matches(password, hashed);
    }
    
    public String generateToken(String userId) {
        Date now = new Date();
        Date expiry = new Date(now.getTime() + 900000);  // 15分钟
        
        return Jwts.builder()
            .setSubject(userId)
            .setIssuedAt(now)
            .setExpiration(expiry)
            .signWith(SignatureAlgorithm.HS256, SECRET_KEY)
            .compact();
    }
    
    public Claims verifyToken(String token) {
        try {
            return Jwts.parser()
                .setSigningKey(SECRET_KEY)
                .parseClaimsJws(token)
                .getBody();
        } catch (ExpiredJwtException e) {
            throw new AuthenticationException("Token expired");
        } catch (JwtException e) {
            throw new AuthenticationException("Invalid token");
        }
    }
    
    public boolean checkLoginAttempts(String username) {
        Integer attempts = loginAttempts.getIfPresent(username);
        if (attempts != null && attempts >= 5) {
            return false;  // 超过限制
        }
        return true;
    }
    
    public void recordFailedAttempt(String username) {
        loginAttempts.put(username, loginAttempts.get(username, k -> 0) + 1);
    }
    
    private String generateSecureKey() {
        byte[] key = new byte[32];
        new SecureRandom().nextBytes(key);
        return Base64.getEncoder().encodeToString(key);
    }
}
```

#### Go
```go
package main

import (
    "errors"
    "time"
    
    "github.com/golang-jwt/jwt/v5"
    "golang.org/x/crypto/bcrypt"
)

// 密码管理
type PasswordManager struct{}

func (pm *PasswordManager) HashPassword(password string) (string, error) {
    bytes, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
    return string(bytes), err
}

func (pm *PasswordManager) VerifyPassword(password, hash string) bool {
    err := bcrypt.CompareHashAndPassword([]byte(hash), []byte(password))
    return err == nil
}

// JWT管理
type JWTManager struct {
    secretKey     []byte
    tokenDuration time.Duration
}

func NewJWTManager(secretKey string, tokenDuration time.Duration) *JWTManager {
    return &JWTManager{
        secretKey:     []byte(secretKey),
        tokenDuration: tokenDuration,
    }
}

func (jm *JWTManager) Generate(userID string) (string, error) {
    claims := jwt.MapClaims{
        "sub": userID,
        "iat": time.Now().Unix(),
        "exp": time.Now().Add(jm.tokenDuration).Unix(),
    }
    
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
    return token.SignedString(jm.secretKey)
}

func (jm *JWTManager) Verify(tokenString string) (*jwt.Token, error) {
    token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        // 验证签名算法
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
            return nil, errors.New("unexpected signing method")
        }
        return jm.secretKey, nil
    })
    
    if err != nil {
        return nil, err
    }
    
    if !token.Valid {
        return nil, errors.New("invalid token")
    }
    
    return token, nil
}
```

#### PHP
```php
<?php
// 密码哈希
function hashPassword($password) {
    return password_hash($password, PASSWORD_ARGON2ID, [
        'memory_cost' => 65536,
        'time_cost' => 4,
        'threads' => 3
    ]);
}

function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

// JWT实现 (使用firebase/php-jwt)
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class JWTManager {
    private static $secretKey;
    private static $algorithm = 'HS256';
    
    public static function init($secret) {
        self::$secretKey = $secret;
    }
    
    public static function generateToken($userId) {
        $issuedAt = time();
        $expirationTime = $issuedAt + 900;  // 15分钟
        
        $payload = [
            'iat' => $issuedAt,
            'exp' => $expirationTime,
            'sub' => $userId
        ];
        
        return JWT::encode($payload, self::$secretKey, self::$algorithm);
    }
    
    public static function verifyToken($token) {
        try {
            $decoded = JWT::decode($token, new Key(self::$secretKey, self::$algorithm));
            return (array) $decoded;
        } catch (Exception $e) {
            throw new Exception("Invalid token: " . $e->getMessage());
        }
    }
}

// 速率限制 (使用Redis)
function checkLoginAttempts($username) {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    
    $key = "login_attempts:$username";
    $attempts = $redis->get($key);
    
    if ($attempts >= 5) {
        return false;
    }
    
    return true;
}

function recordFailedAttempt($username) {
    $redis = new Redis();
    $redis->connect('127.0.0.1', 6379);
    
    $key = "login_attempts:$username";
    $redis->incr($key);
    $redis->expire($key, 900);  // 15分钟
}
?>
```

#### C#
```csharp
using System;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;

public class AuthenticationService
{
    private readonly PasswordHasher<object> _passwordHasher = new PasswordHasher<object>();
    private readonly string _secretKey;
    
    public AuthenticationService()
    {
        _secretKey = Convert.ToBase64String(RandomNumberGenerator.GetBytes(32));
    }
    
    public string HashPassword(string password)
    {
        return _passwordHasher.HashPassword(null, password);
    }
    
    public bool VerifyPassword(string password, string hashedPassword)
    {
        var result = _passwordHasher.VerifyHashedPassword(null, hashedPassword, password);
        return result == PasswordVerificationResult.Success;
    }
    
    public string GenerateToken(string userId)
    {
        var securityKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey));
        var credentials = new SigningCredentials(securityKey, SecurityAlgorithms.HmacSha256);
        
        var claims = new[]
        {
            new Claim(JwtRegisteredClaimNames.Sub, userId),
            new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            new Claim(JwtRegisteredClaimNames.Iat, DateTimeOffset.UtcNow.ToUnixTimeSeconds().ToString())
        };
        
        var token = new JwtSecurityToken(
            claims: claims,
            expires: DateTime.Now.AddMinutes(15),
            signingCredentials: credentials
        );
        
        return new JwtSecurityTokenHandler().WriteToken(token);
    }
    
    public ClaimsPrincipal VerifyToken(string token)
    {
        var tokenHandler = new JwtSecurityTokenHandler();
        var validationParameters = new TokenValidationParameters
        {
            ValidateIssuerSigningKey = true,
            IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_secretKey)),
            ValidateIssuer = false,
            ValidateAudience = false,
            ClockSkew = TimeSpan.Zero
        };
        
        try
        {
            return tokenHandler.ValidateToken(token, validationParameters, out _);
        }
        catch (SecurityTokenExpiredException)
        {
            throw new UnauthorizedAccessException("Token expired");
        }
        catch (SecurityTokenException)
        {
            throw new UnauthorizedAccessException("Invalid token");
        }
    }
}

// ASP.NET Core速率限制
builder.Services.AddRateLimiter(options =>
{
    options.AddPolicy("login", context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.Connection.RemoteIpAddress?.ToString(),
            factory: _ => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 5,
                Window = TimeSpan.FromMinutes(1)
            }));
});
```

### 最佳实践

- 使用bcrypt、Argon2等现代密码哈希算法
- 实施JWT短有效期+刷新令牌机制
- 对敏感操作实施多因素认证
- 实施严格的速率限制

### 参考资源

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) - 认证速查表
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) - 会话管理速查表
- [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - 密码存储速查表
- [OWASP JWT Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html) - JWT安全速查表

---

## 9. 硬编码密钥修复

### 修复步骤

1. **使用密钥管理服务**: 使用AWS KMS、Azure Key Vault、HashiCorp Vault等
2. **环境变量**: 将密钥存储在环境变量而非代码中
3. **配置文件加密**: 加密配置文件中的敏感信息
4. **密钥轮换**: 定期轮换密钥和凭据
5. **秘密扫描**: 使用工具扫描代码中的硬编码密钥

### 安全代码示例

#### Python
```python
import os
from cryptography.fernet import Fernet
import boto3
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# 从环境变量读取
DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
API_KEY = os.environ.get('API_KEY')

# AWS Secrets Manager
def get_secret_from_aws(secret_name):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return response['SecretString']

# Azure Key Vault
def get_secret_from_azure(vault_url, secret_name):
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)
    secret = client.get_secret(secret_name)
    return secret.value

# HashiCorp Vault
def get_secret_from_vault(path):
    import hvac
    client = hvac.Client(url='https://vault.example.com')
    client.auth.approle.login(
        role_id=os.environ['VAULT_ROLE_ID'],
        secret_id=os.environ['VAULT_SECRET_ID']
    )
    secret = client.secrets.kv.v2.read_secret_version(path=path)
    return secret['data']['data']

# 加密配置文件示例
class EncryptedConfig:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def encrypt_value(self, value):
        return self.cipher.encrypt(value.encode()).decode()
    
    def decrypt_value(self, encrypted):
        return self.cipher.decrypt(encrypted.encode()).decode()
```

#### Java
```java
import software.amazon.awsservices.secretsmanager.*;
import software.amazon.awsservices.secretsmanager.model.*;
import com.azure.security.keyvault.secrets.SecretClient;
import com.azure.security.keyvault.secrets.SecretClientBuilder;
import com.azure.identity.DefaultAzureCredentialBuilder;
import org.springframework.vault.core.VaultTemplate;
import org.springframework.vault.support.VaultResponse;

@Component
public class SecretManager {
    
    // AWS Secrets Manager
    public String getSecretFromAWS(String secretName) {
        SecretsManagerClient client = SecretsManagerClient.builder()
            .region(Region.US_EAST_1)
            .build();
        
        GetSecretValueRequest request = GetSecretValueRequest.builder()
            .secretId(secretName)
            .build();
        
        GetSecretValueResponse response = client.getSecretValue(request);
        return response.secretString();
    }
    
    // Azure Key Vault
    public String getSecretFromAzure(String vaultUrl, String secretName) {
        SecretClient secretClient = new SecretClientBuilder()
            .vaultUrl(vaultUrl)
            .credential(new DefaultAzureCredentialBuilder().build())
            .buildClient();
        
        return secretClient.getSecret(secretName).getValue();
    }
    
    // HashiCorp Vault
    @Autowired
    private VaultTemplate vaultTemplate;
    
    public String getSecretFromVault(String path) {
        VaultResponse response = vaultTemplate.read(path);
        return (String) response.getData().get("value");
    }
}

// 从环境变量读取
@Configuration
public class AppConfig {
    
    @Value("${DATABASE_PASSWORD}")
    private String databasePassword;
    
    @Value("${API_KEY}")
    private String apiKey;
    
    // 使用...
}
```

#### Go
```go
package main

import (
    "context"
    "os"
    
    "github.com/aws/aws-sdk-go-v2/aws"
    "github.com/aws/aws-sdk-go-v2/config"
    "github.com/aws/aws-sdk-go-v2/service/secretsmanager"
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/Azure/azure-sdk-for-go/sdk/security/keyvault/azsecrets"
    vault "github.com/hashicorp/vault/api"
)

// 从环境变量读取
func getEnvOrPanic(key string) string {
    value := os.Getenv(key)
    if value == "" {
        panic("Environment variable " + key + " is not set")
    }
    return value
}

// AWS Secrets Manager
func getSecretFromAWS(secretName string) (string, error) {
    cfg, err := config.LoadDefaultConfig(context.Background())
    if err != nil {
        return "", err
    }
    
    client := secretsmanager.NewFromConfig(cfg)
    result, err := client.GetSecretValue(context.Background(), &secretsmanager.GetSecretValueInput{
        SecretId: aws.String(secretName),
    })
    if err != nil {
        return "", err
    }
    
    return *result.SecretString, nil
}

// Azure Key Vault
func getSecretFromAzure(vaultURL, secretName string) (string, error) {
    credential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        return "", err
    }
    
    client, err := azsecrets.NewClient(vaultURL, credential, nil)
    if err != nil {
        return "", err
    }
    
    resp, err := client.GetSecret(context.Background(), secretName, "", nil)
    if err != nil {
        return "", err
    }
    
    return *resp.Value, nil
}

// HashiCorp Vault
func getSecretFromVault(path string) (string, error) {
    config := vault.DefaultConfig()
    config.Address = os.Getenv("VAULT_ADDR")
    
    client, err := vault.NewClient(config)
    if err != nil {
        return "", err
    }
    
    client.SetToken(os.Getenv("VAULT_TOKEN"))
    
    secret, err := client.KVv2("secret").Get(context.Background(), path)
    if err != nil {
        return "", err
    }
    
    value, ok := secret.Data["value"].(string)
    if !ok {
        return "", errors.New("secret not found")
    }
    
    return value, nil
}
```

#### PHP
```php
<?php
// 从环境变量读取
$databasePassword = getenv('DATABASE_PASSWORD') ?: die('DATABASE_PASSWORD not set');
$apiKey = getenv('API_KEY') ?: die('API_KEY not set');

// AWS Secrets Manager
use Aws\SecretsManager\SecretsManagerClient;

function getSecretFromAWS($secretName) {
    $client = new SecretsManagerClient([
        'version' => 'latest',
        'region' => 'us-east-1'
    ]);
    
    $result = $client->getSecretValue(['SecretId' => $secretName]);
    return $result['SecretString'];
}

// Azure Key Vault
function getSecretFromAzure($vaultName, $secretName) {
    $credential = new DefaultAzureCredential();
    $client = new SecretClient(
        "https://$vaultName.vault.azure.net",
        $credential
    );
    
    $secret = $client->getSecret($secretName);
    return $secret->getValue();
}

// HashiCorp Vault
function getSecretFromVault($path) {
    $client = new VaultClient([
        'base_uri' => getenv('VAULT_ADDR'),
        'headers' => [
            'X-Vault-Token' => getenv('VAULT_TOKEN')
        ]
    ]);
    
    $response = $client->get("/v1/secret/data/$path");
    $data = json_decode($response->getBody(), true);
    return $data['data']['data']['value'];
}
?>
```

#### C#
```csharp
using Amazon.SecretsManager;
using Amazon.SecretsManager.Model;
using Azure.Identity;
using Azure.Security.KeyVault.Secrets;
using VaultSharp;
using VaultSharp.V1.AuthMethods.AppRole;

public class SecretManager
{
    // AWS Secrets Manager
    public async Task<string> GetSecretFromAWSAsync(string secretName)
    {
        var client = new AmazonSecretsManagerClient();
        var request = new GetSecretValueRequest { SecretId = secretName };
        var response = await client.GetSecretValueAsync(request);
        return response.SecretString;
    }
    
    // Azure Key Vault
    public string GetSecretFromAzure(string vaultUrl, string secretName)
    {
        var client = new SecretClient(
            new Uri(vaultUrl),
            new DefaultAzureCredential()
        );
        
        var secret = client.GetSecret(secretName);
        return secret.Value.Value;
    }
    
    // HashiCorp Vault
    public async Task<string> GetSecretFromVaultAsync(string path)
    {
        var authMethod = new AppRoleAuthMethodInfo(
            Environment.GetEnvironmentVariable("VAULT_ROLE_ID"),
            Environment.GetEnvironmentVariable("VAULT_SECRET_ID")
        );
        
        var vaultClientSettings = new VaultClientSettings(
            Environment.GetEnvironmentVariable("VAULT_ADDR"),
            authMethod
        );
        
        var vaultClient = new VaultClient(vaultClientSettings);
        var secret = await vaultClient.V1.Secrets.KeyValue.V2.ReadSecretAsync(path);
        return secret.Data.Data["value"].ToString();
    }
}

// 从环境变量读取
public class AppSettings
{
    public string DatabasePassword { get; set; } = 
        Environment.GetEnvironmentVariable("DATABASE_PASSWORD") 
        ?? throw new InvalidOperationException("DATABASE_PASSWORD not set");
    
    public string ApiKey { get; set; } = 
        Environment.GetEnvironmentVariable("API_KEY") 
        ?? throw new InvalidOperationException("API_KEY not set");
}
```

### 最佳实践

- 永远不要将密钥提交到版本控制系统
- 使用.gitignore排除包含密钥的配置文件
- 使用密钥管理服务的自动轮换功能
- 实施最小权限原则,限制密钥访问范围
- 定期审计密钥使用情况

### 参考资源

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) - 密钥管理速查表
- [OWASP Key Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Key_Management_Cheat_Sheet.html) - 密钥管理速查表

---

## 综合参考资源

### OWASP Cheat Sheets (中文描述)

| 英文链接 | 中文描述 |
|---------|---------|
| [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html) | SQL注入防护完整指南,包含所有主流语言的参数化查询示例 |
| [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html) | 跨站脚本攻击防护指南,包含上下文感知编码方法 |
| [OS Command Injection Defense](https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html) | 操作系统命令注入防护指南 |
| [Deserialization](https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html) | 反序列化漏洞防护指南,包含各语言安全实践 |
| [Path Traversal Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Path_Traversal_Prevention_Cheat_Sheet.html) | 路径穿越攻击防护指南 |
| [SSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) | 服务器端请求伪造防护指南 |
| [XXE Prevention](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html) | XML外部实体注入防护指南 |
| [Authentication](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html) | 身份认证最佳实践指南 |
| [Session Management](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html) | 会话管理安全指南 |
| [Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) | 密码存储安全指南 |
| [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) | 密钥和凭据管理指南 |

### 安全工具推荐

| 工具名称 | 用途 | 支持语言 |
|---------|------|---------|
| Bandit | Python安全扫描 | Python |
| Semgrep | 多语言静态分析 | 多语言 |
| SonarQube | 代码质量和安全扫描 | 多语言 |
| GitLeaks | 密钥泄露检测 | 多语言 |
| Trivy | 漏洞扫描 | 多语言 |
| OWASP ZAP | Web应用安全测试 | Web应用 |

---

## 总结

本指南涵盖了9种常见安全漏洞的修复方法,包含Python、Java、Go、PHP、C#五种语言的代码示例。在实际开发中:

1. **始终验证输入**: 对所有用户输入进行验证和清理
2. **使用安全API**: 优先使用框架提供的安全API
3. **保持更新**: 及时更新依赖库到最新版本
4. **安全测试**: 定期进行安全扫描和渗透测试
5. **持续学习**: 关注最新的安全漏洞和防护技术

如需更详细的信息,请参考对应的OWASP Cheat Sheets和各语言官方安全指南。
