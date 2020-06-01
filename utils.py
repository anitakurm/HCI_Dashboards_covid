import pandas as pd
import re


def column_to_question(df = None, return_df = True, lang = 'da'):
    """Renames and keeps only the columns specified in the codebook """

    if lang == 'da':
        codebook = dict(
                    ActualSurveyStartTime = "Time",
                    #q1 = "Kan du med dine egne ord beskrive, hvad du tænker om den nuværende situation med corona-virussen?",
                    #q2 = "Kan du med dine egne ord beskrive, hvordan du tænker, vi kommer ud af den nuværende situation med corona-virussen?",
                    q3 = "I hvilken grad frygter du konsekvenserne af den nuværende situation med corona-virussen?",
                    q4 = "I hvilken grad er du optimistisk i forhold til at Danmark indenfor den nærmeste fremtid kan få kontrol over coronavirussen?",
                    q5 = "I hvilken grad føler du, at du har tilstrækkelig viden om, hvordan du undgår at blive smittet og/eller at smitte andre med corona-virussen?",
                    q6 = "I hvilken grad føler du, at du har tilstrækkelig viden om de symptomer, som corona-virussen giver?",
                    q7 = "I hvilken grad føler du, at du har tilstrækkelig viden om, hvordan du skal forholde dig, hvis du bliver syg af coronavirussen?",
                    q8 = "I hvilken grad føler du, at du har tilstrækkelig viden om, hvordan du som borger bør forholde dig til coronavirussen?",
                    q8A = "Hvor enig eller uenig er du i følgende udsagn: Jeg er sikker på, at jeg kan følge myndighedernes råd om at 'holde afstand' til andre, hvis jeg vil?",
                    q8B_1_resp = "Hvor enig eller uenig er du i følgende udsagn: Regeringen er handlekraftig",
                    q8B_2_resp = "Hvor enig eller uenig er du i følgende udsagn: Regeringen fører en politik, der gavner dansk økonomi",
                    q8B_3_resp = "Hvor enig eller uenig er du i følgende udsagn: Regeringen fører en politik, der er positiv for Danmark",
                    q8B_4_resp = "Hvor enig eller uenig er du i følgende udsagn: Regeringen fører den nødvendige politik for at håndtere corona-virussen",
                    q8C_1_resp = "På en skala fra 0 til 10, hvor stor tillid har du personligt til regeringen?",
                    q8D = "I hvilken grad oplever du, at der er enighed i udmeldingerne fra myndighederne om, hvordan du skal håndtere corona-virussen?",
                    q8E = "Hvor tilfreds eller utilfreds er du med myndighedernes beslutning om kun at teste meget syge for om de er smittet med corona-virus?",
                    # New page: Questions on what you did yesterday (compliance with regulations?)
                    q9 = "Hvor mange gange vil du anslå, at du vaskede dine hænder eller brugte håndsprit i går?",
                    q10_1 = "Hostede og/eller nøs du i går?",
                    q10_2 = "Da du hostede og/eller nøs i går, gjorde du det så i dit ærme hver gang?",
                    q11 = "Gav du et håndtryk til en anden person i går?",
                    q12 = "Krammede eller kyssede du en person udenfor din allernærmeste familie i går?",
                    q13 = "Købte du mere ind, end du plejer, i går?",
                    q14 = "Tog du offentlig transport i går?",
                    q15 = "Var du i et lokale med mere end 10 mennesker i går?",
                    q16 = "I hvilken grad var du i går opmærksom på at holde afstand til folk udenfor din allernærmeste familie?",
                    q17 = "Var du i går opmærksom på at holde afstand til ældre og kronisk syge?",
                    q18 = "I hvilken grad føler du, at den nuværende situation med corona-virussen har fået dig til at ændre adfærd for at undgå at sprede smitte?",
                    # Questions about own thoughts
                    q19_1_resp = "I hvilken grad er du bekymret for konsekvenserne af corona-virussen for dig selv?",
                    q19_2_resp = "I hvilken grad er du bekymret for konsekvenserne af corona-virussen for din familie?",
                    q19_3_resp = "I hvilken grad er du bekymret for konsekvenserne af corona-virussen for dine nære venner?",
                    q19_4_resp = "I hvilken grad er du bekymret for konsekvenserne af corona-virussen for det danske samfund?",
                    # Questions about daily life
                    q20_1_resp = "I hvilken grad har du været i kontakt med nære venner og/eller familie, som du ikke bor sammen med, den seneste uge?",
                    q20_2_resp = "I hvilken grad føler du, at du har spist sundt den seneste uge?",
                    q20_3_resp = "I hvilken grad føler du, at du har fået tilstrækkelig motion den seneste uge?",
                    q20_4_resp = "I hvilken grad føler du, at du står alene i den nuværende corona-situation?",
                    q21_1_resp = "Når alt tages i betragtning, hvor tilfreds er du så nu med dit liv som helhed?",
                    q22_1_resp = "Mener du, at de fleste mennesker i det store og hele er til at stole på, eller kan man ikke være for forsigtig, når man har med andre mennesker at gøre?",
                    q23_0_resp = "Har du den seneste uge oplevet hovedpine?",
                    q23_1_resp = "Har du den seneste uge oplevet ondt i halsen?",
                    q23_2_resp = "Har du den seneste uge oplevet feber?",
                    q23_3_resp = "Har du den seneste uge oplevet hoste?",
                    q23_4_resp = "Har du den seneste uge oplevet muskelømhed?",
                    q23_5_resp = "Har du den seneste uge oplevet åndenød?",
                    Block5_big5_1_1_resp = "Jeg ser mig selv som en person, der ofte er bekymret",
                    Block5_big5_1_2_resp = "Jeg ser mig selv som en person, der let bliver nervøs",
                    Block5_big5_1_3_resp = "Jeg ser mig selv som en person, der er god til at holde hovedet koldt i pressede situationer",
                    Block5_big5_1_4_resp = "Jeg ser mig selv som en person, der godt kan lide at snakke",
                    Block5_big5_1_5_resp = "Jeg ser mig selv som en person, der er udadvendt og selskabelig",
                    Block5_big5_1_6_resp = "Jeg ser mig selv som en person, der er socialt reserveret",
                    Block5_big5_2_7_resp = "Jeg ser mig selv som en person, der får mange nye ideer",
                    Block5_big5_2_8_resp = "Jeg ser mig selv som en person, der påskønner kunst og æstetik",
                    Block5_big5_2_9_resp = "Jeg ser mig selv som en person, der har en levende fantasi og kan forstille mig ting, som endnu ikke findes",
                    Block5_big5_2_10_resp = "Jeg ser mig selv som en person, der sommetider er uhøflig over for andre",
                    Block5_big5_2_11_resp = "Jeg ser mig selv som en person, der er tilgivende over for andre",
                    Block5_big5_2_12_resp = "Jeg ser mig selv som en person, der er hensynsfuld og venlig over for næsten alle",
                    Block5_big5_2_13_resp = "Jeg ser mig selv som en person, der er omhyggelig og grundig",
                    Block5_big5_2_14_resp = "Jeg ser mig selv som en person, der er lidt doven",
                    Block5_big5_2_15_resp = "Jeg ser mig selv som en person, der er effektiv når jeg gør noget",
                    bagg1 = "Køn",
                    alder = "Alder",
                    alder_kat_det = "Alder (kategorier 1)",
                    alder_kat = "Alder (kategorier 2)",
                    køn_alder = "Køn-alder gruppe",
                    #bagg3_postnummer = "Location postnummer: DK",
                    region = "Location Region: DK",
                    #kommune = "Location Kommune: DK",
                    storkreds = "Location Storkreds: DK",
                    bagg3_o1 = "Location: UK",
                    bagg3_FR_o1 = "Location: FR",
                    bagg4 = "Antal personer over 18 i husstanden",
                    person = "Antal personer over 18 i husstanden (kategorier)",
                    #bagg5 = "Højst gennemførte uddannelse: DK",
                    #bagg5_DE_a = "Højst gennemførte uddannelse kategorier a: DE",
                    #bagg5_DE_b = "Højst gennemførte uddannelse kategorier b: DE",
                    #bagg5_DE_c = "Højst gennemførte uddannelse kategorier c: DE",
                    #uddannelse2 = "Højst gennemførte uddannelse kategorier #1: DK",
                    uddannelse_det= "Højst gennemførte uddannelse kategorier #2: DK",
                    uddannelse2_SVE = "Højst gennemførte uddannelse: SVE",
                    uddannelse2_ITA = "Højst gennemførte uddannelse: ITA",
                    uddannelse2_UK = "Højst gennemførte uddannelse: UK",
                    uddannelse2_US = "Højst gennemførte uddannelse: US",
                    uddannelse2_FR = "Højst gennemførte uddannelse: FR",
                    uddannelse2_DE = "Højst gennemførte uddannelse: FR",
                    uddannelse2_HU = "Højst gennemførte uddannelse: HU",
                    bagg5_UK_a = "Højst gennemførte uddannelse:UK a",
                    bagg5_UK_b = "Højst gennemførte uddannelse: UK b",
                    Bagg_børn = "Antal hjemmeboende børn",
                    bagg_civilstand = "Civilstand",
                    bagg_beskaeftigelse = "Nuværende beskæftigelse",
                    Bagg_indkomst_pers = "Årsindkomst brutto",
                    bagg8 = "Hvad stemte du ved sidste folketingsvalg?",
                    party_SVE = "Hvad stemte du ved sidste valg: SVE",
                    party_UK = "Hvad stemte du ved sidste valg: UK",
                    party_US = "Hvad stemte du ved sidste valg: US",
                    #bagg8_ITA = "Hvad stemte du ved sidste valg (italiensk): ITA",
                    party_ITA = "Hvad stemte du ved sidste valg: ITA",
                    party_FR =  "Hvad stemte du ved sidste valg: FR",
                    party_DE = "Hvad stemte du ved sidste valg: DE",
                    party_HU = "Hvad stemte du ved sidste valg: DE",
                    bagg9 = "Type af bolig",
                    husstand = "Type af bolig kategorier",
                    NUTS1_SVE = "Location NUTS1: SVE",
                    Laan_SVE = "Location Laan SVE",
                    Riksomraaden_SVE = "Location Region: SVE",
                    NUTS1_ITA =  "Location: ITA",
                    NUTS2_ITA = "Location 2: ITA",
                    NUTS3_ITA = "Location 3: ITA",
                    NUTS1_UK = "Location: UK",
                    NUTS1_US = "Location: US",
                    NUTS1_FR = "Location: FR",
                    NUTS1_DE = "Location: DE",
                    NUTS1_HU = "Location: HU",
                    kommune = "Kommune",
                    country = "Country"
        )
    if lang == 'en':
        codebook = dict(country = "Country",
                    q1 = "Can you describe in your own words what you think of the current situation with the coronavirus?",
                    q2 = "Can you describe in your own words how you think we will get out of the current situation with the coronavirus?",
                    q3 = "To what degree do you fear the consequences of the current situation with the coronavirus?",
                    q4 = "How optimistic are you that your country will be able to get the coronavirus under control in the near future?",
                    q5 = "To what degree do you feel that you know enough about how to avoid being infected and/or infecting others with the coronavirus?",
                    q6 = "To what degree do you feel that you know enough about the symptoms of the coronavirus?",
                    q7 = "To what degree do you feel that you know enough about what you should do if you fall ill with the coronavirus?",
                    q8 = "To what degree do you feel that you know enough about what you as a citizen should do in relation to the coronavirus?",
                    q8A = "To what extent do you agree or disagree with the following statement: I'm certain I can follow official advice to 'distance myself' from others if I want to.",
                    q8B_1_resp = "To what extent do you agree or disagree with the following statement: The government is decisive",
                    q8B_2_resp = "To what extent do you agree or disagree with the following statement: The government conducts a policy that can benefit the country's economy",
                    q8B_3_resp = "To what extent do you agree or disagree with the following statement: The government conducts a policy that is positive for the country",
                    q8B_4_resp = "To what extent do you agree or disagree with the following statement: The governemnt conducts the policy necessary to handle the coronavirus",
                    q8C_1_resp = "On a scale from 0 to 10, how much confidence do you personally have in the government?",
                    q8D = "To what extent do you feel there is a consensus in the government's statements on how to deal with the coronavirus?",
                    q8E = "How satisfied or dissatisfied are you with the authorities' decision to only test very ill for whether they are infected with coronavirus?",
                    # New page: Questions on what you did yesterday (compliance with regulations?)
                    q9 = "How many times do you estimate that you washed your hands or used hand sanitiser yesterday?",
                    q10_1 = "Did you cough and/or sneeze yesterday?",
                    q10_2 = "When you coughed and/or sneezed yesterday, did you do this in your sleeve each time?",
                    q11 = "Did you shake someone's hand yesterday?",
                    q12 = "Did you hug or kiss someone outside your closest family yesterday?",
                    q13 = "Did you buy more than you usually do, yesterday?",
                    q14 = "Did you use public transport yesterday?",
                    q15 = "Were you in a room with more than 10 people yesterday?",
                    q16 = "To what degree were you careful yesterday to keep your distance from people outside your closest family?",
                    q17 = "Were you careful yesterday to keep your distance from elderly and chronically ill people?",
                    q18 = "To what degree do you feel that the current situation with the coronavirus has made you change your behaviour to avoid spreading infection?",
                    # Questions about own thoughts
                    q19_1_resp = "To what degree are you concerned about the consequences of the coronavirus for yourself?",
                    q19_2_resp = "To what degree are you concerned about the consequences of the coronavirus for your family",
                    q19_3_resp = "To what degree are you concerned about the consequences of the coronavirus for your close friends?",
                    q19_4_resp = "To what degree are you concerned about the consequences of the coronavirus for your country?",
                    # Questions about daily life
                    q20_1_resp = "To what degree have you been in contact with close friends and/or family with whom you do not live, during the past week?",
                    q20_2_resp = "To what degree do you feel you have eaten healthily during the past week?",
                    q20_3_resp = "To what degree do you feel you have taken enough exercise during thepast week?",
                    q20_4_resp = "To what degree do you feel that you stand alone in the current Corona situation?",
                    q21_1_resp = "Taking everything into consideration, how satisfied are you now with your life overall?",
                    q22_2_resp = "Do you think that most people by and large are to be trusted, or that you cannot be too careful when it comes to other people?",
                    q23_0_resp = "During the past week, have you experienced headache?",
                    q23_1_resp = "During the past week, have you experienced sore throat?",
                    q23_2_resp = "During the past week, have you experienced fever?",
                    q23_3_resp = "During the past week, have you experienced cough?",
                    q23_4_resp = "During the past week, have you experienced sore muscles?",
                    q23_5_resp = "Have you experienced shortness of breath over the past week?",
                    Block5_big5_1_1_resp = "I see myself as a person who is often concerned",
                    Block5_big5_1_2_resp = "I see myself as a person who easily gets nervous",
                    Block5_big5_1_3_resp = "I see myself as someone who is good at keeping my head cold in stressful situations",
                    Block5_big5_1_4_resp = "I see myself as a person who likes to talk",
                    Block5_big5_1_5_resp = "I see myself as an outgoing and sociable person",
                    Block5_big5_1_6_resp = "I see myself as a socially reserved person",
                    Block5_big5_2_7_resp = "I see myself as someone who gets many new ideas",
                    Block5_big5_2_8_resp = "I see myself as a person who appreciates art and aesthetics",
                    Block5_big5_2_9_resp = "I see myself as someone who has a vivid imagination and can imagine things that do not yet exist",
                    Block5_big5_2_10_resp = "I see myself as someone who is sometimes rude to others",
                    Block5_big5_2_11_resp = "I see myself as someone who is forgiving of others",
                    Block5_big5_2_12_resp = "I consider myself a person who is considerate and kind to almost everyone",
                    Block5_big5_2_13_resp = "I see myself as a person who is careful and thorough",
                    Block5_big5_2_14_resp = "I consider myself a bit lazy",
                    Block5_big5_2_15_resp = "I see myself as an effective person when I do something",
                    age = "Age",
                    age_cat_det = "Age (categories 1)",
                    age_cat = "Age (categories 2)",
                    gender_alder = "Gender-age group",
                    bagg1 = "Gender",
                    bagg2_2 = "Age (range)",
                    #bagg3_postnumber = "Location postcode: DK",
                    region = "Location Region: DK",
                    municipality = "Location Municipality: DK",
                    storkreds = "Location Storkreds: DK",
                    bagg3_o1 = "Location: UK",
                    bagg3_FR_o1 = "Location: FR",
                    bagg4 = "How many people over the age of 18 live in your household",
                    person = "How many people over the age of 18 live in your household (categories)",
                    bagg5 = "Highest education: DK",
                    bagg5_DE_a = "Highest Education Categories a: DE",
                    bagg5_DE_b = "Highest Education Category B: DE",
                    bagg5_DE_c = "Highest education categories c: DE",
                    education2 = "Highest completed education categories # 1: DK",
                    education_det = "Highest education category # 2: DK",
                    education2_SVE = "Highest Education: SVE",
                    education2_ITA = "Highest Education: ITA",
                    education2_UK = "Highest Education: UK",
                    education2_US = "Highest Education: US",
                    education2_FR = "Highest Education: FR",
                    education2_DE = "Highest Education: FR",
                    education2_HU = "Highest Education: HU",
                    bagg5_UK_a = "Highest Education: UK a",
                    bagg5_UK_b = "Highest Education: UK b",
                    Bagg_børn = "How many home-dwelling children, including any cohabiting children, live with you?",
                    bagg_civilstand = "Civil status",
                    bagg_employment = "Current Employment",
                    Bagg_indkomst_pers = "Gross annual income",
                    bagg8 = "What did you vote for at the last general election?",
                    party_SVE = "What did you vote for last election: SVE",
                    party_UK = "What did you vote for last election: UK",
                    party_US = "What did you vote for last election: US",
                    # bagg8_ITA = "What did you vote for last election (Italian): ITA",
                    party_ITA = "What did you vote for last election: English",
                    party_FR = "What did you vote for last election: FR",
                    party_DE = "What did you vote for last election: DE",
                    party_HU = "What did you vote for last election: DE",
                    bagg9 = "Type of accommodation",
                    household = "Type of housing categories",
                    NUTS1_SVE = "Location NUTS1: CPU",
                    Lane_SVE = "Location Lane CPU",
                    Riksomraaden_SVE = "Location Region: SVE",
                    NUTS1_ITA = "Location: ITA",
                    NUTS2_ITA = "Location 2: ITA",
                    NUTS3_ITA = "Location 3: ITA",
                    NUTS1_UK = "Location: UK",
                    NUTS1_US = "Location: US",
                    NUTS1_FR = "Location: FR",
                    NUTS1_DE = "Location: DE",
                    NUTS1_HU = "Location: HU"
                )

    
    if return_df:
        df = df[codebook.keys()]
        df = df.rename(columns = codebook)
        df = df[codebook.values()]
        return df
    
    else:
        return codebook

###
# Q21 formatting sucks (range 0 - 10 but 0 and 10 are specific strings)
###


def binning(df, col, vals=[], return_all = True, no_grouping = False, group_by = 'date'):
    """
    Find the percentage of people who answered the specific question
    with the given answers

    Requires a date column
    
    df: dataframe
    col: the column of interest
    vals: the answers to calculate percentages of 

    Usage example:
    
        df = pd.read_json("data/corona_survey_20200320.JSON")
        df.loc[:, 'date'] = df.ActualSurveyStartTime.map(lambda x: x.split()[0])

        col = "q3"
        vals = ["I høj grad", "I nogen grad"]    

        binning(df, col, vals)
        >>>	
            date	    percent
        0	2020-03-13	74.615385
        1	2020-03-14	76.655629
        2	2020-03-15	79.232112
        3	2020-03-16	83.359253
        4	2020-03-17	84.185493
        5	2020-03-18	84.928717
        6	2020-03-19	84.860558
    """

    if return_all:
        if no_grouping:
            percentages= pd.DataFrame({'percent' : df[col].\
                value_counts(normalize = True) * 100}).\
                reset_index()

        else:
            percentages = pd.DataFrame({'percent' : df.groupby(group_by)[col].\
                value_counts(normalize = True) * 100}).\
                reset_index()
        
        return percentages

    else:
        if isinstance(vals, str):
            vals = [vals]

        subset = percentages.loc[percentages[col].isin(vals)].\
            groupby('date').sum().\
            reset_index()

        return subset


#pre-processing function
def load_preprocess(df_path, lang_input = "da"):
    """
    Loads a json file from the given path;
    Applies column_to_question() function defined above;
    Aggregates certain groups of columns;
    Creates new columns: reformatting and aggreagation of certain groups of columns
    Drops columns that have been aggregated (to save space)

    Note to self on column aggregation:
        Extracts several groups of columns ('uddannelse' for education, 'stemte' for political party, 'location' for location),
        and merges every group into one column (takes the first non-null value in every row using bfill())
    """
    if df_path.endswith("json"):
        df = pd.read_json(df_path)
    else:
        df = pd.read_csv(df_path)
    df = column_to_question(df, lang = lang_input)
    df.loc[:, 'Date'] = df['Time'].map(lambda x: x.split()[0])
    edu_columns= [k for k in df.columns if 'uddannelse' in k]
    party_columns = [k for k in df.columns if 'stemte' in k]
    location_columns = [k for k in df.columns if 'Location' in k]
    df['Uddannelse'] = df[edu_columns].bfill(axis=1).iloc[:, 0].fillna('unknown')
    df['Valgstemme'] = df[party_columns].bfill(axis=1).iloc[:, 0].fillna('unknown')
    df['Beliggenhed'] = df[location_columns].bfill(axis=1).iloc[:, 0].fillna('unknown')
    df['Indkomst_min'] =  df['Årsindkomst brutto'].map(lambda x: re.findall(r'^\d{1,3}.\d{3}\.?\d?\d?\d?', x) if x not in ['Ved ikke', 'Under 100.000 kr.'] else x)
    df['Indkomst_min'] = df['Indkomst_min'].replace({'Under 100.000 kr.':'0', "Ved ikke": "0"})
    df['Indkomst_min'] = df['Indkomst_min'].map(lambda x: [i.replace(".","") for i in x])
    df['Indkomst_min'] = df['Indkomst_min'].map(lambda x: int(x[0]))
    df['Antal personer over 18 i husstanden'] = df['Antal personer over 18 i husstanden'].map(lambda x: [int(s) for s in x.split() if s.isdigit()][0])
    df['Antal hjemmeboende børn'] = df['Antal hjemmeboende børn'].replace({"Jeg har ingen hjemmeboende børn": '0'})
    df['Antal hjemmeboende børn'] = df['Antal hjemmeboende børn'].map(lambda x: [int(s) for s in x.split() if s.isdigit()][0])
    df['Alder'] = df['Alder'].fillna(0)
    df = df.drop(edu_columns, axis = 1)
    df = df.drop(party_columns, axis = 1)
    df = df.drop(location_columns, axis = 1)
    return df


#define data filtering function
def filter_dataframe(df, country_values, gender_values, age_values, income_values, kids_values, maritalstatus, occupation, housing, education):
    """ Function tailored for filtering callback in the app """
    dff = df[
        df['Country'].isin(country_values)
        & df['Køn'].isin(gender_values)
        & (df['Alder'] >= age_values[0])
        & (df['Alder'] <= age_values[1])
        & (df['Indkomst_min'] >= income_values[0])
        & (df['Indkomst_min'] < income_values[1])
        & (df['Antal hjemmeboende børn'] >= kids_values[0])
        & (df['Antal hjemmeboende børn'] <= kids_values[1])
        & df['Civilstand'].isin(maritalstatus)
        & df['Nuværende beskæftigelse'].isin(occupation)
        & df['Type af bolig kategorier'].isin(housing)
        & df['Uddannelse'].isin(education)
        #& df['partivalg_sidste_fv'].isin(party)
        ]

    return dff


def get_vals_opts(datacolumn):
    """Takes in a column in format df['Columnname']
    and provides a list of unique values as well as a dictionary suited for dcc.dropdown component """
    col_values = datacolumn.fillna('Not specified').unique().tolist()
    col_values.sort()
    col_options = [{'label': i, 'value': i} for i in col_values]
    return col_values, col_options
