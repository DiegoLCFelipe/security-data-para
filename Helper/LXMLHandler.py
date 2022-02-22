from bs4 import BeautifulSoup


class LXMLHandler:
    FORWARD_OFFSET_FROM_HREF_TAG_ATTRIBUTE = 6
    BACKWARD_OFFSET_FROM_TITLE_TAG_ATTRIBUTE = 2
    FORWARD_OFFSET_FROM_TITLE_TAG_ATTRIBUTE = 7
    BACKWARD_OFFSET_FROM_TAG_END = 6

    def __init__(self, lxml_code):
        self.__lxml_code = lxml_code

    def find_url_tags(self):
        return self.__lxml_code.find_all(self.url_filter)

    @staticmethod
    def url_filter(tag):
        return tag.has_attr('href') and \
               tag.has_attr('title') and \
               tag.has_attr('class') and not \
                   tag.has_attr('rel') and not \
                   tag.has_attr('a') and not \
                   tag.has_attr('property')

    def _find_url_start(self, url_line):
        return url_line.find('href') + self.FORWARD_OFFSET_FROM_HREF_TAG_ATTRIBUTE

    def _find_url_end(self, url_line):
        return url_line.find('title') - self.BACKWARD_OFFSET_FROM_TITLE_TAG_ATTRIBUTE

    def _find_title_start(self, url_line):
        return url_line.find('title') + self.FORWARD_OFFSET_FROM_TITLE_TAG_ATTRIBUTE

    def _find_title_end(self, url_line):
        return url_line.find('>') - self.BACKWARD_OFFSET_FROM_TAG_END

    def get_urls(self):
        lst_links_of_page = []
        lst_titles_of_page = []
        for tag in self.find_url_tags():
            lst_links_of_page.append(str(tag)[self._find_url_start(str(tag)):self._find_url_end(str(tag))])
            lst_titles_of_page.append(
                str(tag)[self._find_title_start(str(tag)):self._find_title_end(str(tag))])

        return lst_titles_of_page, lst_links_of_page

    def find_table(self):
        return self.__lxml_code.find('table')

    def table_content(self):
        lst_row_data = []
        for trs in self.find_table().find_all('tr')[1:]:
            row_data = trs.find_all('td')
            row = [i.text.replace(",", "") for i in row_data]

            lst_row_data.append(row)
        return lst_row_data

    def table_header(self):
        table_content = self.table_content()
        lst_header = []
        for i in self.find_table().find_all('th'):
            title = i.text
            lst_header.append(title)

        if len(lst_header) > len(table_content[0]):
            return lst_header[0:len(table_content[0])]

        return lst_header
