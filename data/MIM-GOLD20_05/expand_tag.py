# Code recieved from Stofnun Árna Magnússonar, used on their website http://malvinnsla.arnastofnun.is/
# With small changes to encompany the main program code

FS_MAPPING = {'a':'stýrir ekki falli', 'f':'stýrir falli'}
KYN_MAPPING = {'k':'karlkyn', 'v':'kvenkyn', 'h':'hvorugkyn'}
TALA_MAPPING = {'e':'eintala', 'f':'fleirtala'}
FALL_MAPPING = {'n':'nefnifall', 'o':'þolfall', 'þ':'þágufall', 'e':'eignarfall'}
SN_MAPPING = {'m':'mannsnafn', 'ö':'örnefni', 's':'önnur sérnöfn'}
BEYGING_MAPPING = {'s':'sterk beyging', 'v':'veik beyging', 'o':'óbeygt'}
STIG_MAPPING = {'f':'frumstig', 'm':'miðstig', 'e':'efstastig'}
FNF_MAPPING = {'a':'ábendingarfornafn', 'b':'óákveðið ábendingarfornafn', 'e':'eignarfornafn', 'o':'óákveðið fornafn', 'p':'persónufornafn', 's':'spurnarfornafn', 't':'tilvísunarfornafn'}
HATTUR_MAPPING = {'n':'nafnháttur', 'b':'boðháttur', 'f':'framsöguháttur', 'v':'viðtengingarháttur', 's':'sagnbót', 'l':'lýsingarháttur nútíðar', 'þ':'lýsingarháttur þátíðar'}
MYND_MAPPING = {'g':'germynd', 'm':'miðmynd'}
TID_MAPPING = {'n':'nútíð', 'þ':'þátíð'}
TOF_MAPPING = {'f':'frumtala', 'a':'ártöl og fleiri óbeygjanlegar tölur', 'p':'prósentutölur', 'o':'fjöldatölur framan við hundrað og þúsund'}
PUNKT_MAPPING= {'l':'lok setningar', 'k':'komma','g':'gæsalappir','a':'önnur greinarmerki'}
POS = 'orðflokkur'
CASE_GOV = 'fallstjórn'
COMP = 'stig'
SUBCATEGORY = 'undirflokkur'
INFLECTION = 'beyging'
ARTICLE = 'greinir'
PROPER_NOUN = 'sérnöfn'
MOOD = 'háttur'
TENSE = 'tíð'
PERSON = 'persóna'
NUMBER = 'tala'
VOICE = 'mynd'
GENDER = 'kyn'
CASE = 'fall'

def expand_tag(tag):
    expanded_tag = {}
    if not tag:
        expanded_tag = None 
    if tag[0] == "p":
        expanded_tag[POS]="greinarmerki"
        expanded_tag[SUBCATEGORY]=PUNKT_MAPPING[tag[1]] if tag[1] in PUNKT_MAPPING.keys() else None
    elif tag[0]=='x':
        expanded_tag[POS]="ógreint"
    elif tag[0]=='e':
        expanded_tag[POS]="erlent orð"
    elif tag[0]=='a':
        if tag[1]=='u':
            expanded_tag[POS]="upphrópun"
        else:
            expanded_tag[POS]="atviksorð"
            expanded_tag[CASE_GOV]=FS_MAPPING[tag[1]] if tag[1] in FS_MAPPING.keys() else None
            if len(tag)==3:
                expanded_tag[COMP]=STIG_MAPPING[tag[2]]
    elif tag[0]=='c':
        if len(tag)==2 and tag[1]=='n':
            expanded_tag[POS]="nafnháttarmerki"
        else:
            expanded_tag[POS]="samtenging"
            if len(tag)==2:
                expanded_tag[SUBCATEGORY]="tilvísunartenging"
    elif tag[0] in "nlg":
        expanded_tag[GENDER] = KYN_MAPPING[tag[1]]
        expanded_tag[NUMBER] = TALA_MAPPING[tag[2]]
        expanded_tag[CASE] = FALL_MAPPING[tag[3]]
        if tag[0]=='n':
            expanded_tag[POS]="nafnorð"
            if len(tag)>4 and tag[4]=='g':
                expanded_tag[ARTICLE]='með viðskeyttum greini'
            elif len(tag)>5:
                expanded_tag[PROPER_NOUN]=SN_MAPPING[tag[5]]
        elif tag[0]=='l':
            expanded_tag[POS]='lýsingarorð'
            expanded_tag[INFLECTION]=BEYGING_MAPPING[tag[4]]
            expanded_tag[COMP]=STIG_MAPPING[tag[5]]
        elif tag[0]=='g':
            expanded_tag[POS]='greinir'
        else:
            print("{} EKKI FLOKKAÐ".format(tag))
    elif tag[0]=='f':
        expanded_tag[POS]="fornafn"
        expanded_tag[SUBCATEGORY]=FNF_MAPPING[tag[1]]
        if tag[2] in '12':
            expanded_tag[PERSON]='{}. persóna'.format(tag[2])
        else:
            expanded_tag[PERSON]='3. persóna'
            expanded_tag[GENDER]=KYN_MAPPING[tag[2]]
        expanded_tag[NUMBER]=TALA_MAPPING[tag[3]]
        expanded_tag[CASE]=FALL_MAPPING[tag[4]]
    elif tag[0]=='s':
        expanded_tag[POS]="sagnorð"
        expanded_tag[MOOD]=HATTUR_MAPPING[tag[1]]
        expanded_tag[VOICE]=MYND_MAPPING[tag[2]]
        if tag[1] in 'lns':
            if len(tag) == 6:
                expanded_tag[TENSE] = TID_MAPPING[tag[5]]
        elif tag[1] != 'þ':
            expanded_tag[PERSON]='{}. persóna'.format(tag[3])
            expanded_tag[NUMBER]=TALA_MAPPING[tag[4]]
            expanded_tag[TENSE] = TID_MAPPING[tag[5]]
        else:
            expanded_tag[GENDER]=KYN_MAPPING[tag[3]]
            expanded_tag[NUMBER]=TALA_MAPPING[tag[4]]
            expanded_tag[CASE]=FALL_MAPPING[tag[5]]
    elif tag[0]=='t':
        expanded_tag[POS]="töluorð"
        expanded_tag[SUBCATEGORY]=TOF_MAPPING[tag[1]]
        if tag[1] not in 'aop':
            expanded_tag[GENDER]=KYN_MAPPING[tag[2]]
            expanded_tag[NUMBER]=TALA_MAPPING[tag[3]]
            expanded_tag[CASE]=FALL_MAPPING[tag[4]]


    return expanded_tag
