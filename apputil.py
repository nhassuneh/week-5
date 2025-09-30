import plotly.express as px
import pandas as pd
import numpy as np

# update/add code below ...
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

def survival_demographics(df=None):
    """
    Analyze survival patterns by passenger class, sex, and age group.
    
    Args:
        df: DataFrame containing Titanic passenger data
        
    Returns:
        DataFrame with survival statistics by demographic groups
    """

    if df is None:
        df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Lowercase column names for the sake of the autograder and my sanity
    df.columns = df.columns.str.lower()

    # Create age groups as categorical
    bins = [0, 12, 19, 59, np.inf]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)
    
    # Group by class, sex, and age group
    grouped = df.groupby(['pclass', 'sex', 'age_group'], dropna=False)
    
    # Calculate statistics
    result = grouped.agg(
        n_passengers=('passengerid', 'count'),
        n_survivors=('survived', 'sum')
    ).reset_index()
    
    # Create all combinations to include groups with no members
    all_combos = pd.MultiIndex.from_product(
        [[1, 2, 3], ['female', 'male'], labels],
        names=['pclass', 'sex', 'age_group']
    ).to_frame(index=False)
    
    # Merge and fill missing groups with 0
    result = (all_combos
        .merge(result, how='left', on=['pclass', 'sex', 'age_group'])
        .fillna({'n_passengers': 0, 'n_survivors': 0}))
    result['n_passengers'] = result['n_passengers'].astype(int)
    result['n_survivors'] = result['n_survivors'].astype(int)

    # Ensure age_group is categorical
    result['age_group'] = result['age_group'].astype(
        pd.CategoricalDtype(categories=labels, ordered=True)
    )
    
    # Calculate survival rate, and handle division
    result['survival_rate'] = result['n_survivors'] / result['n_passengers'].replace(0, np.nan)
    result['survival_rate'] = result['survival_rate'].fillna(0)
    
    # Sort for better readability
    result = result.sort_values(['pclass', 'sex', 'age_group'])
    
    return result


def visualize_demographic():
    """
    Visualize survival rates across different age groups.
    
    Returns:
        Plotly figure showing survival patterns
    """
    # Load data
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Get survival demographics
    data = survival_demographics(df)
    
    # Calculate average survival rate for each age group
    avg_by_age = data.groupby('age_group').agg(
        avg_survival_rate=('survival_rate', 'mean')
    ).reset_index()
    
    # Simple bar chart
    fig = px.bar(
        avg_by_age,
        x='age_group',
        y='avg_survival_rate',
        color='age_group',
    )

    fig.update_layout(
        title='Average Survival Rates by Age Group',
        xaxis_title='Age Group',
        yaxis_title='Average Survival Rate',
    )
    # Change the survival rates to percentages instead of decimals
    fig.update_yaxes(tickformat='.0%')
    
    return fig

def family_groups(df=None):
    """
    Explore the relationship between family size, passenger class, and ticket fare.
    
    Args:
        df: DataFrame containing Titanic passenger data
        
    Returns:
        DataFrame with family size statistics by passenger class
    """
    if df is None:
        df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Create family_size column: Adding the 1 for the passenger themselves
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    
    # Group by family size and passenger class
    grouped = df.groupby(['family_size', 'Pclass'])
    
    # Calculate statistics
    result = grouped.agg(
        n_passengers=('PassengerId', 'count'),
        avg_fare=('Fare', 'mean'),
        min_fare=('Fare', 'min'),
        max_fare=('Fare', 'max')
    ).reset_index()
    
    # Sort for better readability (by class, then family size)
    result = result.sort_values(['Pclass', 'family_size'])
    
    return result


def last_names(df=None):
    """
    Extract last names from the Name column and count occurrences.
    
    Args:
        df: DataFrame containing Titanic passenger data
        
    Returns:
        Series with last name as index and count as value
    """
    if df is None:
        df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

    # Extract last name (text before the first comma)
    last_names = df['Name'].str.split(',').str[0]
    
    # Count occurrences of each last name
    last_name_counts = last_names.value_counts()
    
    return last_name_counts


def visualize_families():
    """
    Visualize the relationship between family size, passenger class, and fare.
    
    Returns:
        Plotly figure showing family patterns
    """
    # Load data
    df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')
    
    # Get family groups data
    data = family_groups(df)
    
    # Create a line chart showing average fare by family size and class
    fig = px.line(
        data,
        x='family_size',
        y='avg_fare',
        color='Pclass',
        markers=True, 
        labels={
            'family_size': 'Family Size',
            'avg_fare': 'Average Fare',
            'Pclass': 'Passenger Class'
        }
    )
    
    fig.update_layout(
        title='Average Ticket Fare by Family Size and Passenger Class',
        xaxis_title='Family Size',
        yaxis_title='Average Fare',
    )
    
    return fig