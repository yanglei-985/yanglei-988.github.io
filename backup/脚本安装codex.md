@echo off
chcp 65001 >nul
title Codex 一键安装脚本
echo ========================================
echo        Codex 一键安装脚本
echo ========================================
echo.

:: 需要管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 正在请求管理员权限...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: ─────────────────────────────────────────
:: 刷新当前会话的 PATH
:: ─────────────────────────────────────────
for /f "tokens=*" %%i in ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\",\"Machine\")"') do set "SYS_PATH=%%i"
for /f "tokens=*" %%i in ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\",\"User\")"') do set "USR_PATH=%%i"
set "PATH=%SYS_PATH%;%USR_PATH%"

:: ─────────────────────────────────────────
:: 安装 winget（如果没有）
:: ─────────────────────────────────────────
echo [检测] winget...
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [提示] 未检测到 winget，正在安装...
    powershell -Command "Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe" >nul 2>&1
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [错误] winget 安装失败，请手动安装 Node.js 和 Git：
        echo   Node.js：https://nodejs.org/zh-cn/download
        echo   Git：https://git-scm.com/download/win
        pause
        exit /b 1
    )
)
echo [OK] winget 可用

:: ─────────────────────────────────────────
:: 安装 Git
:: ─────────────────────────────────────────
echo.
echo [检测] Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] 正在安装 Git，请稍候...
    winget install Git.Git -e --silent --accept-package-agreements --accept-source-agreements
    for /f "tokens=*" %%i in ('powershell -Command "[System.Environment]::GetEnvironmentVariable(\"PATH\",\"Machine\")"') do set "PATH=%%i;%PATH%"
) else (
    echo [OK] Git 已安装
)

:: ─────────────────────────────────────────
:: 安装 Node.js
:: ─────────────────────────────────────────
echo.
echo [检测] Node.js...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [安装] 正在安装 Node.js，请稍候...
    winget install OpenJS.NodeJS.LTS -e --silent --accept-package-agreements --accept-source-agreements
    echo.
    echo [提示] Node.js 安装完成，需要重启脚本使环境变量生效
    echo [提示] 请关闭此窗口后重新双击运行脚本！
    pause
    exit /b 0
) else (
    echo [OK] Node.js 已安装：
    node --version
)

:: ─────────────────────────────────────────
:: 安装 Codex
:: ─────────────────────────────────────────
echo.
echo [安装] 正在安装 Codex，请稍候...
npm install -g @openai/codex
if %errorlevel% neq 0 (
    echo [错误] Codex 安装失败，请检查网络连接后重试
    pause
    exit /b 1
)
echo [OK] Codex 安装成功

:: ─────────────────────────────────────────
:: 写入配置
:: ─────────────────────────────────────────
echo.
echo [配置] 写入 API 配置...

set CODEX_DIR=%USERPROFILE%\.codex
if not exist "%CODEX_DIR%" mkdir "%CODEX_DIR%"

:: 写入 auth.json
(
echo {
echo   "OPENAI_API_KEY": "sk-135015f496145b2c50d773c1aed762b5fa98efede5342539f667a4dfd9485442"
echo }
) > "%CODEX_DIR%\auth.json"
echo [OK] 写入 auth.json

:: 写入 config.toml
(
echo model_provider = "aicoco"
echo model = "gpt-5.2-codex"
echo model_reasoning_effort = "high"
echo disable_response_storage = true
echo preferred_auth_method = "apikey"
echo.
echo [model_providers.aicoco]
echo name = "aicoco"
echo base_url = "https://aicoco.xyz/v1"
echo wire_api = "responses"
) > "%CODEX_DIR%\config.toml"
echo [OK] 写入 config.toml

echo.
echo ========================================
echo   安装完成！
echo ========================================
echo.
echo 使用方法：打开 CMD 或 PowerShell，输入 codex 启动
echo.
pause


vless://45b4bd9c-6a6d-4c57-cfb4-e85b535d844f@69.63.218.212:44?security=reality&encryption=none&pbk=5ZKqYySQiiqjmG_LkVtN3HDbVBAkHlhjMPkwPzGOGzQ&headerType=none&fp=firefox&type=tcp&flow=xtls-rprx-vision&sni=apps.mzstatic.com#vless-reality