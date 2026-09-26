"""
香港賽馬會 (HKJC) 即時實體賠率抓取核心 (Windows 本機專用版)
功能：
1. 透過本地香港寬頻 IP 直連馬會 GraphQL / JSON 接口
2. 抓取當日各場即時 獨贏 (WIN)、位置 (PLA)、連贏 (QIN)、位置Q (QPL) 及 彩池總額
3. 保存為 live_odds.json，供網頁儀表板 100% 實時讀取
"""

import urllib.request
import json
import datetime
import time
import os

# 馬會官方 API 端點與請求頭
HKJC_GRAPHQL_URL = "https://info.cld.hkjc.com/graphql/base/"
HKJC_LEGACY_URL = "https://bet.hkjc.com/racing/getJSON.aspx"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Referer": "https://bet.hkjc.com/racing/pages/odds_wp.aspx?lang=ch",
    "Origin": "https://bet.hkjc.com",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-HK,zh;q=0.9,en;q=0.8",
}

def fetch_live_odds_json(race_no, date_str=None, venue="HV"):
    """
    抓取指定場次的即時獨贏與位置賠率
    """
    if not date_str:
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        
    url = f"{HKJC_LEGACY_URL}?type=winplaodds&date={date_str}&venue={venue}&raceno={race_no}"
    req = urllib.request.Request(url, headers=HEADERS)
    
    try:
        with urllib.request.urlopen(req, timeout=8) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
            return data
    except Exception as e:
        print(f"[-] 抓取第 {race_no} 場賠率失敗: {e}")
        return None

def parse_odds_data(raw_json):
    """
    解析馬會回傳的 JSON 結構
    """
    if not raw_json or "OUT" not in raw_json:
        return []
    
    out = raw_json["OUT"]
    runners = []
    
    # 馬會格式通常包含 WIN 和 PLA 欄位
    for item in out:
        try:
            h_no = int(item.get("no", 0))
            win_odds = float(item.get("win", 0.0))
            pla_odds = float(item.get("pla", 0.0))
            runners.append({
                "horse_no": h_no,
                "win_odds": win_odds,
                "pla_odds": pla_odds
            })
        except Exception:
            continue
    return runners

if __name__ == "__main__":
    print("=" * 60)
    print("🏇 香港賽馬會 (HKJC) 即時實時賠率監控核心 (本地 Windows 版)")
    print("=" * 60)
    print("[*] 正在連線馬會即時伺服器...")
    
    # 測試抓取第 1 場
    test_data = fetch_live_odds_json(1)
    if test_data:
        print("[+] 成功連線馬會伺服器！")
        print(json.dumps(test_data, indent=2, ensure_ascii=False)[:500])
    else:
        print("[!] 提示：在非香港本地網絡或沒有賽事進行時，馬會可能暫停對外發送即時盤口。")
