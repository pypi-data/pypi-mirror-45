def loadneptun(versionNumber):  
    import pandas as pd 
    
    df = pd.read_csv(f"https://github.com/bradib0y/neptun_db/raw/master/neptun_db_v{versionNumber}.csv", sep="\t", encoding="utf-8")
    
    df.set_index(['Key', 'FélévSorszám'], inplace=True)

    df['KépzésStátusz'] = df['KépzésStátusz'].astype('category')
    df['FélévesStátusz'] = df['FélévesStátusz'].astype('category')
    df['Pénzügyi státusz'] = df['Pénzügyi státusz'].astype('category')
    df['Képzési szint'] = df['Képzési szint'].astype('category')
    df['Modulkód'] = df['Modulkód'].astype('category')
    df['Tagozat'] = df['Tagozat'].astype('category')
    df['Nem'] = df['Nem'].astype('category')
    df['Irányítószám'] = df['Irányítószám'].astype('category')

    return df

if __name__ == "__main__":
    import sys
    loadneptun(int(sys.argv[0]))
