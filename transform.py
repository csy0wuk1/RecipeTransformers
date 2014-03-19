import pprint
import NLPtool

class IngredObj:
# holds the original name and some associated attributes of an ingredient
    #name
    #nutri
    #cuisine
    def __init__(self, Name):
        self.name = Name
        self.nutri = set()
        self.cuisine = set()
    def print_info(self, tab=''):
        print tab, 'name:     ', self.name
        print tab, 'nutrition:', self.nutri
        print tab, 'cuisine:  ', self.cuisine
#


def txt2attr_list(folder, attr_names, Dict):
# Read the lists for all the attribute names passed in
# folder    = path
# attr_name = file name & attribute name 
    for attr_name in attr_names:
        tmp = []
        filename = folder + '\\' + attr_name + '.txt'
        with open(filename, 'r') as f:
            for line in f:
                ingreds = line.split('/')
                # some ingredients are separated by '/'
                for ingred in ingreds:
                    tmp.append(ingred.lower().rstrip().lstrip())
        Dict[attr_name] = tmp
#
    


def add_nutrition(nutritions, ingred_attr):
# Make the diagram of each ingredient and all
# its associated attributes
    for nutri_name in nutritions:
        nutrition = nutritions[nutri_name]
        for ingred in nutrition:
            ID = NLPtool.uni_rep(ingred)
            # Make unique identifier to merge similar 
            # representations of the same ingredient
            if ID not in ingred_attr:
                ingred_attr[ID] = IngredObj(ingred) # Point ID to a new ingredient object, with name ingred
            ingred_attr[ID].nutri.add(nutri_name)
            #ingred_attr[ID].print_info()
#


def add_cuisine(cuisines, ingred_attr, thrown_list):
    for cuisine_name in cuisines:
        cuisine = cuisines[cuisine_name]
        for ingred in cuisine:
            ID = NLPtool.uni_rep(ingred)
            # Make unique identifier to merge similar 
            # representations of the same ingredient
            if ID not in ingred_attr:
                thrown_list.append(cuisine_name+': '+ingred)
            else:
                ingred_attr[ID].cuisine.add(cuisine_name)
                #ingred_attr[ID].print_info()
#


def load_knowledge_base(nutritions, cuisines):
    global path
    nutri_names = ['protein', 'spice', 'vegetables','meat','grain','protein','fruit','fats_oils']
    cuisine_names = ['french','indian','italian']
    txt2attr_list(path + 'nutrition categories', nutri_names, nutritions)
    #pprint.pprint(nutritions)
    txt2attr_list(path + 'cuisines', cuisine_names, cuisines)
    #pprint.pprint(cuisines)
#


def build_table(ingred_attr, nutritions, cuisines, thrown_list):
    add_nutrition(nutritions, ingred_attr)
    add_cuisine(cuisines, ingred_attr, thrown_list)
    print len(ingred_attr), '\n'
    #pprint.pprint(ingred_attr)
#
def learn_ingredients(ingred_attr, nutritions, cuisines, thrown_list):
    load_knowledge_base(nutritions, cuisines)
    build_table(ingred_attr, nutritions, cuisines, thrown_list)
    #pprint.pprint(thrown_list)
#
def naive_transform(from_ingreds, to_cuisine_name, cuisines, ingred_attr, mute = False):
# Give a valid transformation
    out_list = []
    target_cuisine = cuisines[to_cuisine_name]
    for ingred in from_ingreds:
        fromID = NLPtool.uni_rep(ingred)
        # To use the id instead of the actual name,
        # because all ingredients are stored by id in dictionary ingred_attr
        if fromID not in ingred_attr:
            if not mute:
                print 'Ingredient', ingred, "not identified: left unchanged"
            out_list.append(ingred)
        else:
            substitute = 'NOT FOUND'
            NUTRI = ingred_attr[fromID].nutri
            for cand in target_cuisine:
                candID = NLPtool.uni_rep(cand)
                if candID in ingred_attr and \
                        NUTRI.intersection(ingred_attr[candID].nutri) != set() and \
                        cand not in out_list:
                    substitute = cand
                    break
            if substitute == 'NOT FOUND':
                if not mute:
                    print "Substitue for", ingred, "not found: left unchanged"
                substitute = ingred
            out_list.append(substitute)
    out_list = list(set(out_list)) # get rid of possible duplicates
    return out_list
#


def whatis(ingred):
    global ingred_attr
    ID = NLPtool.uni_rep(ingred)
    if ID in ingred_attr:
        ingred_attr[ID].print_info()
    else:
        print ingred, 'not found in database'
#



# ENTRY POINT
path = '.\\'     # CHANGE HERE if path for data folders are changed
nutritions = {}
cuisines = {}
ingred_attr = {}
thrown_list = []
learn_ingredients(ingred_attr, nutritions, cuisines, thrown_list)
print naive_transform(['pork','lamb','salt','deep south dry rub'], 'french', cuisines, ingred_attr)
print ''
print naive_transform(['skinless, boneless chicken breasts', 'garlic', \
                        'balsamic vinegar', 'chicken broth', 'mushrooms', \
                        'all-purpose flour', 'olive oil', 'butter', \
                        'dried thyme', 'bay leaf'], 'french', cuisines, ingred_attr)

