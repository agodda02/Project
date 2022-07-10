from datetime import date
import re

class Contribution:
    def __init__(self, markup, link):
        self.contributor = self.get_contributor(markup)
        self.paragraph = self.get_paragraph(markup)
        self.date = self.get_date(link)
        interruptors = ['Mr Speaker', 'Mr. Speaker', 'Mr, Speaker', 'Madam Speaker', 'Mr. Deputy Speaker', 'Mr. Deputy-Speaker', 
                        'Several Hon Members', 'Several Hon. Members', 'Several hon. Members roseâ€”', 'Hon Members', 'Hon.', 'Hon. Members',
                        'An Hon. Member']
        
        if self.contributor == "The Prime Minister":
            self.contribution_type = "answer"
        elif self.contributor in interruptors:
            self.contribution_type = "interruption"
        else:
            self.contribution_type = "question"
        
    def get_contributor(self, markup):
        contributor_markup = markup.find(class_ = "primary-text")
        return contributor_markup.get_text().strip()
        
    def get_paragraph(self, markup):
        paragraph_markup = markup.find_all("p")
        paragraph = ""
        for p in paragraph_markup:
            paragraph += p.get_text().strip()
            
        paragraph_no_toggle_text = re.sub(r'Column [0-9]*is located hereToggle showing location of Column [0-9]*', '', paragraph)
        paragraph_no_markup = re.sub(r'<[A-Za-z\/][^>]*>', '', paragraph_no_toggle_text)
        paragraph_no_square_brackets = re.sub(r'[\[].*?[\]]', '', paragraph_no_markup)
        cleaned_paragraph = paragraph_no_square_brackets

        return cleaned_paragraph

    def get_date(self, link):
        date_string = link[:10]
        items = date_string.split('-')
        return date(int(items[0]), int(items[1]), int(items[2]))
        
    def concatenate_with(self, paragraph):
        self.paragraph = self.paragraph + " " + paragraph

