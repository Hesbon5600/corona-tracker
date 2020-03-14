from django_countries import countries


def countries_(country):
    """
    return the country's ISO names
    Args:
        country (str): the country name
    Returns:
        (str) country ISO name
    """
    countries.countries['US'] = 'USA'
    countries.countries['GB'] = 'UK'
    countries.countries['AE'] = 'UAE'
    countries.countries['PS'] = 'Palestine'
    countries.countries['CD'] = 'DRC'
    countries.countries['CI'] = 'Ivory Coast'
    countries.countries['BL'] = 'St. Barth'
    countries.countries['VI'] = 'U.S. Virgin Islands'
    countries.countries['VA'] = 'Vatican City'
    countries.countries['CAR'] = 'CAR'
    countries.countries['KR'] = 'S. Korea'
    countries.countries['FO'] = 'Faeroe Islands'
    countries.countries['MF'] = 'Saint Martin'
    countries.countries['SVG'] = 'St. Vincent Grenadines'

    return countries.by_name(country)
