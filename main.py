import ticker.process_ticker as ticker
import ticker.stock_history_spider as stock_spider
import seekingalpha.news_spider as news_spider
import seekingalpha.processor as processor
import seekingalpha.word_embedding as word_embedding
import seekingalpha.train as train

ticker.dump_tickers_into_json()
stock_spider.get_all_history()
news_spider.get_news()
processor.process_news()
word_embedding.get_training_data()
train.train()