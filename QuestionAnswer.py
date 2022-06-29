from bs4 import BeautifulSoup

with open("example.txt", "r") as f:
    data = f.read()

soup = BeautifulSoup(data, 'html.parser')
contributions = soup.find_all(class_ = 'debate-item-contributiondebateitem')
contribution_objects = list()

for contribution in contributions:
    contribution_objects.append(Contribution(contribution))

print(contribution_objects)

paragraphs = contributions[4].find_all('p')
#print(paragraphs[0].get_text())

#Useful

# <div class="primary-text">The Prime Minister</div>
# <span class="sr-only">Share contribution 5 on</span>
# <div class="content">
# <p class="">I first have to say yes, indeed, we have had a busy day because this Government, unlike the last Government, are governing in the interests of the people of this country. Secondly, the windfall tax will not harm pensioners at all. What did, however, harm pensioners was the last Government's imposition of VAT on fuel. It is precisely for that reason that we propose cutting it.</p>
# </div>
