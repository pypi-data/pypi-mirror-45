import feedparser
from googletrans import Translator


class LanguageTranslator(object):
    translator = Translator()

    def translateToEnglish(self, language):
        """ DocTest: translateToEnglish(input)
        >>> LanguageTranslator().translateToEnglish('잘 지냈어요?')
        'How are you?'
        """
        return self.translator.translate(language).text

    def detectLanguage(self, language):
        """ DocTest: detectLanguage(input)
        >>> LanguageTranslator().detectLanguage('잘 지냈어요?')
        'ko'
        """
        return self.translator.detect(language).lang


class RSSFeed(object):
    cnnFeed = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")
    weatherFeed = feedparser.parse("http://www.rssweather.com/zipcode/45201/rss.php")

    def getCNNFeedTitle(self, index):
        return self.cnnFeed.entries[index].title

    def getCNNFeedURLLink(self, index):
        return self.cnnFeed.entries[index].feedburner_origlink

    def getCincinnatiWeather(self):
        today_weather = "Cincinnati's Temperature: " + self.weatherFeed.entries[0].summary
        return today_weather
