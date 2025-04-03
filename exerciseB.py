import pandas as pd
from collections import defaultdict


def extract_personal_data(file_path):
    df= pd.read_csv(file_path)
    return df


def add_parents(person, df_connections):
    df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], person["Fathеr_Id"], "אב"]
    df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], person["Mother_Id"], "אם"]


def add_children(person, df_connections):
    if person["Gender"]=="Male":
        df_connections.loc[len(df_connections)]= [person["Fathеr_Id"], person["Ρerson_Id"], "בן"]
        df_connections.loc[len(df_connections)]= [person["Mother_Id"], person["Ρerson_Id"], "בן"]
    else:
        df_connections.loc[len(df_connections)]= [person["Fathеr_Id"], person["Ρerson_Id"], "בת"]
        df_connections.loc[len(df_connections)]= [person["Mother_Id"], person["Ρerson_Id"], "בת"]


def add_spouse(person, df_connections):
    if person["Gender"] == "Male":
        df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], person["Spouѕe_Id"], "בת זוג"]
        df_connections.loc[len(df_connections)]= [person["Spouѕe_Id"], person["Ρerson_Id"], "בן זוג"]
    else:
        df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], person["Spouѕe_Id"], "בן זוג"]
        df_connections.loc[len(df_connections)]= [person["Spouѕe_Id"], person["Ρerson_Id"], "בת זוג"]


def add_siblings(person, df_connections, siblings):
    for sibling_id, s_gender in siblings:
        if s_gender=="Male":
            df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], sibling_id, "אח"]
        else:
            df_connections.loc[len(df_connections)]= [person["Ρerson_Id"], sibling_id, "אחות"]

        if person["Gender"]=="Male":
            df_connections.loc[len(df_connections)]= [sibling_id, person["Ρerson_Id"], "אח"]
        else:
            df_connections.loc[len(df_connections)]= [sibling_id, person["Ρerson_Id"], "אחות"]


def connections(file_path):
    df= extract_personal_data(file_path)
    df_connections= pd.DataFrame(columns=["Person_Id", "Relative_Id", "Connection_Type"])
    parents= defaultdict(list)
    spouses= set()

    for _, person in df.iterrows():
        add_parents(person, df_connections)

        add_children(person, df_connections)

        if pd.notna(person["Spouѕe_Id"]) and person["Spouѕe_Id"] not in spouses:
            add_spouse(person, df_connections)
            spouses.add(person["Ρerson_Id"])
            spouses.add(person["Spouѕe_Id"])

        if parents[person["Fathеr_Id"]] or parents[person["Mother_Id"]]:
            add_siblings(person, df_connections, set(parents[person["Fathеr_Id"]] + parents[person["Mother_Id"]]))

        parents[person["Fathеr_Id"]].append((person["Ρerson_Id"], person["Gender"]))
        parents[person["Mother_Id"]].append((person["Ρerson_Id"], person["Gender"]))

    return df_connections







if __name__=="__main__":
    file_path="personal_data.csv"
    df_connections= connections(file_path)
    print(df_connections)
    df_connections.to_csv("connections.csv", index=False, encoding='iso-8859-8')








