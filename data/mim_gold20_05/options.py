import json

ERROR = "Ekki er hægt að bæta við tagi!"

with open('data/MIM-GOLD20_05/markamengi.json') as j_file:
    tag_dict = json.load(j_file)

def show_option(tag:str, tag_sets:dict)->dict:

    if not tag:
        option = tag_sets['Orðflokkur']
        return option
    
    elif len(tag) == 1:
        option = tag_sets[tag_sets[tag][0]]
        return option

    elif len(tag) >= 2 and tag.startswith('sþ'):
        if len(tag) == 2:
            option = tag_sets[tag_sets['sþ'][0]]
            return option
        
        elif len(tag) == 3:
            option = tag_sets[tag_sets['sþ'][1]]
            return option
        
        if len(tag) == 4:
            option = tag_sets[tag_sets['sþ'][2]]
            return option
        
        if len(tag) == 5:
            option = tag_sets[tag_sets['sþ'][3]]
            return option
    
    elif len(tag) == 2:
        option = tag_sets[tag_sets[tag[0]][1]]
        return option
    
    elif len(tag) == 3:
        option = tag_sets[tag_sets[tag[0]][2]]
        return option
    
    elif len(tag) == 4:
        option = tag_sets[tag_sets[tag[0]][3]]
        return option

    elif len(tag) == 5:
        option = tag_sets[tag_sets[tag[0]][4]]
        return option
    
    else:
        option = ERROR
        return option
    

if __name__ == '__main__': 
    test_tag = 'k'
    try:
        option = show_option(test_tag, tag_dict)
    except IndexError:
        option = ERROR

    print(option)
