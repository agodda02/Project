class Contribution:
    def __init__(self, markup):
        self.contributor = self.get_contributor(markup)
        self.paragraph = self.get_paragraph(markup)
        # Date of contribution
        # Associated question or answer? How to create this key? Date, contributor and number?
        
        if "Prime Minister" in self.contributor:
            self.question_or_answer = "answer"
        else:
            self.question_or_answer = "question"
        
    def get_contributor(self, markup):
        contributor_markup = markup.find(class_ = "primary-text")
        return contributor_markup.get_text().strip()
        
    def get_paragraph(self, markup):
        paragraph_markup = markup.find_all("p")
        paragraph = ""
        for p in paragraph_markup:
            paragraph += p.get_text().strip()
        return paragraph

