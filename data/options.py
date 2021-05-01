import json

ERROR = "Ekki er hægt að bæta við tagi!"

# Uncomment for MIM-GOLD tagset
tagset_file = 'data/mim_gold20_05/markamengi.json'

# Uncomment for IFD tagset
# tagset_file = 'data/markamengi.json'

with open(tagset_file) as j_file:
    tag_dict = json.load(j_file)

def show_option(tag:str, tag_sets:dict, lookah=1)->dict:

    max_length = tag_sets['max_len']

    if not tag:
        option = tag_sets['PoS']
        return option

    if tag[:2] in tag_sets['forked_tags']:
        for i in range(max_length):
            if len(tag)-lookah == i:
                flokkur = tag_sets['forked_tags'][tag[:2]][i]
                option = tag_sets[flokkur]
                return option

    
    for i in range(max_length):
        if len(tag)-lookah == i:
            option = tag_sets[tag_sets[tag[0]][i]]
            return option

    return ERROR

def extend_tag(tag:str, tag_set:dict):

    expanded_tag = {}
    if not tag:
        return None

    pos = tag[0]
    expanded_tag['PoS'] = tag_set['PoS'][pos]
    pos_list = tag_set[pos]

    if len(tag) > 1:
        index = 0
        pos_list = tag_set['forked_tags'][tag[:2]] if tag[:2] in tag_set['forked_tags'] else pos_list

        for letter in tag[1:]:
            expanded_tag[pos_list[index]] = tag_set[pos_list[index]][letter].capitalize()
            index += 1
    
    return expanded_tag



    
if __name__ == '__main__': 
    test_tag = 'a'

    ex_tag = extend_tag(test_tag, tag_dict)

    print(ex_tag)

    try:
        option = show_option(test_tag, tag_dict)
    except IndexError:
        option = ERROR

    print(option)
