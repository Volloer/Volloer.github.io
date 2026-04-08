import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. 環境変数の読み込み (ファイル名を secret.env に指定)
load_dotenv("secret.env")

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

# 接続エラーチェック
if not url or not key:
    print("エラー: secret.env から URL または KEY が読み込めませんでした。")
    exit()

supabase: Client = create_client(url, key)

def process_new_data():
    # 2. まだ処理されていないデータだけを取得 (is_processed が False のもの)
    # ※後述する SQL でカラムを追加した後に有効になります
    try:
        response = (
            supabase.table("posts")
            .select("*")
            .eq("is_processed", False) 
            .execute()
        )
        
        records = response.data
        print(f"--- 処理開始: 未処理データ {len(records)} 件 ---")

        for record in records:
            # 3. Python でのデータ処理 (例: 文字数カウント)
            content = record.get('content', '')
            content_length = len(content)
            print(f"ID: {record['id']} を処理中... (文字数: {content_length})")

            # 4. 処理が終わったら「処理済み」に更新する
            supabase.table("posts") \
                .update({"is_processed": True}) \
                .eq("id", record["id"]) \
                .execute()
                
        print("--- すべての処理が完了しました ---")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        print("※テーブルに 'is_processed' カラムがない可能性があります。")

if __name__ == "__main__":
    process_new_data()