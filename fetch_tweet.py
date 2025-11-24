from twikit import Client
import nest_asyncio, asyncio

nest_asyncio.apply()

client = Client('en-US')

async def test_twitter_connection():
    try:
        client.load_cookies('cookies.json')

        user_id = await client.user_id()
        me = await client.get_user_by_id(user_id)
        print(f"✅ Logged in as: {me.name} (@{me.screen_name})\n")

        query = "Oppo V6 phone"
        print(f"🔍 Searching 1 tweet for: '{query}'...\n")

        tweets = await client.search_tweet(query, count=1)
        tweet = tweets[0]
        print(f"🗨️  Tweet: {tweet.text}")

    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    asyncio.run(test_twitter_connection())
