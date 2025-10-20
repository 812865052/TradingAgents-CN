---
version: cn-0.1.14
last_updated: 2025-09-24
code_compatibility: cn-0.1.14
status: complete
---

# 用户认证系统使用指南

> **版本说明**: 本文档基于 `cn-0.1.14` 版本编写  
> **最后更新**: 2025-09-24  
> **状态**: ✅ 完整 - 用户认证系统完整使用指南

## 📋 概述

TradingAgents-CN 采用基于文件的用户认证系统，提供安全的用户登录、权限管理和会话控制功能。系统设计为企业级应用，注重安全性和权限控制。

### 🎯 核心特性

- **🔐 安全认证**: SHA-256密码加密存储
- **👥 角色权限**: 多级用户角色和权限管理
- **⏰会话管理**: 10分钟无操作自动登出
- **📊 活动日志**: 完整的用户操作记录
- **🌐 前端缓存**: 智能登录状态保持
- **🛡️ 安全防护**: 防止会话劫持和CSRF攻击

## 🔑 默认账号信息

系统初始化时会自动创建以下默认账号：

### 管理员账号
```
用户名: admin
密码: admin123
角色: 管理员
权限: 分析、配置、管理员功能
```

### 普通用户账号
```
用户名: user
密码: user123
角色: 普通用户
权限: 仅分析功能
```

> ⚠️ **安全提醒**: 首次部署后请立即修改默认密码！

## 🚀 快速开始

### 1. 首次登录

1. 启动Web界面：
   ```bash
   python start_web.py
   ```

2. 打开浏览器访问：`http://localhost:8501`

3. 使用默认账号登录：
   - 管理员：`admin` / `admin123`
   - 普通用户：`user` / `user123`

### 2. 修改默认密码

登录后建议立即修改密码：

```bash
# 修改管理员密码
python scripts/user_password_manager.py change-password admin 你的新密码

# 修改普通用户密码
python scripts/user_password_manager.py change-password user 你的新密码
```

## 👥 用户角色与权限

### 管理员 (admin)
- **权限**: `["analysis", "config", "admin"]`
- **功能**:
  - ✅ 股票分析功能
  - ✅ 系统配置管理
  - ✅ 用户管理功能
  - ✅ 查看系统日志
  - ✅ 数据库管理

### 普通用户 (user)
- **权限**: `["analysis"]`
- **功能**:
  - ✅ 股票分析功能
  - ❌ 系统配置管理
  - ❌ 用户管理功能
  - ❌ 系统管理功能

## 🛠️ 用户管理

### 命令行管理工具

系统提供了强大的命令行用户管理工具：

#### 列出所有用户
```bash
python scripts/user_password_manager.py list
```

#### 创建新用户
```bash
# 创建普通用户
python scripts/user_password_manager.py create-user 用户名 密码 --role user

# 创建管理员用户
python scripts/user_password_manager.py create-user 管理员名 密码 --role admin
```

#### 修改用户密码
```bash
python scripts/user_password_manager.py change-password 用户名 新密码
```

#### 删除用户
```bash
python scripts/user_password_manager.py delete-user 用户名
```

#### 重置为默认配置
```bash
python scripts/user_password_manager.py reset
```

### Windows 用户

Windows用户可以使用批处理文件：

```cmd
# 列出用户
scripts\user_manager.bat list

# 创建用户
scripts\user_manager.bat create-user 用户名 密码 user

# 修改密码
scripts\user_manager.bat change-password 用户名 新密码
```

## 📁 配置文件管理

### 用户配置文件位置
```
web/config/users.json
```

### 配置文件格式
```json
{
  "用户名": {
    "password_hash": "SHA256哈希值",
    "role": "user|admin",
    "permissions": ["analysis", "config", "admin"],
    "created_at": 时间戳
  }
}
```

### 手动编辑配置文件

如需手动编辑用户配置：

1. 打开 `web/config/users.json`
2. 按照上述格式添加或修改用户信息
3. 密码哈希可通过以下Python代码生成：
   ```python
   import hashlib
   password = "你的密码"
   hash_value = hashlib.sha256(password.encode()).hexdigest()
   print(hash_value)
   ```

## 🔒 安全特性

### 密码安全
- **加密存储**: 使用SHA-256哈希算法
- **不可逆**: 密码不以明文形式存储
- **强度要求**: 建议使用复杂密码

### 会话管理
- **超时机制**: 10分钟无操作自动登出
- **前端缓存**: 智能保持登录状态
- **活动追踪**: 实时更新用户活动时间

### 权限控制
- **分级权限**: 基于角色的访问控制
- **功能隔离**: 不同角色访问不同功能
- **操作审计**: 记录所有用户操作

## 📊 用户活动监控

### 活动日志
系统自动记录以下用户活动：
- 登录/登出事件
- 分析任务执行
- 配置修改操作
- 系统管理操作

### 查看活动日志
管理员可以在Web界面查看用户活动仪表板，包括：
- 用户登录历史
- 操作统计信息
- 系统使用情况

## 🚨 常见问题

### Q1: 忘记密码怎么办？
**A**: 使用命令行工具重置密码：
```bash
python scripts/user_password_manager.py change-password 用户名 新密码
```

### Q2: 用户不存在错误
**A**: 检查用户名是否正确，或创建新用户：
```bash
python scripts/user_password_manager.py create-user 用户名 密码 --role user
```

### Q3: 登录后自动退出
**A**: 这是正常的安全机制，10分钟无操作会自动登出。保持页面活跃即可。

### Q4: 无法访问某些功能
**A**: 检查用户权限，普通用户只能使用分析功能，管理功能需要管理员权限。

### Q5: 配置文件损坏
**A**: 使用重置命令恢复默认配置：
```bash
python scripts/user_password_manager.py reset
```

## 🔧 故障排除

### 认证系统无法启动
1. 检查 `web/config/` 目录权限
2. 确保Python环境正确
3. 查看系统日志：`logs/tradingagents.log`

### 用户配置文件问题
1. 验证JSON格式是否正确
2. 检查文件编码（应为UTF-8）
3. 确认文件路径正确

### 权限错误
1. 检查用户角色配置
2. 验证权限列表格式
3. 重启Web服务

## 📚 相关文档

- [快速开始指南](./quick-start-guide.md)
- [配置管理指南](./config-management-guide.md)
- [故障排除指南](../troubleshooting/)
- [API开发指南](../development/api-development-guide.md)

## 🔄 版本历史

### v0.1.14 (2025-01-15)
- ✅ 完整的用户权限管理系统
- ✅ Web用户认证界面
- ✅ 用户活动日志功能
- ✅ 前端缓存登录状态

### v0.1.14-preview (2024-08-14)
- 🆕 用户认证系统预览版
- 🆕 基础权限控制
- 🆕 登录界面组件

---

## 📞 技术支持

如遇到认证系统相关问题，请：

1. 查看本文档的故障排除部分
2. 检查系统日志文件
3. 参考相关技术文档
4. 联系系统管理员

---

> 💡 **提示**: 定期备份用户配置文件，确保系统安全稳定运行。
