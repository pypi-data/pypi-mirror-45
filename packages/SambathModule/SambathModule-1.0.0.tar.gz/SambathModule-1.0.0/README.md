# SambathModule

This module is created for assignment purpose only. It contains two main parts: RSS feeds and language translator.

## Usage

# There are two classes inside the module: LanguageTranslator and RSSFeed. To import it:
	from SambathModule import *

# To translate, for example, Korean to English:
	languageTranslator = LanguageTranslator()
	print(languageTranslator.translateToEnglish('잘 지냈어요?'))

# To detect, for example, Korean language:
	languageDectector = LanguageTranslator()
	print(languageDectector.detectLanguage('잘 지냈어요?'))

# To retrieve RSSFeed information, such as Weather at Cincinnati or CNN Top News:
	rssFeed = RSSFeed()
	print(rssFeed.getCNNFeedTitle(0))
	print((rssFeed.getCNNFeedURLLink(0)))
	print(rssFeed.getCincinnatiWeather())




