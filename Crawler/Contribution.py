from datetime import date
import re

class Contribution:
    def __init__(self, markup, link):
        self.__contributor = self.__set_contributor(markup)
        self.__paragraph = self.__set_paragraph(markup)
        self.__date = self.__set_date(link)
        __interruptors = ['Mr Speaker', 'Mr. Speaker', 'Mr, Speaker', 'Madam Speaker', 'Mr. Deputy Speaker', 'Mr. Deputy-Speaker', 
                        'Several Hon Members', 'Several Hon. Members', 'Several hon. Members roseâ€”', 'Hon Members', 'Hon.', 'Hon. Members',
                        'An Hon. Member']
        
        if self.__contributor == "The Prime Minister":
            self.__contribution_type = "answer"
        elif self.__contributor in __interruptors:
            self.__contribution_type = "interruption"
        elif len(self.__paragraph) < 20 and '?' in self.__paragraph:
            self.__contribution_type = "interruption"
        elif len(self.__paragraph) < 50 and '?' not in self.__paragraph:
            self.__contribution_type = "interruption"
        else:
            self.__contribution_type = "question"
        
    def __set_contributor(self, markup):
        contributor_markup = markup.find(class_ = "primary-text")
        return contributor_markup.get_text().strip()
        
    def get_contributor(self):
        return self.__contributor
                
    def __set_paragraph(self, markup):
        paragraph_markup = markup.find_all("p")
        paragraph = ""
        for p in paragraph_markup:
            paragraph += p.get_text().strip()
            
        paragraph_no_toggle_text = re.sub(r'Column [0-9]*is located hereToggle showing location of Column [0-9]*', '', paragraph)
        paragraph_no_markup = re.sub(r'<[A-Za-z\/][^>]*>', '', paragraph_no_toggle_text)
        paragraph_no_square_brackets = re.sub(r'[\[].*?[\]]', '', paragraph_no_markup)
        cleaned_paragraph = paragraph_no_square_brackets

        return cleaned_paragraph

    def get_paragraph(self):
        return self.__paragraph

    def __set_date(self, link):
        date_string = link[:10]
        items = date_string.split('-')
        return date(int(items[0]), int(items[1]), int(items[2]))
        
    def get_date(self):
        return self.__date

    def get_contribution_type(self):
        return self.__contribution_type
        
    def concatenate_with(self, paragraph):
        self.__paragraph = self.__paragraph + " " + paragraph

