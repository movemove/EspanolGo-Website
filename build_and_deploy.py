#!/usr/bin/env python3
"""Build EspanolGo 4-language showcase, /privacy, and /support pages, bundle Cloudflare Worker, and deploy to https://espanolgo.appengine.fun."""
from __future__ import annotations

import base64
import html as html_mod
import json
import os
import sys
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PUBLIC_DIR = BASE_DIR / "public"
IMG_DIR = PUBLIC_DIR / "images"
AUD_DIR = PUBLIC_DIR / "audio"

ACCOUNT_ID = "9fb3b494e6d4d659f2cf567efb94fc38"
ZONE_ID = "977b0b4fa0ab6e587b8758a04016c5e8"
SCRIPT_NAME = "espanolgo-site"
HOSTNAME = "espanolgo.appengine.fun"
ORIGIN = f"https://{HOSTNAME}"
APP_STORE_ID = "6837611917"
APP_STORE_URL = f"https://apps.apple.com/app/id{APP_STORE_ID}"
SUPPORTED_LANGS = ("en", "zh-Hant", "zh-Hans", "ja")

CONTENT = {
    "en": {
        "html_lang": "en",
        "title": "EspanolGo — Travel Spanish, 32 Sounds, 100 Video Dialogues & Live Translation",
        "desc": "Master real-life travel Spanish with 15 guided lessons, 32 LatAm & España IPA sound rules, 24 minimal-pair drills, 100 real-world travel dialogue videos, Voice Practice, and Live 2-Way Translation.",
        "keywords": "EspanolGo,learn Spanish,travel Spanish,Spanish pronunciation,IPA,minimal pairs,voice roleplay,live Spanish translator,AE Interactive",
        "nav_privacy": "Privacy",
        "nav_support": "Support",
        "nav_download": "Get App",
        "hero_badge": "15 LESSONS · 32 SOUNDS · 100 VIDEO DIALOGUES · LIVE TRANSLATION",
        "hero_title": "Speak Real Spanish <span>Before Your Flight Lands</span>",
        "hero_sub": "Master crisp Spanish vowels, rolled rr, 100 real-world travel video scenes, 12 guided staff-first roleplay missions, and instant 2-way voice translation—with zero sign-up and zero tracking.",
        "status_pill": "Available Now on App Store · iPhone, iPad & iPhone Duo",
        "cta_store_sub": "Download Free on",
        "cta_store_main": "App Store",
        "cta_audio": "▶ Hear Native Phrases",
        "cta_screens": "Explore Screens ↓",
        "sec_audio_badge": "REAL IN-APP STUDIO AUDIO · CLEAR SPANISH IPA",
        "sec_audio_title": "Hear Everyday Travel Spanish as Locals Speak It",
        "sec_audio_sub": "Actual studio MP3 clips bundled inside EspanolGo—featuring silent h, soft b/v, throat jota /x/, and exact IPA guidance.",
        "btn_play": "Play",
        "btn_playing": "Playing",
        "sec_screens_badge": "LIVE APP PREVIEWS · IPHONE & IPAD",
        "sec_screens_title": "Built for One-Handed Travel Confidence",
        "sec_screens_sub": "Portrait-first typography with Standard, Large, and Extra-Large text scaling—plus native iPhone Duo and iPad 13-inch support.",
        "screens_labels": [
            "15-Lesson Spanish Path",
            "12-Scene Voice Roleplay",
            "Live 2-Way Interpreter",
            "100 Video Dialogues",
            "32 Sounds & Minimal Pairs",
            "iPad 13-Inch Guided Speaking",
        ],
        "sec_features_badge": "FIVE INTEGRATED MODULES",
        "sec_features_title": "Everything You Need in One Offline-Ready App",
        "features": [
            ("📚", "15 Guided Lessons & 18 Grammar Drills", "Progress smoothly from pure vowels and accent timing through rolled rr, ser vs. estar, por vs. para, gustar, and real café, transit, hotel, and clinic lines."),
            ("🎬", "100 Real-World Travel Scenario Videos", "Chronological scenes across Dining, Shopping, Transit, Hotels, and Emergencies—complete with 200 studio recordings, IPA, and cultural tips."),
            ("🎧", "32 Sounds & 24 Minimal-Pair Ear Drills", "Toggle Latin American (LatAm seseo) and Peninsular (España distinción) IPA guides with mouth placement tips and blind minimal-pair tests (pero vs. perro)."),
            ("💬", "12-Scene Staff-First Voice Practice", "On-device interactive roleplay: local staff speak first, helpful Spanish phrase cards stay onscreen while you talk, and you clear 3 mission steps."),
            ("🗣️", "Live 2-Way Voice Interpreter & 160 SRS Cards", "Translate two-way between English, 繁中, 简中, or 日本語 and Spanish—plus fullscreen show-the-clerk cards and 320 spaced-repetition flashcard recordings."),
            ("🔒", "Zero Sign-In · Local Privacy Only", "No accounts, no ads, and zero third-party SDKs. Your study streaks, mastery, and preferences stay strictly inside iOS UserDefaults on device."),
        ],
        "sec_pricing_badge": "NO SUBSCRIPTIONS · START FREE",
        "sec_pricing_title": "Generous Free Tier. One-Time $3.99 Upgrade.",
        "sec_pricing_sub": "Explore pronunciation, flashcards, quizzes, Lessons 1–3, and 10 video dialogues free—then unlock everything forever with a single App Store purchase.",
        "free_tier_title": "Free Forever",
        "free_tier_price": "$0",
        "free_tier_items": [
            "All 32 LatAm/España sound rules + 24 minimal-pair drills",
            "Complete 160 SRS flashcards (320 clips) & 18 grammar quizzes",
            "Lessons 1–3 + 10 travel video dialogues (2 per category)",
            "Daily free Voice Practice (5/day) & Live Interpreter (8/day)",
        ],
        "pro_tier_badge": "ONE-TIME BUYOUT · NO SUBSCRIPTION",
        "pro_tier_title": "EspanolGo Pro Lifetime",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "All 15 guided travel lessons (Lessons 4–15 unlocked)",
            "All 100 real-world travel videos & 200 studio audio clips",
            "Unlimited 12-scene Voice Practice roleplay turns",
            "Unlimited two-way Live Voice Interpreter (offline-ready)",
        ],
        "bottom_cta_title": "Ready to Speak Spanish on Your Next Trip?",
        "bottom_cta_sub": "Free to start on iPhone & iPad—no sign-up required.",
        "appstore_btn_label": "Download Free on the App Store",
        "privacy_title": "Privacy Policy — EspanolGo",
        "privacy_updated": "Last Updated: November 23, 2026",
        "privacy_sections": [
            ("1. Zero Account & Zero Personal Data Collection", "EspanolGo is developed by AE Interactive (AppEngine Interactive). We do not require registration and never collect, sell, or transmit your personal data to AE Interactive servers (App Store Connect Privacy Label: Data Not Collected / NSPrivacyTracking = false). Study progress, Spanish sound mastery, SRS flashcard intervals, streaks, and font sizes are saved locally on device using iOS UserDefaults (Required Reason API CA92.1)."),
            ("2. Microphone, Speech Recognition & On-Device Processing", "Microphone and speech recognition permissions are requested strictly on demand when you tap a record button in Voice Practice or Live Interpreter. Roleplay prompts and live translations run through Apple's native on-device System Language, Speech, and Translation frameworks without routing conversations to third-party servers."),
            ("3. No Ads, No Analytics, No Tracking", "EspanolGo bundles zero advertising networks, zero third-party telemetry SDKs, and zero cross-app tracking."),
            ("4. Contact Us", "Questions? Email AE Interactive anytime at help@appengine.fun."),
        ],
        "support_title": "Support & Compatibility — EspanolGo",
        "support_sub": "Device requirements for Voice Practice, Offline Translation Packs, and App Support.",
        "support_cards": [
            ("Interactive Voice Practice Compatibility", "Runs 100% on-device via Apple's native system language model. Requires compatible Apple Intelligence hardware running iOS / iPadOS 26.0+ with system features enabled, or use keyboard hints anytime."),
            ("Offline Courses, Videos & Flashcards", "All 15 units, 32 IPA sounds, 24 minimal pairs, 100 real-world travel videos (200 MP3s), 160 flashcards (320 MP3s), and 18 grammar drills work on any iPhone or iPad running iOS 17.0+ without an account."),
            ("Live Two-Way Translation Offline Packs", "Uses Apple's native Translation framework. You can download Spanish and your native language packs in iOS Settings -> Apps -> Translate (or when prompted inside Interpreter) for airplane and subway use."),
            ("Direct Support Contact", "Email AE Interactive at help@appengine.fun — we typically reply within 24 hours."),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive Studio",
    },
    "zh-Hant": {
        "html_lang": "zh-Hant",
        "title": "EspanolGo — 旅遊西語、32 音標與辨音、100 支實境對話影片及即時口譯",
        "desc": "結合 15 堂系統西語課程、32 個拉美／西班牙 IPA 發音規則與 24 組辨音訓練、100 個實境對話影片、12 情境互動口說與四語雙向即時口譯，免登入零追蹤。",
        "keywords": "EspanolGo,西班牙語,西語發音,旅遊西語,即時翻譯,口語練習,西語會話,單字卡,拉美發音,辨音,AE Interactive",
        "nav_privacy": "隱私權政策",
        "nav_support": "支援與常見問題",
        "nav_download": "立即下載",
        "hero_badge": "15 堂系統課 · 32 發音＋24 辨音 · 100 支實境影片 · 四語雙向口譯",
        "hero_title": "飛抵西語國家前，<span>先自信開口說對每一句</span>",
        "hero_sub": "把「32 個核心 IPA 發音與辨音 → 100 個實境對話影片預習 → 店員主動發問互動口說 → 雙向即時語音口譯」串成一條直覺學習路線——免註冊、無廣告、本機隱私優先。",
        "status_pill": "App Store 正式上架 · 免費下載體驗 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "免費下載體驗",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 試聽原生發音",
        "cta_screens": "瀏覽實機畫面 ↓",
        "sec_audio_badge": "收錄真實 App 錄音室語音 · 標註清晰西班牙語 IPA",
        "sec_audio_title": "點一下，試聽地道西語實戰例句",
        "sec_audio_sub": "直接試聽 EspanolGo 內建 320 句單字實戰音檔——一次聽懂不發音 h、柔和 b/v 與喉音 j /x/。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "實機畫面精選 · IPHONE 與 IPAD",
        "sec_screens_title": "單手直式大字體，旅途中一眼看懂",
        "sec_screens_sub": "專為旅遊與通勤單手操作設計，支援標準／大字／特大三段字級與 iPad 13 吋大螢幕。",
        "screens_labels": [
            "15 堂實戰學習路徑",
            "12 情境互動口說練習",
            "四語雙向即時語音口譯",
            "100 個實境對話影片",
            "32 音標與 24 組辨音",
            "iPad 13 吋實境口說模擬",
        ],
        "sec_features_badge": "五大整合模組",
        "sec_features_title": "從零基礎發音到現場救場，一套搞定",
        "features": [
            ("📚", "15 堂實戰路線＋18 堂文法練習", "從五大純淨母音與重音節拍出發，涵蓋彈舌 rr、ser/estar、por/para、gustar 與點餐交通住宿會話。"),
            ("🎬", "100 個旅遊實境對話影片（200 句錄音）", "五大情境×時間線編排，搭配雙語台詞、IPA 音標與文化小叮嚀，先看懂場景再聽懂語速。"),
            ("🎧", "32 核心音標 lab＋24 組易混辨音", "一鍵切換拉美（LatAm seseo）與西班牙（España distinción）IPA，搭配舌位圖解徹底分清 pero / perro。"),
            ("💬", "12 情境店員主動提問口說模擬", "採用裝置端互動引導：店員先開口提問，畫面同步保留西語參考提示方便照唸，完成 3 關旅遊任務。"),
            ("🗣️", "雙向即時語音口譯＋160 張 SRS 單字卡", "支援繁中／簡中／英文／日文 ⇄ 西班牙語雙向互譯與全螢幕大字給對方看，附 320 句錄音間隔重複複習。"),
            ("🔒", "免帳號登入・100% 本機隱私", "零廣告聯播網、零第三方追蹤 SDK（NSPrivacyTracking = false），所有學習進度僅保存於 iPhone 本機。"),
        ],
        "sec_pricing_badge": "無月費訂閱壓力 · 免費起步",
        "sec_pricing_title": "核心工具免費暢學 · $3.99 一次永久買斷",
        "sec_pricing_sub": "免費打好 32 個發音、辨音、單字卡與前 3 課基礎；需要全部 100 支影片與無限口說口譯再一次買斷即可。",
        "free_tier_title": "永久免費版",
        "free_tier_price": "免費 $0",
        "free_tier_items": [
            "完整 32 個拉美／西班牙 IPA 發音與 24 組辨音測試",
            "全套 160 張 SRS 記憶卡（320 句音檔）與 18 堂文法測驗",
            "第 1–3 課完整教學＋10 支精選實境對話影片",
            "每日免費口說互動（5 次/天）與雙向即時口譯（8 次/天）",
        ],
        "pro_tier_badge": "一次買斷 · 無定期訂閱費",
        "pro_tier_title": "EspanolGo Pro 永久買斷版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "解鎖全部 15 堂結構化旅遊西語課程（含第 4–15 課）",
            "解鎖全部 100 支旅遊實境對話影片與 200 句原生音檔",
            "無限次數暢玩 12 情境三回合口說互動任務",
            "無限次數使用四語雙向即時語音口譯（支援離線包）",
        ],
        "bottom_cta_title": "準備好出發去西班牙或拉丁美洲了嗎？",
        "bottom_cta_sub": "在 iPhone 與 iPad 免費下載開始練習，免註冊立即可用。",
        "appstore_btn_label": "前往 App Store 免費下載",
        "privacy_title": "隱私權政策 — EspanolGo",
        "privacy_updated": "最後更新：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 免註冊且零個人資料收集", "EspanolGo 由 AE Interactive（AppEngine Interactive）開發。我們不要求註冊帳號，也絕不收集、販售或上傳任何個人資料至外部伺服器（App Store 隱私標籤：不收集資料 / NSPrivacyTracking = false）。學習進度、發音熟練度、單字排程與字體設定僅透過系統 UserDefaults（Required Reason API CA92.1）保存在裝置本機。"),
            ("2. 麥克風與裝置端語音處理", "麥克風與語音辨識權限僅在您主動點擊口說練習或即時口譯的錄音鍵時請求；語音辨識、翻譯與對話提示均優先呼叫 Apple 裝置端原生框架，不會將對話上傳第三方追蹤伺服器。"),
            ("3. 無廣告、無追蹤碼", "本 App 不含任何廣告 SDK、行為分析工具或跨 App 追蹤機制。"),
            ("4. 聯絡我們", "任何問題或合作洽詢，歡迎來信 help@appengine.fun。"),
        ],
        "support_title": "支援與裝置相容性 — EspanolGo",
        "support_sub": "互動口說環境需求、離線翻譯語系包下載方式與客服聯絡信箱。",
        "support_cards": [
            ("互動口說練習相容裝置", "透過 Apple 裝置端原生語言模型運作，需於支援 Apple Intelligence 的 iPhone / iPad（iOS / iPadOS 26.0 以上並開啟系統功能）上執行；其他裝置亦可隨時開啟提示卡或切換文字作答。"),
            ("離線課程、影片與測驗完整相容", "全部 15 堂課、32 音標、24 辨音、100 支實境影片（200 句 MP3）、160 張單字卡（320 句 MP3）與 18 堂文法測驗於任何 iOS 17.0 以上之 iPhone / iPad 皆可離線流暢使用。"),
            ("雙向即時口譯離線語系包", "採用 Apple 原生 Translation 框架；出發前可在 iOS「設定 → App → 翻譯」預先下載西班牙文與您的母語離線包，搭飛機或進地鐵也能翻。"),
            ("直接聯繫客服", "寫信至 help@appengine.fun，AE Interactive 團隊通常於 24 小時內回覆。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 版權所有。",
        "studio_link_label": "AE Interactive 開發工作室",
    },
    "zh-Hans": {
        "html_lang": "zh-Hans",
        "title": "EspanolGo — 旅游西语、32 音标与辨音、100 支实景对话视频及实时口译",
        "desc": "集 15 节系统西语课程、32 个拉美/西班牙 IPA 发音规则与 24 组辨音训练、100 个实景对话视频、12 情景互动口语与四语双向实时口译于一身，免登录零追踪。",
        "keywords": "EspanolGo,西班牙语,西语发音,旅游西语,实时翻译,口语练习,西语会话,单词卡,拉美发音,辨音,AE Interactive",
        "nav_privacy": "隐私政策",
        "nav_support": "支持与常见问题",
        "nav_download": "立即下载",
        "hero_badge": "15 节系统课 · 32 发音+24 辨音 · 100 支实景视频 · 四语双向口译",
        "hero_title": "落地西语国家前，<span>先自信开口说对每一句</span>",
        "hero_sub": "将“32 个核心 IPA 发音与辨音 → 100 个实景对话视频预习 → 店员主动提问互动口语 → 双向实时语音口译”串成一条流畅路线——免注册、无广告、本地隐私优先。",
        "status_pill": "App Store 正式上线 · 免费下载体验 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "免费下载体验",
        "cta_store_main": "App Store",
        "cta_audio": "▶ 试听原生发音",
        "cta_screens": "浏览实机画面 ↓",
        "sec_audio_badge": "收录真实 App 录音室语音 · 清晰标注西班牙语 IPA",
        "sec_audio_title": "点一下，试听地道西语实战例句",
        "sec_audio_sub": "直接试听 EspanolGo 内置 320 句单词实战音频——一次听清不发音 h、柔和 b/v 与喉音 j /x/。",
        "btn_play": "播放",
        "btn_playing": "播放中",
        "sec_screens_badge": "实机画面精选 · IPHONE 与 IPAD",
        "sec_screens_title": "单手竖屏大字体，旅途中一眼看懂",
        "sec_screens_sub": "专为旅行单手操作设计，支持标准/大字/特大三档字号与 iPad 13 英寸大屏。",
        "screens_labels": [
            "15 节实战学习路径",
            "12 情景互动口语练习",
            "四语双向实时语音口译",
            "100 个实景对话视频",
            "32 音标与 24 组辨音",
            "iPad 13 英寸实景口语模拟",
        ],
        "sec_features_badge": "五大整合模块",
        "sec_features_title": "从零基础发音到现场救场，一套搞定",
        "features": [
            ("📚", "15 节实战路线 + 18 节语法练习", "从五大纯净元音与重音节拍起步，涵盖弹舌 rr、ser/estar、por/para、gustar 与点餐交通住宿会话。"),
            ("🎬", "100 个旅游实景对话视频（200 句录音）", "五大场景×时间线编排，配双语台词、IPA 音标与文化要点，先看懂场景再跟上原生语速。"),
            ("🎧", "32 核心音标实验室 + 24 组易混辨音", "一键切换拉美（LatAm seseo）与西班牙（España distinción）IPA，配舌位图解彻底区分 pero / perro。"),
            ("💬", "12 情景店员主动发问口语模拟", "采用设备端互动引导：店员先开口发问，屏幕同步保留西语参考提示方便照读，完成 3 关旅行任务。"),
            ("🗣️", "双向实时语音口译 + 160 张 SRS 单词卡", "支持繁中/简中/英文/日文 ⇄ 西班牙语双向互译与全屏大字给对方看，附 320 句录音间隔重复复习。"),
            ("🔒", "免账号登录 · 100% 本地隐私", "零广告联盟、零第三方追踪 SDK（NSPrivacyTracking = false），学习记录仅保存在您的设备本地。"),
        ],
        "sec_pricing_badge": "无月费订阅压力 · 免费起步",
        "sec_pricing_title": "核心工具免费畅学 · $3.99 一次永久买断",
        "sec_pricing_sub": "免费打好 32 个发音、辨音、单词卡与前 3 节基础；需要全部 100 支视频与无限口语口译再一次解锁即可。",
        "free_tier_title": "永久免费版",
        "free_tier_price": "免费 $0",
        "free_tier_items": [
            "完整 32 个拉美/西班牙 IPA 发音与 24 组辨音测试",
            "全套 160 张 SRS 记忆卡（320 句音频）与 18 节语法测验",
            "第 1–3 节完整教学 + 10 支精选实景对话视频",
            "每日免费口语互动（5 次/天）与双向实时口译（8 次/天）",
        ],
        "pro_tier_badge": "一次买断 · 无定期订阅费",
        "pro_tier_title": "EspanolGo Pro 永久买断版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "解锁全部 15 节结构化旅游西语课程（含第 4–15 节）",
            "解锁全部 100 支旅游实景对话视频与 200 句原生音频",
            "无限次数畅玩 12 情景三回合口语互动任务",
            "无限次数使用四语双向实时语音口译（支持离线包）",
        ],
        "bottom_cta_title": "准备好出发去西班牙或拉丁美洲了吗？",
        "bottom_cta_sub": "在 iPhone 与 iPad 免费下载开始练习，免注册立即可用。",
        "appstore_btn_label": "前往 App Store 免费下载",
        "privacy_title": "隐私政策 — EspanolGo",
        "privacy_updated": "最后更新：2026 年 11 月 23 日",
        "privacy_sections": [
            ("1. 免注册且零个人数据收集", "EspanolGo 由 AE Interactive（AppEngine Interactive）开发。我们不要求注册账号，也绝不收集、出售或上传任何个人数据至外部服务器（App Store 隐私标签：不收集数据 / NSPrivacyTracking = false）。学习进度、发音熟练度、单词排程与字体设置仅通过系统 UserDefaults（Required Reason API CA92.1）保存在设备本地。"),
            ("2. 麦克风与设备端语音处理", "麦克风与语音识别权限仅在您主动点击口语练习或实时口译录音键时请求；语音识别、翻译与对话提示均优先调用 Apple 设备端原生框架，不会将对话发送至第三方追踪服务器。"),
            ("3. 无广告、无追踪代码", "本 App 不包含任何广告 SDK、行为分析工具或跨应用追踪机制。"),
            ("4. 联系我们", "如有任何问题，欢迎发送邮件至 help@appengine.fun。"),
        ],
        "support_title": "支持与设备兼容性 — EspanolGo",
        "support_sub": "互动口语环境要求、离线翻译语言包下载指南与客服邮箱。",
        "support_cards": [
            ("互动口语练习兼容设备", "通过 Apple 设备端原生语言模型运行，需在支持 Apple Intelligence 的 iPhone / iPad（iOS / iPadOS 26.0 及以上并开启系统功能）上运行；其他设备也可随时点击提示或使用键盘输入。"),
            ("离线课程、视频与测验全兼容", "全部 15 节课、32 音标、24 辨音、100 支实景视频（200 句 MP3）、160 张单词卡（320 句 MP3）与 18 节语法测验在任何 iOS 17.0 及以上 iPhone / iPad 上均可离线使用。"),
            ("双向实时口译离线语言包", "采用 Apple 原生 Translation 框架；行前可在 iOS“设置 → App → 翻译”预先下载西班牙语与您的母语离线包，航班或地铁无网也能用。"),
            ("直接联系客服", "写信至 help@appengine.fun，AE Interactive 团队通常在 24 小时内回复。"),
        ],
        "footer_rights": "© 2026 AE Interactive. 保留所有权利。",
        "studio_link_label": "AE Interactive 工作室",
    },
    "ja": {
        "html_lang": "ja",
        "title": "EspanolGo — 旅行スペイン語・32発音記号・100本実境動画・リアルタイム双方向通訳",
        "desc": "全15課の体系的ロードマップ、中南米／スペイン32発音ルール＆24組の聞き分けテスト、100本の実境会話動画、12場面の対話練習と4言語対応双方向通訳を一つに。",
        "keywords": "EspanolGo,スペイン語学習,旅行スペイン語,スペイン語発音,IPA,聞き分け,音声通訳,単語帳,AE Interactive",
        "nav_privacy": "プライバシーポリシー",
        "nav_support": "サポート",
        "nav_download": "無料入手",
        "hero_badge": "全15課 · 32発音+24聞き分け · 100本実境動画 · 4言語双方向通訳",
        "hero_title": "現地に到着する前に、<span>通じるスペイン語を口から</span>",
        "hero_sub": "5つの明瞭な母音や巻き舌rr、100本の旅行実境動画、店員が先に話しかける12場面の対話練習、リアルタイム双方向音声通訳まで——登録不要・広告ゼロで快適に。",
        "status_pill": "App Store で配信中 · 無料で体験 · iPhone / iPad / iPhone Duo",
        "cta_store_sub": "無料でダウンロード",
        "cta_store_main": "App Store",
        "cta_audio": "▶ ネイティブ音声を試聴",
        "cta_screens": "アプリ画面を見る ↓",
        "sec_audio_badge": "アプリ収録のスタジオ音声 · 見やすいスペイン語IPA表記",
        "sec_audio_title": "旅先でそのまま使えるスペイン語を試聴",
        "sec_audio_sub": "EspanolGoに収録された320語の例文MP3から厳選——発音しないHや喉音J /x/ の響きを体感できます。",
        "btn_play": "再生",
        "btn_playing": "再生中",
        "sec_screens_badge": "アプリ画面プレビュー · IPHONE & IPAD",
        "sec_screens_title": "片手縦持ちで移動中も迷わず確認",
        "sec_screens_sub": "標準／大／特大の3段階文字サイズ調整に加え、iPad 13インチの大画面にも最適化されています。",
        "screens_labels": [
            "全15課の学習ロードマップ",
            "12場面・実践会話ロールプレイ",
            "4言語対応リアルタイム双方向通訳",
            "100本の旅行・日常実境動画",
            "32発音ルール＆24組聞き分け",
            "iPad 13インチ 会話練習画面",
        ],
        "sec_features_badge": "5つの統合モジュール",
        "sec_features_title": "発音の基礎から現地での会話サポートまでこれ一本",
        "features": [
            ("📚", "全15課の学習ルート＆18問の文法ドリル", "5つの母音とアクセント位置の基礎から、巻き舌rr、ser/estar、por/para、カフェ・電車・ホテル・病院表現まで段階的に習得。"),
            ("🎬", "100本の実境旅行会話動画（音声200本）", "食事・買物・空港交通・宿泊・緊急時の5カテゴリを時系列に収録。二言語台詞・IPA・文化解説付き。"),
            ("🎧", "32発音ラボ＆24組の聞き分けテスト", "中南米（LatAm）とスペイン（España）IPAをワンタップ切替。舌の位置ガイドとブラインド聴き比べで pero / perro を完全攻略。"),
            ("💬", "店員が先に話す12場面ロールプレイ", "端末内言語モデルを活用した対話練習。ヒントを見ながら3ステップのミッションを達成でき、静かな場所ではキーボード入力も可能。"),
            ("🗣️", "双方向リアルタイム音声通訳＆160語SRS単語帳", "日本語・英語・繁体字・簡体字 ⇄ スペイン語の音声通訳（全画面表示対応）と320本音声付きSM-2単語カードを搭載。"),
            ("🔒", "ログイン不要・端末内プライバシー徹底", "広告SDKや外部トラッキングは一切なし（NSPrivacyTracking = false）。学習記録は端末内のUserDefaultsのみに保存されます。"),
        ],
        "sec_pricing_badge": "月額課金なし・無料で体験",
        "sec_pricing_title": "充実の無料範囲・一度きりの $3.99 買い切り",
        "sec_pricing_sub": "まずは32発音・単語帳・第1〜3課・厳選動画10本を無料で体験し、必要になった時に一回買い切りで永久解放できます。",
        "free_tier_title": "ずっと無料プラン",
        "free_tier_price": "無料 $0",
        "free_tier_items": [
            "32の中南米／スペインIPA発音規則＆24組聞き分けテスト",
            "160語のSM-2単語カード（音声320本）＆文法ドリル18問",
            "第1〜3課の全レッスン＋旅行会話動画10本（各カテゴリ2本）",
            "毎日の無料枠：会話練習（5回/日）・双方向音声通訳（8回/日）",
        ],
        "pro_tier_badge": "一回買い切り · サブスクなし",
        "pro_tier_title": "EspanolGo Pro 買い切り版",
        "pro_tier_price": "$3.99",
        "pro_tier_items": [
            "全15課の旅行スペイン語カリキュラムを永久解放（第4〜15課）",
            "100本すべての実境会話動画＆200本のネイティブ音声を解放",
            "12場面×3ステップの実践会話ロールプレイが回数無制限",
            "4言語対応リアルタイム双方向音声通訳を無制限利用",
        ],
        "bottom_cta_title": "スペイン・中南米旅行の準備を始めませんか？",
        "bottom_cta_sub": "iPhone・iPadで今すぐ無料ダウンロード。アカウント作成は不要です。",
        "appstore_btn_label": "App Storeで無料入手",
        "privacy_title": "プライバシーポリシー — EspanolGo",
        "privacy_updated": "最終更新日: 2026年11月23日",
        "privacy_sections": [
            ("1. アカウント登録不要・個人情報収集ゼロ", "EspanolGoはAE Interactive（AppEngine Interactive）が開発しています。会員登録は不要で、個人データを当社サーバーへ収集・販売・送信することは一切ありません（App Storeラベル：データ未収集 / NSPrivacyTracking = false）。学習進捗・発音習得度・単語帳スケジュールは端末内のUserDefaults（Required Reason API CA92.1）にのみ保存されます。"),
            ("2. マイク・音声認識および端末内処理", "マイクと音声認識権限は、ユーザーが会話練習またはリアルタイム通訳の録音ボタンを押した際にのみオンデマンドで要求されます。通訳と対話練習はApple純正の端末内フレームワークを利用し、第三者サーバーへ会話を送信しません。"),
            ("3. 広告・トラッキングなし", "広告ネットワーク、第三者解析SDK、アプリ間トラッキングは一切含まれていません。"),
            ("4. お問い合わせ", "ご質問は help@appengine.fun までメールでご連絡ください。"),
        ],
        "support_title": "サポート・動作環境 — EspanolGo",
        "support_sub": "インタラクティブ会話練習の対応機種、オフライン翻訳パックの設定方法、お問い合わせ窓口。",
        "support_cards": [
            ("インタラクティブ会話練習の対応機種", "Apple純正の端末内言語モデルを使用し、Apple Intelligence対応のiPhone / iPad（iOS / iPadOS 26.0以降・機能有効時）で動作します。非対応端末でもヒント表示やキーボードで学習可能です。"),
            ("オフライン教材・動画・クイズの対応機種", "全15課、32発音記号、24聞き分け、100本の実境動画（200本MP3）、160語単語帳（320本MP3）、18文法テストは iOS 17.0以降のすべてのiPhone / iPad でアカウント不要で動作します。"),
            ("双方向音声通訳のオフラインパック", "Apple純正Translationフレームワークを使用します。渡航前にiOSの「設定 → アプリ → 翻訳」からスペイン語と日本語パックをダウンロードしておくと機内や地下鉄でも利用可能です。"),
            ("ダイレクトサポート窓口", "AE Interactive（help@appengine.fun）までご連絡ください。通常24時間以内にご返信いたします。"),
        ],
        "footer_rights": "© 2026 AE Interactive. All rights reserved.",
        "studio_link_label": "AE Interactive スタジオ",
    },
}

AUDIO_ITEMS = [
    {
        "file": "split.mp3",
        "es": "¿Podemos pagar por separado?",
        "phonetic": "/poˈðemos paˈɣaɾ poɾ sepaˈ<b>ɾaðo</b>/ · por <b>separado</b>",
        "meaning": {
            "en": "Can we pay separately?",
            "zh-Hant": "請問我們可以分開結帳嗎？",
            "zh-Hans": "请问我们可以分开结账吗？",
            "ja": "別々にお支払いできますか？",
        },
        "tag": {
            "en": "Dining & Tapas · Split Bill",
            "zh-Hant": "餐館分帳 · 日常必備",
            "zh-Hans": "餐馆分账 · 日常必备",
            "ja": "レストラン・別会計",
        },
    },
    {
        "file": "oatmilk.mp3",
        "es": "¿Tienen leche de avena o de almendras?",
        "phonetic": "/ˈtjenen ˈletʃe ðe aˈ<b>β</b>ena o ðe alˈmendɾas/ · <b>b/v</b> → /β/",
        "meaning": {
            "en": "Do you have oat or almond milk?",
            "zh-Hant": "請問你們有燕麥奶或杏仁奶嗎？",
            "zh-Hans": "请问你们有燕麦奶或杏仁奶吗？",
            "ja": "オーツミルクかアーモンドミルクはありますか？",
        },
        "tag": {
            "en": "Café · Soft b/v Liaison",
            "zh-Hant": "咖啡廳 · b/v 柔和擦音",
            "zh-Hans": "咖啡厅 · b/v 柔和擦音",
            "ja": "カフェ・b/v の柔らかい発音",
        },
    },
    {
        "file": "card.mp3",
        "es": "¿Puedo pagar con tarjeta?",
        "phonetic": "/ˈpweðo paˈɣaɾ kon taɾˈ<b>x</b>eta/ · tar<b>j</b>eta (/x/)",
        "meaning": {
            "en": "Can I pay by card?",
            "zh-Hant": "請問我可以刷信用卡嗎？",
            "zh-Hans": "请问我可以刷信用卡吗？",
            "ja": "カードで支払えますか？",
        },
        "tag": {
            "en": "Checkout · Spanish Jota /x/",
            "zh-Hant": "結帳刷卡 · 喉音 J /x/",
            "zh-Hans": "结账刷卡 · 喉音 J /x/",
            "ja": "会計・喉音 J /x/",
        },
    },
    {
        "file": "checkin.mp3",
        "es": "Hola, vengo a hacer el check-in.",
        "phonetic": "/ˈ<b>o</b>la ˈβeŋɡo a aˈ<b>seɾ</b> el tʃekˈin/ · Silent <b>H</b>",
        "meaning": {
            "en": "Hello, I'm here to check in.",
            "zh-Hant": "您好，我要辦理入住手續。",
            "zh-Hans": "您好，我要办理入住手续。",
            "ja": "こんにちは、チェックインをお願いします。",
        },
        "tag": {
            "en": "Hotel Desk · Silent H",
            "zh-Hant": "飯店櫃檯 · 不發音的 H",
            "zh-Hans": "酒店前台 · 不发音的 H",
            "ja": "ホテル受付・発音しない H",
        },
    },
]

CSS = """
:root {
  --bg: #070913;
  --card: rgba(20, 24, 42, 0.86);
  --card-solid: #14182a;
  --border: rgba(255, 255, 255, 0.11);
  --text: #F8FAFC;
  --muted: #94A3B8;
  --accent: #F97316;
  --teal: #2DD4BF;
  --amber: #FBBF24;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "PingFang TC", "PingFang SC", "Hiragino Sans", "Helvetica Neue", Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  overflow-x: hidden;
  background-image:
    radial-gradient(ellipse 80% 42% at 50% -5%, rgba(249, 115, 22, 0.22) 0%, transparent 70%),
    radial-gradient(circle at 86% 18%, rgba(45, 212, 191, 0.14) 0%, transparent 45%);
  background-repeat: no-repeat;
}
a { color: inherit; }
header { position: sticky; top: 12px; z-index: 100; padding: 0 16px; }
nav {
  max-width: 980px; margin: 0 auto; padding: 10px 16px;
  display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap;
  background: rgba(11, 14, 28, 0.84);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border); border-radius: 999px;
  box-shadow: 0 12px 34px rgba(0,0,0,0.45);
}
.brand { display: flex; align-items: center; gap: 10px; text-decoration: none; font-weight: 800; font-size: 17px; letter-spacing: -0.3px; }
.brand img { width: 34px; height: 34px; border-radius: 9px; border: 1px solid rgba(251, 146, 60, 0.55); }
.nav-right { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.nav-links { display: flex; gap: 14px; font-size: 13px; font-weight: 600; color: var(--muted); }
.nav-links a { text-decoration: none; transition: color .18s; }
.nav-links a:hover, .nav-links a.active { color: #fff; }
.lang-picker {
  display: flex; align-items: center; gap: 4px;
  background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.09);
  padding: 4px 10px; border-radius: 999px; font-size: 12px; font-weight: 700;
}
.lang-picker a { color: var(--muted); text-decoration: none; padding: 2px 6px; border-radius: 99px; }
.lang-picker a.active { color: var(--teal); background: rgba(45,212,191,0.14); }
main { max-width: 980px; margin: 0 auto; padding: 36px 18px 64px; }
.hero { text-align: center; padding: 20px 0 36px; }
.badge {
  display: inline-block; font-size: 11px; font-weight: 800; letter-spacing: 0.7px;
  color: var(--teal); background: rgba(45,212,191,0.12);
  border: 1px solid rgba(45,212,191,0.34); padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
h1 { font-size: clamp(30px, 5.4vw, 54px); font-weight: 900; letter-spacing: -1.1px; line-height: 1.12; margin-bottom: 14px; text-wrap: balance; }
h1 span { background: linear-gradient(125deg, #FB923C 0%, #FBBF24 46%, #2DD4BF 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { max-width: 680px; margin: 0 auto 22px; color: var(--muted); font-size: clamp(15px, 2vw, 18px); text-wrap: balance; }
.status-pill {
  display: inline-flex; align-items: center; gap: 8px; padding: 8px 16px; border-radius: 999px;
  background: rgba(249,115,22,0.14); border: 1px solid rgba(251,146,60,0.4);
  color: #FED7AA; font-size: 13px; font-weight: 700; margin-bottom: 22px;
}
.hero-cta { display: flex; justify-content: center; gap: 12px; flex-wrap: wrap; }
.btn {
  display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 999px;
  font-size: 14px; font-weight: 700; text-decoration: none; border: 1px solid transparent; cursor: pointer;
  transition: transform .16s ease, box-shadow .16s ease, background .16s ease;
}
.btn:hover { transform: translateY(-1px); }
.btn-primary { border: 0; background: linear-gradient(135deg, #EA580C, #14B8A6); color: #fff; box-shadow: 0 10px 26px rgba(234,88,12,0.32); }
.btn-ghost { background: rgba(255,255,255,0.06); border-color: var(--border); color: #E2E8F0; }
.btn-appstore {
  background: #fff; color: #090D16; border: 1px solid rgba(255,255,255,0.85);
  padding: 9px 20px; gap: 10px; box-shadow: 0 12px 30px rgba(255,255,255,0.16), 0 8px 24px rgba(249,115,22,0.28);
}
.btn-appstore svg { width: 20px; height: 24px; fill: currentColor; flex-shrink: 0; }
.btn-appstore .as-copy { display: flex; flex-direction: column; align-items: flex-start; line-height: 1.12; text-align: left; }
.btn-appstore .as-sub { font-size: 10px; font-weight: 700; opacity: 0.72; letter-spacing: 0.2px; }
.btn-appstore .as-main { font-size: 15px; font-weight: 850; letter-spacing: -0.2px; }
.nav-cta {
  display: inline-flex; align-items: center; gap: 6px; padding: 6px 14px; border-radius: 999px;
  background: linear-gradient(135deg, #EA580C, #14B8A6); color: #fff; text-decoration: none;
  font-size: 12.5px; font-weight: 800; box-shadow: 0 4px 14px rgba(234,88,12,0.35);
  transition: transform .16s ease, filter .16s ease;
}
.nav-cta:hover { transform: translateY(-1px); filter: brightness(1.08); }
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 16px; }
.price-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 24px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 18px;
}
.price-card.pro {
  border-color: rgba(45, 212, 191, 0.55);
  background: linear-gradient(160deg, rgba(249,115,22,0.16), rgba(20,24,42,0.94) 45%, rgba(20,184,166,0.14));
  box-shadow: 0 18px 40px rgba(0,0,0,0.42);
}
.price-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.price-tag { font-size: 11px; font-weight: 800; color: var(--teal); letter-spacing: 0.4px; margin-bottom: 4px; }
.price-title { font-size: 20px; font-weight: 850; color: #fff; }
.price-num { font-size: 26px; font-weight: 900; color: #fff; white-space: nowrap; }
.price-list { list-style: none; display: flex; flex-direction: column; gap: 10px; }
.price-list li { display: flex; gap: 9px; font-size: 14px; color: #CBD5E1; line-height: 1.45; }
.price-list li span.chk { color: var(--teal); font-weight: 900; flex-shrink: 0; }
.price-card .btn-appstore { justify-content: center; }
.cta-banner {
  margin-top: 56px; padding: 34px 24px; border-radius: 26px; text-align: center;
  background: linear-gradient(135deg, rgba(249,115,22,0.2), rgba(20,184,166,0.18));
  border: 1px solid rgba(45,212,191,0.35);
  display: flex; flex-direction: column; align-items: center; gap: 14px;
}
.cta-banner img { width: 64px; height: 64px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.25); box-shadow: 0 10px 28px rgba(0,0,0,0.4); }
.cta-banner h2 { margin-bottom: 0; }
.cta-banner p { color: #CBD5E1; max-width: 540px; font-size: 15px; }
section { margin-top: 56px; }
.sec-head { text-align: center; margin-bottom: 24px; }
.sec-head .badge { margin-bottom: 10px; }
h2 { font-size: clamp(22px, 3.6vw, 34px); font-weight: 850; letter-spacing: -0.6px; margin-bottom: 8px; }
.sec-sub { color: var(--muted); max-width: 620px; margin: 0 auto; font-size: 15px; }
.audio-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; }
.audio-card {
  background: var(--card); border: 1px solid var(--border); border-radius: 18px; padding: 16px;
  display: flex; flex-direction: column; justify-content: space-between; gap: 12px;
  transition: border-color .2s, transform .2s;
}
.audio-card.playing { border-color: var(--teal); box-shadow: 0 0 0 1px rgba(45,212,191,0.3), 0 14px 32px rgba(0,0,0,0.4); }
.audio-tag { font-size: 11px; font-weight: 700; color: var(--teal); letter-spacing: 0.3px; }
.audio-es { font-size: 18px; font-weight: 800; margin-top: 6px; color: #fff; line-height: 1.3; }
.audio-ipa { font-size: 12.5px; color: #FDBA74; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; margin-top: 6px; }
.audio-ipa b { background: rgba(45, 212, 191, 0.2); color: #5EEAD4; padding: 0 4px; border-radius: 4px; }
.audio-meaning { font-size: 13px; color: var(--muted); margin-top: 6px; }
.play-btn {
  align-self: flex-start; background: rgba(249,115,22,0.2); color: #FED7AA; border: 1px solid rgba(251,146,60,0.45);
  padding: 6px 14px; border-radius: 999px; font-size: 12.5px; font-weight: 700; cursor: pointer;
}
.audio-card.playing .play-btn { background: var(--teal); color: #042F2E; border-color: var(--teal); }
.gallery-strip {
  display: flex; gap: 16px; overflow-x: auto; padding: 8px 4px 16px; scroll-snap-type: x mandatory;
}
.shot-card {
  flex: 0 0 230px; scroll-snap-align: start; background: var(--card); border: 1px solid var(--border);
  border-radius: 20px; padding: 10px; text-align: center;
}
.shot-card.wide { flex: 0 0 340px; }
.shot-card img { width: 100%; height: auto; border-radius: 14px; display: block; }
.shot-cap { font-size: 12.5px; font-weight: 700; color: #CBD5E1; margin-top: 9px; }
.bento { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; }
.bento-card { background: var(--card); border: 1px solid var(--border); border-radius: 20px; padding: 20px; }
.bento-icon { font-size: 24px; margin-bottom: 10px; }
.bento-card h3 { font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #fff; }
.bento-card p { font-size: 14px; color: var(--muted); }
.doc-box { max-width: 780px; margin: 14px auto; background: var(--card); border: 1px solid var(--border); border-radius: 22px; padding: 28px; }
.doc-box h1 { font-size: clamp(24px, 4vw, 36px); text-align: left; }
.doc-item { margin-top: 22px; padding-top: 18px; border-top: 1px solid var(--border); }
.doc-item h2 { font-size: 18px; margin-bottom: 6px; color: #E2E8F0; }
.doc-item p { font-size: 14.5px; color: var(--muted); }
footer {
  max-width: 980px; margin: 36px auto 0; padding: 24px 18px 42px;
  border-top: 1px solid var(--border);
  display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: 13px;
}
footer a { color: #CBD5E1; text-decoration: none; }
footer a:hover { color: var(--teal); }
@media (max-width: 680px) {
  nav { border-radius: 22px; padding: 10px 14px; }
  .nav-right { gap: 8px; }
  .hero-cta .btn { width: 100%; justify-content: center; max-width: 300px; }
}
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn, .audio-card { transition: none; }
}
"""

SCRIPT_JS = """
const audioMap = {};
let activeKey = null;
function togglePhrase(key, src, btnEl, cardEl, playLabel, playingLabel) {
  if (activeKey && activeKey !== key && audioMap[activeKey]) {
    audioMap[activeKey].audio.pause();
    audioMap[activeKey].audio.currentTime = 0;
    audioMap[activeKey].btn.textContent = "▶ " + playLabel;
    audioMap[activeKey].card.classList.remove("playing");
  }
  let item = audioMap[key];
  if (!item) {
    const a = new Audio(src);
    item = { audio: a, btn: btnEl, card: cardEl };
    a.addEventListener("ended", () => {
      btnEl.textContent = "▶ " + playLabel;
      cardEl.classList.remove("playing");
      if (activeKey === key) activeKey = null;
    });
    audioMap[key] = item;
  }
  if (!item.audio.paused) {
    item.audio.pause();
    item.audio.currentTime = 0;
    btnEl.textContent = "▶ " + playLabel;
    cardEl.classList.remove("playing");
    activeKey = null;
  } else {
    item.audio.play();
    btnEl.textContent = "■ " + playingLabel;
    cardEl.classList.add("playing");
    activeKey = key;
  }
}
"""


def appstore_badge_svg() -> str:
    return '<svg viewBox="0 0 384 512" aria-hidden="true"><path d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 75.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>'


def nav_html(lang: str, route: str, t: dict) -> str:
    langs = [("en", "EN"), ("zh-Hant", "繁中"), ("zh-Hans", "简中"), ("ja", "日本語")]
    lang_links = []
    for code, label in langs:
        cls = ' class="active"' if code == lang else ""
        href = f"{route}?lang={code}"
        lang_links.append(f'<a href="{href}"{cls}>{label}</a>')
    p_cls = ' class="active"' if route == "/privacy" else ""
    s_cls = ' class="active"' if route == "/support" else ""
    q = f"?lang={lang}"
    return f"""
<header>
  <nav aria-label="Main navigation">
    <a class="brand" href="/{q}">
      <img src="/images/icon.webp" alt="EspanolGo Icon" width="34" height="34">
      <span>EspanolGo</span>
    </a>
    <div class="nav-right">
      <div class="nav-links">
        <a href="/privacy{q}"{p_cls}>{html_mod.escape(t['nav_privacy'])}</a>
        <a href="/support{q}"{s_cls}>{html_mod.escape(t['nav_support'])}</a>
      </div>
      <div class="lang-picker" role="navigation" aria-label="Language">{''.join(lang_links)}</div>
      <a class="nav-cta" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['nav_download'])}</a>
    </div>
  </nav>
</header>"""


def footer_html(lang: str, t: dict) -> str:
    q = f"?lang={lang}"
    return f"""
<footer>
  <div>{html_mod.escape(t['footer_rights'])}</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <a href="/{q}">EspanolGo</a>
    <a href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">App Store</a>
    <a href="/privacy{q}">{html_mod.escape(t['nav_privacy'])}</a>
    <a href="/support{q}">{html_mod.escape(t['nav_support'])}</a>
    <a href="https://appengine.fun" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['studio_link_label'])}</a>
    <a href="mailto:help@appengine.fun">help@appengine.fun</a>
  </div>
</footer>"""


OG_LOCALES = {
    "en": "en_US",
    "zh-Hant": "zh_TW",
    "zh-Hans": "zh_CN",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "es": "es_ES",
}


def head_html(lang: str, t: dict, title: str, canonical_path: str, faq_items: list[tuple[str, str]] | None = None) -> str:
    q = f"?lang={lang}" if lang != "en" else ""
    canon_url = f"{ORIGIN}{canonical_path}{q}"
    site_langs = ('en', 'zh-Hant', 'zh-Hans', 'ja')
    app_schema: dict = {
        "@type": "SoftwareApplication",
        "name": 'EspanolGo: Travel Spanish',
        "softwareVersion": '1.0.0',
        "operatingSystem": "iOS 17.0+, iPadOS 17.0+",
        "applicationCategory": "EducationApplication",
        "url": ORIGIN,
        "image": f"{ORIGIN}/images/og.png",
        "inLanguage": list(site_langs),
        "isAccessibleForFree": True,
        "offers": [
            {"@type": "Offer", "name": "Free Forever", "price": "0", "priceCurrency": "USD"},
            {"@type": "Offer", "name": "EspanolGo Pro Lifetime", "price": "3.99", "priceCurrency": "USD"},
        ],
        "publisher": {"@id": "https://appengine.fun/#organization"},
    }
    if APP_STORE_URL:
        app_schema["downloadUrl"] = APP_STORE_URL
        app_schema["installUrl"] = APP_STORE_URL
    graph: list[dict] = [
        {
            "@type": "Organization",
            "@id": "https://appengine.fun/#organization",
            "name": "AE Interactive",
            "url": "https://appengine.fun/",
            "sameAs": ["https://www.youtube.com/@appengine-a", "https://languages.appengine.fun/"],
        },
        {
            "@type": "WebSite",
            "@id": f"{ORIGIN}/#website",
            "name": 'EspanolGo',
            "url": f"{ORIGIN}/",
            "inLanguage": list(site_langs),
            "publisher": {"@id": "https://appengine.fun/#organization"},
        },
        app_schema,
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "AE Interactive", "item": "https://appengine.fun/"},
                {"@type": "ListItem", "position": 2, "name": "AE Languages", "item": "https://languages.appengine.fun/"},
                {"@type": "ListItem", "position": 3, "name": 'EspanolGo', "item": f"{ORIGIN}/"},
            ] + (
                [{"@type": "ListItem", "position": 4, "name": title, "item": canon_url}]
                if canonical_path != "/"
                else []
            ),
        },
    ]
    if faq_items:
        graph.append({
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": h, "acceptedAnswer": {"@type": "Answer", "text": p}}
                for h, p in faq_items
            ],
        })
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    smart_banner = f'<meta name="apple-itunes-app" content="app-id={APP_STORE_ID}">\n' if APP_STORE_ID else ""
    alternates = "".join(
        f'<link rel="alternate" hreflang="{code}" href="{ORIGIN}{canonical_path}' + ("" if code == "en" else f"?lang={code}") + '">\n'
        for code in site_langs
    )
    og_loc = OG_LOCALES.get(lang, "en_US")
    og_loc_alts = "".join(
        f'<meta property="og:locale:alternate" content="{OG_LOCALES[c]}">\n'
        for c in site_langs if c != lang
    )
    return f"""<!DOCTYPE html>
<html lang="{t['html_lang']}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html_mod.escape(title)}</title>
<meta name="description" content="{html_mod.escape(t['desc'])}">
<meta name="keywords" content="{html_mod.escape(t['keywords'])}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
<meta name="author" content="AE Interactive">
<meta name="theme-color" content="#070913">
{smart_banner}<link rel="canonical" href="{canon_url}">
{alternates}<link rel="alternate" hreflang="x-default" href="{ORIGIN}{canonical_path}">
<link rel="icon" type="image/png" href="/images/icon.png">
<link rel="apple-touch-icon" href="/images/icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AE Interactive">
<meta property="og:locale" content="{og_loc}">
{og_loc_alts}<meta property="og:title" content="{html_mod.escape(title)}">
<meta property="og:description" content="{html_mod.escape(t['desc'])}">
<meta property="og:url" content="{canon_url}">
<meta property="og:image" content="{ORIGIN}/images/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html_mod.escape(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html_mod.escape(title)}">
<meta name="twitter:description" content="{html_mod.escape(t['desc'])}">
<meta name="twitter:image" content="{ORIGIN}/images/og.png">
<meta name="twitter:image:alt" content="{html_mod.escape(title)}">
<script type="application/ld+json">{schema}</script>
<style>{CSS}</style>
</head>"""


def build_home(lang: str, t: dict) -> str:
    audio_cards = []
    for idx, item in enumerate(AUDIO_ITEMS):
        play_lbl = html_mod.escape(t["btn_play"])
        playing_lbl = html_mod.escape(t["btn_playing"])
        audio_cards.append(f"""
        <article class="audio-card" id="card-{idx}">
          <div>
            <div class="audio-tag">{html_mod.escape(item['tag'][lang])}</div>
            <div class="audio-es">{html_mod.escape(item['es'])}</div>
            <div class="audio-ipa">{item['phonetic']}</div>
            <div class="audio-meaning">{html_mod.escape(item['meaning'][lang])}</div>
          </div>
          <button type="button" class="play-btn" onclick="togglePhrase('p{idx}','/audio/{item['file']}',this,document.getElementById('card-{idx}'),'{play_lbl}','{playing_lbl}')">▶ {play_lbl}</button>
        </article>""")

    shot_cards = []
    for i in range(1, 6):
        lbl = html_mod.escape(t["screens_labels"][i - 1])
        shot_cards.append(f"""
        <div class="shot-card">
          <img src="/images/{lang}_s0{i}.webp" alt="{lbl}" loading="lazy" width="640" height="1390">
          <div class="shot-cap">{lbl}</div>
        </div>""")
    ipad_lbl = html_mod.escape(t["screens_labels"][5])
    shot_cards.append(f"""
        <div class="shot-card wide">
          <img src="/images/{lang}_ipad.webp" alt="{ipad_lbl}" loading="lazy" width="760" height="1013">
          <div class="shot-cap">{ipad_lbl}</div>
        </div>""")

    bento_cards = []
    for icon, title, body in t["features"]:
        bento_cards.append(f"""
        <article class="bento-card">
          <div class="bento-icon" aria-hidden="true">{icon}</div>
          <h3>{html_mod.escape(title)}</h3>
          <p>{html_mod.escape(body)}</p>
        </article>""")

    free_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["free_tier_items"])
    pro_lis = "".join(f'<li><span class="chk">✓</span><span>{html_mod.escape(x)}</span></li>' for x in t["pro_tier_items"])
    appstore_btn = (
        f'<a class="btn btn-appstore" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">'
        f'{appstore_badge_svg()}'
        f'<span class="as-copy"><span class="as-sub">{html_mod.escape(t["cta_store_sub"])}</span>'
        f'<span class="as-main">{html_mod.escape(t["cta_store_main"])}</span></span></a>'
    )

    return f"""{head_html(lang, t, t['title'], '/')}
<body>
{nav_html(lang, '/', t)}
<main>
  <section class="hero">
    <div class="badge">{html_mod.escape(t['hero_badge'])}</div>
    <h1>{t['hero_title']}</h1>
    <p class="hero-sub">{html_mod.escape(t['hero_sub'])}</p>
    <div class="status-pill"> {html_mod.escape(t['status_pill'])}</div>
    <div class="hero-cta">
      {appstore_btn}
      <a class="btn btn-primary" href="#audio">{html_mod.escape(t['cta_audio'])}</a>
      <a class="btn btn-ghost" href="#preview">{html_mod.escape(t['cta_screens'])}</a>
    </div>
  </section>

  <section id="audio">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_audio_badge'])}</div>
      <h2>{html_mod.escape(t['sec_audio_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_audio_sub'])}</p>
    </div>
    <div class="audio-grid">{''.join(audio_cards)}</div>
  </section>

  <section id="preview">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_screens_badge'])}</div>
      <h2>{html_mod.escape(t['sec_screens_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_screens_sub'])}</p>
    </div>
    <div class="gallery-strip">{''.join(shot_cards)}</div>
  </section>

  <section id="features">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_features_badge'])}</div>
      <h2>{html_mod.escape(t['sec_features_title'])}</h2>
    </div>
    <div class="bento">{''.join(bento_cards)}</div>
  </section>

  <section id="pricing">
    <div class="sec-head">
      <div class="badge">{html_mod.escape(t['sec_pricing_badge'])}</div>
      <h2>{html_mod.escape(t['sec_pricing_title'])}</h2>
      <p class="sec-sub">{html_mod.escape(t['sec_pricing_sub'])}</p>
    </div>
    <div class="pricing-grid">
      <article class="price-card">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">ESPANOLGO FREE</div>
              <div class="price-title">{html_mod.escape(t['free_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['free_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{free_lis}</ul>
        </div>
        <a class="btn btn-ghost" style="justify-content:center;" href="{APP_STORE_URL}" target="_blank" rel="noopener noreferrer">{html_mod.escape(t['appstore_btn_label'])}</a>
      </article>
      <article class="price-card pro">
        <div>
          <div class="price-head">
            <div>
              <div class="price-tag">{html_mod.escape(t['pro_tier_badge'])}</div>
              <div class="price-title">{html_mod.escape(t['pro_tier_title'])}</div>
            </div>
            <div class="price-num">{html_mod.escape(t['pro_tier_price'])}</div>
          </div>
          <ul class="price-list" style="margin-top:16px;">{pro_lis}</ul>
        </div>
        {appstore_btn}
      </article>
    </div>
  </section>

  <section class="cta-banner">
    <img src="/images/icon.webp" alt="EspanolGo" width="64" height="64">
    <h2>{html_mod.escape(t['bottom_cta_title'])}</h2>
    <p>{html_mod.escape(t['bottom_cta_sub'])}</p>
    {appstore_btn}
  </section>
</main>
{footer_html(lang, t)}
<script>{SCRIPT_JS}</script>
</body>
</html>"""


def build_doc_page(lang: str, t: dict, route: str, heading: str, sub: str, items: list[tuple[str, str]]) -> str:
    blocks = "".join(
        f'<div class="doc-item"><h2>{html_mod.escape(h)}</h2><p>{html_mod.escape(p)}</p></div>'
        for h, p in items
    )
    faq = items if route == '/support' else None
    return f"""{head_html(lang, t, heading + ' | EspanolGo', route, faq_items=faq)}
<body>
{nav_html(lang, route, t)}
<main>
  <article class="doc-box">
    <h1>{html_mod.escape(heading)}</h1>
    <p style="color:var(--teal);font-weight:700;font-size:14px;margin-top:8px;">{html_mod.escape(sub)}</p>
    {blocks}
  </article>
</main>
{footer_html(lang, t)}
</body>
</html>"""


def cf_request(method: str, path: str, token: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"https://api.cloudflare.com/client/v4{path}", data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read())


def deploy_worker(token: str, worker_js: str) -> None:
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}"
    boundary = "----EspanolGoBoundary918273"
    body = [
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="metadata"',
        b"Content-Type: application/json",
        b"",
        json.dumps({"main_module": "index.js", "compatibility_date": "2024-03-03"}).encode(),
        f"--{boundary}".encode(),
        b'Content-Disposition: form-data; name="index.js"; filename="index.js"',
        b"Content-Type: application/javascript+module",
        b"",
        worker_js.encode("utf-8"),
        f"--{boundary}--".encode(),
        b"",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(body),
        method="PUT",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        res = json.loads(resp.read())
        assert res.get("success"), f"Worker upload failed: {res}"
        print("WORKER_UPLOADED:", SCRIPT_NAME)


def ensure_dns_and_route(token: str) -> None:
    dns = cf_request("GET", f"/zones/{ZONE_ID}/dns_records?name={HOSTNAME}", token)
    existing = dns.get("result", [])
    if not existing:
        created = cf_request("POST", f"/zones/{ZONE_ID}/dns_records", token, {
            "type": "A",
            "name": HOSTNAME,
            "content": "192.0.2.1",
            "proxied": True,
            "ttl": 1,
        })
        assert created.get("success"), f"DNS create failed: {created}"
        print("DNS_CREATED:", HOSTNAME)
    else:
        print("DNS_EXISTS:", [(r["type"], r["name"], r["content"], r["proxied"]) for r in existing])

    routes = cf_request("GET", f"/zones/{ZONE_ID}/workers/routes", token).get("result", [])
    pattern = f"{HOSTNAME}/*"
    match = [r for r in routes if r.get("pattern") == pattern]
    if not match:
        rc = cf_request("POST", f"/zones/{ZONE_ID}/workers/routes", token, {
            "pattern": pattern,
            "script": SCRIPT_NAME,
        })
        assert rc.get("success"), f"Route create failed: {rc}"
        print("ROUTE_CREATED:", pattern, "->", SCRIPT_NAME)
    else:
        rid = match[0]["id"]
        if match[0].get("script") != SCRIPT_NAME:
            cf_request("PUT", f"/zones/{ZONE_ID}/workers/routes/{rid}", token, {
                "pattern": pattern,
                "script": SCRIPT_NAME,
            })
            print("ROUTE_UPDATED:", pattern, "->", SCRIPT_NAME)
        else:
            print("ROUTE_EXISTS:", pattern, "->", SCRIPT_NAME)


def main() -> None:
    pages = {}
    privacy_pages = {}
    support_pages = {}
    for code, t in CONTENT.items():
        home_html = build_home(code, t)
        priv_html = build_doc_page(code, t, "/privacy", t["privacy_title"], t["privacy_updated"], t["privacy_sections"])
        supp_html = build_doc_page(code, t, "/support", t["support_title"], t["support_sub"], t["support_cards"])
        pages[code] = home_html
        privacy_pages[code] = priv_html
        support_pages[code] = supp_html
        suffix = "" if code == "en" else f"_{code}"
        (PUBLIC_DIR / f"index{suffix}.html").write_text(home_html, encoding="utf-8")
        (PUBLIC_DIR / f"privacy{suffix}.html").write_text(priv_html, encoding="utf-8")
        (PUBLIC_DIR / f"support{suffix}.html").write_text(supp_html, encoding="utf-8")

    images = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(IMG_DIR.glob("*"))}
    audio = {p.name: base64.b64encode(p.read_bytes()).decode("ascii") for p in sorted(AUD_DIR.glob("*.mp3"))}

    _site_langs = ('en', 'zh-Hant', 'zh-Hans', 'ja')
    def _sm_entry(path: str, code: str, prio: str) -> str:
        loc = f"{ORIGIN}{path}" if code == "en" else f"{ORIGIN}{path}?lang={code}"
        links = "\n".join(
            [f'    <xhtml:link rel="alternate" hreflang="{c}" href="{ORIGIN}{path}' + ("" if c == "en" else f"?lang={c}") + '"/>' for c in _site_langs]
            + [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}"/>']
        )
        return f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>2026-11-26</lastmod>\n{links}\n    <priority>{prio}</priority>\n  </url>"

    sitemap_urls = "\n".join(
        [_sm_entry("/", c, "1.0" if c == "en" else "0.9") for c in _site_langs]
        + [_sm_entry("/privacy", "en", "0.7"), _sm_entry("/support", "en", "0.7")]
    )
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{sitemap_urls}\n</urlset>'
    robots_txt = f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}/sitemap.xml\n"

    worker_js = f"""const PAGES = {json.dumps(pages)};
const PRIVACY_PAGES = {json.dumps(privacy_pages)};
const SUPPORT_PAGES = {json.dumps(support_pages)};
const IMAGES = {json.dumps(images)};
const AUDIO = {json.dumps(audio)};
const SITEMAP = {json.dumps(sitemap_xml)};
const ROBOTS = {json.dumps(robots_txt)};

function b64ToBytes(b64) {{
  const s = atob(b64);
  const out = new Uint8Array(s.length);
  for (let i = 0; i < s.length; i++) out[i] = s.charCodeAt(i);
  return out;
}}

function resolveLang(request) {{
  const url = new URL(request.url);
  const q = url.searchParams.get("lang");
  if (q && PAGES[q]) return q;
  if (q === "zh-TW" || q === "tw" || q === "hk") return "zh-Hant";
  if (q === "zh-CN" || q === "cn" || q === "zh") return "zh-Hans";
  if (q === "jp") return "ja";
  const accept = (request.headers.get("accept-language") || "").toLowerCase();
  if (accept.includes("zh-tw") || accept.includes("zh-hk") || accept.includes("zh-hant")) return "zh-Hant";
  if (accept.includes("zh")) return "zh-Hans";
  if (accept.includes("ja")) return "ja";
  return "en";
}}

export default {{
  async fetch(request) {{
    const pathname = new URL(request.url).pathname;
    if (pathname === "/sitemap.xml") {{
      return new Response(SITEMAP, {{ headers: {{ "content-type": "application/xml;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname === "/robots.txt") {{
      return new Response(ROBOTS, {{ headers: {{ "content-type": "text/plain;charset=UTF-8", "cache-control": "public, max-age=86400" }} }});
    }}
    if (pathname.startsWith("/images/")) {{
      const name = pathname.slice("/images/".length);
      if (IMAGES[name]) {{
        const ct = name.endsWith(".png") ? "image/png" : "image/webp";
        return new Response(b64ToBytes(IMAGES[name]), {{ headers: {{ "content-type": ct, "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    if (pathname.startsWith("/audio/")) {{
      const name = pathname.slice("/audio/".length);
      if (AUDIO[name]) {{
        return new Response(b64ToBytes(AUDIO[name]), {{ headers: {{ "content-type": "audio/mpeg", "accept-ranges": "bytes", "cache-control": "public, max-age=31536000, immutable" }} }});
      }}
      return new Response("Not Found", {{ status: 404 }});
    }}
    const lang = resolveLang(request);
    const htmlHeaders = {{
      "content-type": "text/html;charset=UTF-8",
      "cache-control": "public, max-age=0, must-revalidate",
      "vary": "Accept-Language"
    }};
    if (pathname === "/privacy" || pathname === "/privacy.html") {{
      return new Response(PRIVACY_PAGES[lang] || PRIVACY_PAGES.en, {{ headers: htmlHeaders }});
    }}
    if (pathname === "/support" || pathname === "/support.html") {{
      return new Response(SUPPORT_PAGES[lang] || SUPPORT_PAGES.en, {{ headers: htmlHeaders }});
    }}
    return new Response(PAGES[lang] || PAGES.en, {{ headers: htmlHeaders }});
  }}
}};
"""
    (BASE_DIR / "worker.js").write_text(worker_js, encoding="utf-8")
    print(f"BUILT_WORKER: {len(worker_js) / 1024:.1f} KB")

    if "--build-only" in sys.argv:
        return

    token = os.environ.get("CF_API_TOKEN", "").strip()
    if not token:
        token = Path("~/.cf_token").expanduser().read_text().strip()
    deploy_worker(token, worker_js)
    ensure_dns_and_route(token)
    print("DEPLOY_COMPLETE:", ORIGIN)


if __name__ == "__main__":
    main()
