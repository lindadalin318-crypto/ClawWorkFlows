#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 Chrome 浏览器提取 X (Twitter) Cookie
前提：你已经在 Chrome 中登录了 x.com
"""

import os
import json
import shutil
import sqlite3
import tempfile
import subprocess
import base64

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "x_cookies.json")

def get_chrome_encryption_key():
    """获取 macOS 上 Chrome 的 Cookie 加密密钥"""
    try:
        result = subprocess.run(
            ['security', 'find-generic-password', '-w', '-a', 'Chrome', '-s', 'Chrome Safe Storage'],
            capture_output=True, text=True
        )
        password = result.stdout.strip()
        if password:
            import hashlib
            key = hashlib.pbkdf2_hmac(
                'sha1',
                password.encode('utf8'),
                b'saltysalt',
                1003,
                dklen=16
            )
            return key
    except Exception as e:
        print(f"⚠️ 获取加密密钥失败: {e}")
    return None

def decrypt_cookie_value(encrypted_value, key):
    """解密 Chrome Cookie 值"""
    try:
        from Crypto.Cipher import AES
        # Chrome macOS 格式：v10 + IV(16) + ciphertext
        if encrypted_value[:3] == b'v10':
            iv = b' ' * 16
            encrypted_value = encrypted_value[3:]
            cipher = AES.new(key, AES.MODE_CBC, IV=iv)
            decrypted = cipher.decrypt(encrypted_value)
            # 去除 PKCS7 padding
            padding = decrypted[-1]
            return decrypted[:-padding].decode('utf-8')
    except Exception as e:
        pass
    return ""

def extract_x_cookies():
    chrome_cookie_path = os.path.expanduser(
        '~/Library/Application Support/Google/Chrome/Default/Cookies'
    )
    
    if not os.path.exists(chrome_cookie_path):
        print("❌ 未找到 Chrome Cookie 文件")
        return False

    # 复制数据库（Chrome 可能锁定原文件）
    tmp = tempfile.mktemp(suffix='.db')
    shutil.copy2(chrome_cookie_path, tmp)
    
    try:
        key = get_chrome_encryption_key()
        conn = sqlite3.connect(tmp)
        cursor = conn.cursor()
        
        # 查询 x.com 和 twitter.com 的 Cookie
        cursor.execute("""
            SELECT name, encrypted_value, host_key, path, expires_utc, is_secure, is_httponly
            FROM cookies
            WHERE host_key LIKE '%x.com%' OR host_key LIKE '%twitter.com%'
        """)
        
        rows = cursor.fetchall()
        print(f"找到 {len(rows)} 条 X/Twitter Cookie")
        
        if len(rows) == 0:
            print("❌ 未找到 X Cookie，请确认你已在 Chrome 中登录 x.com")
            conn.close()
            os.unlink(tmp)
            return False
        
        # 转换为 Playwright 格式
        playwright_cookies = []
        for name, encrypted_value, domain, path, expires_utc, is_secure, is_httponly in rows:
            # 尝试解密
            value = ""
            if key and encrypted_value:
                value = decrypt_cookie_value(encrypted_value, key)
            
            # Chrome 时间戳转 Unix 时间戳（微秒 → 秒，从1601年1月1日起）
            expires = -1
            if expires_utc > 0:
                expires = (expires_utc / 1000000) - 11644473600
            
            playwright_cookies.append({
                "name": name,
                "value": value,
                "domain": domain if domain.startswith('.') else domain,
                "path": path,
                "expires": expires,
                "httpOnly": bool(is_httponly),
                "secure": bool(is_secure),
                "sameSite": "None"
            })
        
        conn.close()
        os.unlink(tmp)
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(playwright_cookies, f, indent=2)
        
        print(f"✅ Cookie 已保存到 {OUTPUT_FILE}")
        
        # 检查关键 Cookie 是否存在
        key_cookies = {c['name'] for c in playwright_cookies}
        important = ['auth_token', 'ct0', 'twid']
        for ck in important:
            if ck in key_cookies:
                print(f"  ✅ 关键 Cookie '{ck}' 存在")
            else:
                print(f"  ❌ 关键 Cookie '{ck}' 缺失（可能未登录或加密未解密）")
        
        return True
        
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        import traceback
        traceback.print_exc()
        if os.path.exists(tmp):
            os.unlink(tmp)
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("📦 从 Chrome 提取 X Cookie")
    print("=" * 50)
    
    # 检查是否有 pycryptodome
    try:
        from Crypto.Cipher import AES
        print("✅ pycryptodome 已安装")
    except ImportError:
        print("⚠️ 安装 pycryptodome...")
        import subprocess
        subprocess.run(['pip', 'install', 'pycryptodome', '-q'])
    
    success = extract_x_cookies()
    if success:
        print("\n✅ 完成！现在可以运行搜索测试了")
    else:
        print("\n❌ 提取失败，请检查是否已在 Chrome 中登录 x.com")
