from datetime import date

class Contribution:
    def __init__(self, markup, link):
        self.contributor = self.get_contributor(markup)
        self.paragraph = self.get_paragraph(markup)
        self.date = self.get_date(link)
        # Associated question or answer? How to create this key? Date, contributor and number?
        
        if self.contributor == "The Prime Minister":
            self.contribution_type = "answer"
        elif self.contributor == "Mr Speaker":          # Examples in every session
            self.contribution_type = "interruption"
        elif self.contributor == "Hon. Members":        # Found an example - view-source:https://hansard.parliament.uk/commons/2022-01-12/debates/3B53E066-9746-4AB8-A8F9-9C08981A8D9B/OralAnswersToQuestions
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
        return paragraph

    def get_date(self, link):
        date_string = link[:10]
        items = date_string.split('-')
        return date(int(items[0]), int(items[1]), int(items[2]))

